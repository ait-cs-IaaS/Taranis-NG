import base64
from flask import Response
from flask import request
from flask_restx import Resource, Namespace

from core.managers import auth_manager, presenters_manager, publishers_manager
from core.managers.log_manager import logger
from core.managers.auth_manager import auth_required, ACLCheck
from core.model import product, publisher_preset


class Products(Resource):
    @auth_required("PUBLISH_ACCESS")
    def get(self):
        try:
            filter_keys = ["search", "range", "sort"]
            filter_args: dict[str, str | int | list] = {k: v for k, v in request.args.items() if k in filter_keys}

            filter_args["limit"] = min(int(request.args.get("limit", 20)), 200)
            filter_args["offset"] = int(request.args.get("offset", 0))
            return product.Product.get_json(filter_args, auth_manager.get_user_from_jwt())
        except Exception:
            logger.exception("Failed to get Products")
            return "Failed to get Products", 400

    @auth_required("PUBLISH_CREATE")
    def post(self):
        user = auth_manager.get_user_from_jwt()
        if user is None:
            return "Creating Product Failed", 401
        return product.Product.add_product(request.json, user.id), 201


class Product(Resource):
    @auth_required("PUBLISH_UPDATE", ACLCheck.PRODUCT_TYPE_ACCESS)
    def get(self, product_id):
        return product.Product.get_detail_json(product_id)

    @auth_required("PUBLISH_UPDATE", ACLCheck.PRODUCT_TYPE_MODIFY)
    def put(self, product_id):
        product.Product.update(product_id, request.json)

    @auth_required("PUBLISH_DELETE", ACLCheck.PRODUCT_TYPE_MODIFY)
    def delete(self, product_id):
        return product.Product.delete(product_id)


class PublishProduct(Resource):
    @auth_required("PUBLISH_PRODUCT")
    def post(self, product_id, publisher_id):
        product_data, status_code = presenters_manager.generate_product(product_id)
        if status_code == 200:
            return publishers_manager.publish(
                publisher_preset.PublisherPreset.find(publisher_id),
                product_data,
                None,
                None,
                None,
            )
        else:
            return "Failed to generate product", status_code


class ProductsOverview(Resource):
    @auth_required("PUBLISH_ACCESS")
    def get(self, product_id):
        product_data, status_code = presenters_manager.generate_product(product_id)
        if status_code == 200:
            return Response(
                base64.b64decode(product_data["data"]),
                mimetype=product_data["mime_type"],
            )
        return "Failed to generate product", status_code


def initialize(api):
    namespace = Namespace("publish", description="Publish API", path="/api/v1/publish")
    namespace.add_resource(Products, "/products")
    namespace.add_resource(Product, "/products/<int:product_id>")
    namespace.add_resource(ProductsOverview, "/products/<int:product_id>/overview")
    namespace.add_resource(
        PublishProduct,
        "/products/<int:product_id>/publishers/<string:publisher_id>",
    )
    api.add_namespace(namespace)
