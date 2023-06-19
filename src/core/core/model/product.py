from datetime import datetime, timedelta
import sqlalchemy
from marshmallow import fields
from marshmallow import post_load
from sqlalchemy import orm, func, or_, and_
from sqlalchemy.sql.expression import cast

from core.managers.db_manager import db
from core.model.acl_entry import ACLEntry
from core.model.report_item import ReportItem
from shared.schema.acl_entry import ItemType
from shared.schema.product import ProductPresentationSchema, ProductSchemaBase
from shared.schema.report_item import ReportItemIdSchema


class NewProductSchema(ProductSchemaBase):
    report_items = fields.Nested(ReportItemIdSchema, many=True)

    @post_load
    def make(self, data, **kwargs):
        return Product(**data)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    created = db.Column(db.DateTime, default=datetime.now)

    product_type_id = db.Column(db.Integer, db.ForeignKey("product_type.id"))
    product_type = db.relationship("ProductType")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    report_items = db.relationship("ReportItem", secondary="product_report_item")

    def __init__(self, title, description, product_type_id, report_items, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.product_type_id = product_type_id
        self.tag = ""

        self.report_items = [ReportItem.find(report_item.id) for report_item in report_items]

    @orm.reconstructor
    def reconstruct(self):
        self.tag = "mdi-file-pdf-outline"

    @classmethod
    def count_all(cls):
        return cls.query.count()

    @classmethod
    def find(cls, product_id):
        return cls.query.get(product_id)

    @classmethod
    def get_detail_json(cls, product_id):
        product = cls.query.get(product_id)
        products_schema = ProductPresentationSchema()
        return products_schema.dump(product)

    @classmethod
    def get(cls, filter, user):
        query = (
            db.session.query(
                Product,
                func.count().filter(ACLEntry.id is not None).label("acls"),
                func.count().filter(ACLEntry.access).label("access"),
                func.count().filter(ACLEntry.modify).label("modify"),
            )
            .distinct()
            .group_by(Product.id)
        )

        query = query.outerjoin(
            ACLEntry,
            and_(
                cast(Product.product_type_id, sqlalchemy.String) == ACLEntry.item_id,
                ACLEntry.item_type == ItemType.PRODUCT_TYPE,
            ),
        )
        query = ACLEntry.apply_query(query, user, True, False, False)

        search = filter.get("search")
        if search and search != "":
            query = query.filter(
                or_(
                    Product.title.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                )
            )

        if "range" in filter and filter["range"].upper() != "ALL":
            filter_range = filter["range"].upper()
            date_limit = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            if filter_range == "WEEK":
                date_limit -= timedelta(days=date_limit.weekday())

            elif filter_range == "MONTH":
                date_limit = date_limit.replace(day=1)

            query = query.filter(Product.created >= date_limit)

        if "sort" in filter:
            if filter["sort"] == "DATE_DESC":
                query = query.order_by(db.desc(Product.created))

            elif filter["sort"] == "DATE_ASC":
                query = query.order_by(db.asc(Product.created))

        offset = filter.get("offset", 0)
        limit = filter.get("limit", 20)
        return query.offset(offset).limit(limit).all(), query.count()

    @classmethod
    def get_json(cls, filter, user):
        results, count = cls.get(filter, user)
        products = []
        for result in results:
            product = result.Product
            product.see = True
            product.access = result.access > 0 or result.acls == 0
            product.modify = result.modify > 0 or result.acls == 0
            products.append(product)

            for report_item in product.report_items:
                report_item.see = True
                report_item.access = True
                report_item.modify = False

        products_schema = ProductPresentationSchema(many=True)
        return {"total_count": count, "items": products_schema.dump(products)}

    @classmethod
    def add_product(cls, product_data, user_id):
        product = cls.from_dict(product_data)
        product.user_id = user_id
        db.session.add(product)
        db.session.commit()

        return product.id

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def update(cls, product_id, data) -> tuple[str, int]:
        product = Product.find(product_id)
        if product is None:
            return f"Product {product_id} not found", 404
        new_product = cls.from_dict(data)
        for key, value in vars(new_product).items():
            if hasattr(product, key) and key != "id":
                setattr(product, key, value)

        db.session.commit()
        return f"Product {product_id} updated", 200

    @classmethod
    def delete(cls, id):
        product = cls.query.get(id)
        if product is not None:
            db.session.delete(product)
            db.session.commit()


class ProductReportItem(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    report_item_id = db.Column(db.Integer, db.ForeignKey("report_item.id"), primary_key=True)
