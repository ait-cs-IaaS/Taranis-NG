import json
from flask import request
from flask_restx import Resource, Namespace
from datetime import datetime, timedelta

from core.managers import bots_manager
from core.managers.sse_manager import sse_manager
from core.managers.log_manager import logger
from core.managers.auth_manager import api_key_required
from core.model import news_item, word_list, bots_node, bot


class BotGroupAction(Resource):
    @api_key_required
    def put(self):
        aggregate_ids = request.json
        if not aggregate_ids:
            return {"No aggregate ids provided"}, 400
        response, code = news_item.NewsItemAggregate.group_aggregate(aggregate_ids)
        sse_manager.news_items_updated()
        return response, code


class BotUnGroupAction(Resource):
    @api_key_required
    def put(self):
        newsitem_ids = request.json
        if not newsitem_ids:
            return {"No aggregate ids provided"}, 400
        response, code = news_item.NewsItemAggregate.ungroup_aggregate(newsitem_ids)
        sse_manager.news_items_updated()
        return response, code


class NewsItemData(Resource):
    @api_key_required
    def get(self):
        try:
            limit = request.args.get("limit", default=(datetime.now() - timedelta(weeks=1)).isoformat())
            return news_item.NewsItemData.get_all_news_items_data(limit)
        except Exception:
            logger.log_debug_trace("GET /news-item-data failed")
            return "", 400


class UpdateNewsItemData(Resource):
    @api_key_required
    def put(self, news_item_data_id):
        try:
            if not request.json:
                return {"Not update data provided"}
            if language := request.json.get("language"):
                return news_item.NewsItemData.update_news_item_lang(news_item_data_id, language)
            return {"Not implemented"}
        except Exception:
            logger.log_debug_trace("GET /news-item-data failed")
            return "", 400


class BotsNode(Resource):
    @api_key_required
    def get(self, node_id):
        return bots_node.BotsNode.get_json_by_id(node_id)

    @api_key_required
    def put(self, node_id):
        return bots_manager.update_bots_node(node_id, request.json)

    @api_key_required
    def post(self):
        return bots_manager.add_bots_node(request.json)

    @api_key_required
    def delete(self, node_id):
        bots_node.BotsNode.delete(node_id)


class UpdateNewsItemAttributes(Resource):
    @api_key_required
    def put(self, news_item_data_id):
        news_item.NewsItemData.update_news_item_attributes(news_item_data_id, request.json)


class UpdateNewsItemTags(Resource):
    @api_key_required
    def put(self, aggregate_id):
        if data := request.json:
            return news_item.NewsItemAggregate.update_tags(aggregate_id, data)


class UpdateNewsItemsAggregateSummary(Resource):
    @api_key_required
    def put(self, aggregate_id):
        news_item.NewsItemAggregate.update_news_items_aggregate_summary(aggregate_id, request.json)


class GetNewsItemsAggregate(Resource):
    @api_key_required
    def get(self, group_id):
        limit = request.args.get("limit", "")
        resp_str = news_item.NewsItemAggregate.get_news_items_aggregate(group_id, limit)
        return json.loads(resp_str)


class GetDefaultNewsItemsAggregate(Resource):
    @api_key_required
    def get(self):
        limit = request.args.get("limit", "")
        resp_str = news_item.NewsItemAggregate.get_default_news_items_aggregate(limit)
        return json.loads(resp_str)


class WordListEntries(Resource):
    @api_key_required
    def delete(self, word_list_id, entry_name):
        return word_list.WordListEntry.delete_entries(word_list_id, entry_name)

    @api_key_required
    def put(self, word_list_id, entry_name):
        return word_list.WordListEntry.update_word_list_entries(word_list_id, request.json)


class BotsInfo(Resource):
    def get(self):
        search = request.args.get(key="search", default=None)
        return bot.Bot.get_all_json(search)


class BotInfo(Resource):
    def get(self, bot_id):
        return bot.Bot.get_by_id(bot_id)

    def put(self, bot_id):
        return bot.Bot.update_bot_parameters(bot_id, request.json)


def initialize(api):
    namespace = Namespace("bots", description="Bots related operations", path="/api/v1/bots")
    namespace.add_resource(BotsInfo, "/")
    namespace.add_resource(BotInfo, "/<string:bot_id>")
    namespace.add_resource(NewsItemData, "/news-item-data")
    namespace.add_resource(
        UpdateNewsItemTags,
        "/news-items-aggregate/<string:aggregate_id>/tags",
    )
    namespace.add_resource(
        UpdateNewsItemData,
        "/news-item-data/<string:news_item_data_id>",
    )
    namespace.add_resource(
        UpdateNewsItemAttributes,
        "/news-item-data/<string:news_item_data_id>/attributes",
    )
    namespace.add_resource(BotGroupAction, "/news-item-aggregates/group")
    namespace.add_resource(BotUnGroupAction, "/news-item-aggregates/ungroup")
    namespace.add_resource(
        GetNewsItemsAggregate,
        "/news-item-aggregates-by-group/<string:group_id>",
    )
    namespace.add_resource(
        UpdateNewsItemsAggregateSummary,
        "/news-items-aggregate/<string:aggregate_id>/summary",
    )
    namespace.add_resource(GetDefaultNewsItemsAggregate, "/news-item-aggregates")
    namespace.add_resource(
        WordListEntries,
        "/word-list/<int:word_list_id>/entries/<string:entry_name>",
    )
    namespace.add_resource(BotsNode, "/node/<string:node_id>", "/node")
    api.add_namespace(namespace)
