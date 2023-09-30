from datetime import datetime, timedelta
from typing import Any
from sqlalchemy import orm, func, or_, and_, String as SQLString
from sqlalchemy.sql.expression import cast

from core.managers.db_manager import db
from core.model.acl_entry import ACLEntry, ItemType
from core.model.report_item import ReportItem
from core.model.base_model import BaseModel


class Product(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title: Any = db.Column(db.String(), nullable=False)
    description: Any = db.Column(db.String())

    created = db.Column(db.DateTime, default=datetime.now)

    product_type_id = db.Column(db.Integer, db.ForeignKey("product_type.id"))
    product_type = db.relationship("ProductType")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    report_items = db.relationship("ReportItem", secondary="product_report_item")
    last_rendered = db.Column(db.DateTime)
    render_result = orm.deferred(db.Column(db.LargeBinary))

    def __init__(self, title, product_type_id, description="", report_items=None, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.product_type_id = product_type_id
        self.report_items = [ReportItem.get(report_item) for report_item in report_items] if report_items else []

    @classmethod
    def count_all(cls):
        return cls.query.count()

    @classmethod
    def get_detail_json(cls, product_id):
        return product.to_dict() if (product := cls.get(product_id)) else None

    @classmethod
    def get_by_filter(cls, filter, user):
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
                cast(Product.product_type_id, SQLString) == ACLEntry.item_id,
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
        results, count = cls.get_by_filter(filter, user)
        products = []
        for result in results:
            product = result.Product
            product.see = True
            product.access = result.access > 0 or result.acls == 0
            product.modify = result.modify > 0 or result.acls == 0
            products.append(product)

        items = [product.to_dict() for product in products]
        return {"total_count": count, "items": items}

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["report_items"] = [report_item.id for report_item in self.report_items if report_item]
        data.pop("render_result", None)
        return data

    def update_render(self, render_result):
        try:
            self.last_rendered = datetime.now()
            self.render_result = render_result
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @classmethod
    def update_render_for_id(cls, product_id, render_result):
        product = cls.get(product_id)
        if not product:
            return {"error": f"Product {product_id} not found"}, 404
        if product.update_render(render_result):
            return {"message": f"Product {product_id} updated"}, 200
        return {"error": f"Product {product_id} not updated"}, 500

    @classmethod
    def get_render(cls, product_id):
        if product := cls.get(product_id):
            if product.render_result:
                return {"mime_type": product.product_type.get_mimetype(), "blob": product.render_result}
        return None

    @classmethod
    def update(cls, product_id, data) -> tuple[dict, int]:
        product = Product.get(product_id)
        if product is None:
            return {"error": f"Product {product_id} not found"}, 404
        new_product = cls.from_dict(data)
        for key, value in vars(new_product).items():
            if hasattr(product, key) and key != "id":
                setattr(product, key, value)

        db.session.commit()
        return {"message": f"Product {product_id} updated"}, 200


class ProductReportItem(BaseModel):
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    report_item_id = db.Column(db.Integer, db.ForeignKey("report_item.id", ondelete="CASCADE"), primary_key=True)
