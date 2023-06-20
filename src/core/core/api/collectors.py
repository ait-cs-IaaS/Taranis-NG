from flask import request
from flask_restx import Resource, Namespace

from core.managers import collectors_manager
from core.managers.sse_manager import sse_manager
from core.managers.auth_manager import api_key_required
from core.managers.log_manager import logger
from core.model import osint_source, news_item, collectors_node


class OSINTSourcesForCollectors(Resource):
    @api_key_required
    def get(self, collector_type):
        try:
            return osint_source.OSINTSource.get_all_by_type(collector_type)
        except Exception:
            logger.log_debug_trace()


class AddNewsItems(Resource):
    @api_key_required
    def post(self):
        json_data = request.json
        osint_source_ids = news_item.NewsItemAggregate.add_news_items(json_data)
        sse_manager.news_items_updated()
        sse_manager.remote_access_news_items_updated(osint_source_ids)


class CollectorsNode(Resource):
    @api_key_required
    def get(self, node_id):
        return collectors_node.CollectorsNode.get_json_by_id(node_id)

    @api_key_required
    def put(self, node_id):
        return collectors_manager.update_collectors_node(node_id, request.json)

    @api_key_required
    def post(self):
        return collectors_manager.add_collectors_node(request.json)

    @api_key_required
    def delete(self, node_id):
        collectors_node.CollectorsNode.delete(node_id)


def initialize(api):
    namespace = Namespace("Collectors", description="Collectors related operations", path="/api/v1/collectors")
    namespace.add_resource(
        OSINTSourcesForCollectors,
        "/osint-sources/<string:collector_type>",
    )
    namespace.add_resource(AddNewsItems, "/news-items")
    namespace.add_resource(CollectorsNode, "/node/<string:node_id>", "/node")
    api.add_namespace(namespace)
