import datetime
from typing import Any
from sqlalchemy import or_, and_
import sqlalchemy
from sqlalchemy.sql.expression import cast

from core.managers.db_manager import db
from core.model.product import Product
from core.model.base_model import BaseModel
from core.model.acl_entry import ACLEntry, ItemType


class ProductType(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    presenter_id = db.Column(db.String, db.ForeignKey("presenter.id"))
    presenter = db.relationship("Presenter")

    parameter_values = db.relationship("ParameterValue", secondary="product_type_parameter_value", cascade="all")

    def __init__(self, title, description, presenter_id, parameter_values, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.presenter_id = presenter_id
        self.parameter_values = parameter_values

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(ProductType.title)).all()

    @classmethod
    def allowed_with_acl(cls, product_id, user, see, access, modify):
        product = db.session.query(Product).filter_by(id=product_id).first()
        if not product:
            return False

        query = db.session.query(ProductType.id).distinct().group_by(ProductType.id).filter(ProductType.id == product.product_type_id)

        query = query.outerjoin(
            ACLEntry,
            and_(
                cast(ProductType.id, sqlalchemy.String) == ACLEntry.item_id,
                ACLEntry.item_type == ItemType.PRODUCT_TYPE,
            ),
        )

        query = ACLEntry.apply_query(query, user, see, access, modify)

        return query.scalar() is not None

    @classmethod
    def get_by_filter(cls, search, user, acl_check):
        query = cls.query.distinct().group_by(ProductType.id)

        if acl_check:
            query = query.outerjoin(
                ACLEntry,
                and_(
                    cast(ProductType.id, sqlalchemy.String) == ACLEntry.item_id,
                    ACLEntry.item_type == ItemType.PRODUCT_TYPE,
                ),
            )
            query = ACLEntry.apply_query(query, user, True, False, False)

        if search:
            query = query.filter(
                or_(
                    ProductType.title.ilike(f"%{search}%"),
                    ProductType.description.ilike(f"%{search}%"),
                )
            )

        return query.order_by(db.asc(ProductType.title)).all(), query.count()

    @classmethod
    def get_all_json(cls, search, user, acl_check):
        product_types, count = cls.get_by_filter(search, user, acl_check)
        items = [product_type.to_dict() for product_type in product_types]
        return {"total_count": count, "items": items}

    @classmethod
    def update(cls, preset_id, data):
        product_type = cls.query.get(preset_id)
        updated_product_type = cls.from_dict(data)
        product_type.title = updated_product_type.title
        product_type.description = updated_product_type.description

        for value in product_type.parameter_values:
            for updated_value in updated_product_type.parameter_values:
                if value.parameter_key == updated_value.parameter_key:
                    value.value = updated_value.value

        db.session.commit()
        return product_type.id

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["parameter_values"] = [value.to_dict() for value in self.parameter_values]
        data["tag"] = "mdi-file-document-outline"
        return data


class ProductTypeParameterValue(BaseModel):
    product_type_id = db.Column(db.Integer, db.ForeignKey("product_type.id"), primary_key=True)
    parameter_value_id = db.Column(db.Integer, db.ForeignKey("parameter_value.id"), primary_key=True)
