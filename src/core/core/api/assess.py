import io
from flask import request, send_file
from flask_restx import Resource, Namespace

from core.managers import auth_manager
from core.managers.sse_manager import sse_manager
from core.managers.log_manager import logger
from core.managers.auth_manager import ACLCheck, auth_required
from core.model import news_item, osint_source


class OSINTSourceGroupsAssess(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self):
        return osint_source.OSINTSourceGroup.get_all_json(None, auth_manager.get_user_from_jwt(), True)


class OSINTSourceGroupsList(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self):
        return osint_source.OSINTSourceGroup.get_all_json(search=None, user=auth_manager.get_user_from_jwt(), acl_check=True)


class OSINTSourcesList(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self):
        return osint_source.OSINTSource.get_all_with_type()


class ManualOSINTSources(Resource):
    @auth_required(["ASSESS_ACCESS"])
    def get(self):
        return osint_source.OSINTSource.get_all_by_type("MANUAL_COLLECTOR")


class AddNewsItem(Resource):
    @auth_required("ASSESS_CREATE")
    def post(self):
        osint_source_ids = news_item.NewsItemAggregate.add_news_item(request.json)
        sse_manager.news_items_updated()
        sse_manager.remote_access_news_items_updated(osint_source_ids)


class NewsItems(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self):
        user = auth_manager.get_user_from_jwt()

        try:
            filter_keys = ["search" "read", "important", "relevant", "in_analyze", "range", "sort"]
            filter_args: dict[str, str | int] = {k: v for k, v in request.args.items() if k in filter_keys}

            filter_args["group"] = request.args.get("group", osint_source.OSINTSourceGroup.get_default().id)
            filter_args["limit"] = min(int(request.args.get("limit", 20)), 200)
            page = int(request.args.get("page", 0))
            filter_args["offset"] = int(request.args.get("offset", page * filter_args["limit"]))
        except Exception as ex:
            logger.log_debug(ex)
            return "", 400

        return news_item.NewsItem.get_by_filter_json(filter_args, user)


class NewsItemAggregates(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self):
        try:
            filter_keys = ["search", "read", "unread", "important", "relevant", "in_report", "range", "sort", "source"]
            filter_args: dict[str, str | int | list] = {k: v for k, v in request.args.items() if k in filter_keys}

            filter_args["group"] = request.args.get("group", osint_source.OSINTSourceGroup.get_default().id) or "default"
            filter_args["limit"] = min(int(request.args.get("limit", 20)), 200)
            filter_args["tags"] = request.args.getlist("tags")
            page = int(request.args.get("page", 0))
            filter_args["offset"] = int(request.args.get("offset", page * filter_args["limit"]))

            return news_item.NewsItemAggregate.get_by_filter_json(filter_args, auth_manager.get_user_from_jwt())
        except Exception:
            logger.exception("Failed to get Stories")
            return "Failed to get Stories", 400


class NewsItemAggregateTags(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self):
        try:
            search = request.args.get("search", "")
            limit = int(request.args.get("limit", 20))
            offset = int(request.args.get("offset", 0))
            filter_args = {"limit": limit, "offset": offset, "search": search}
            return news_item.NewsItemTag.get_json(filter_args)
        except Exception as ex:
            logger.log_debug(ex)
            return "Failed to get Tags", 400


class NewsItemAggregateTagList(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self):
        try:
            search = request.args.get("search", "")
            limit = int(request.args.get("limit", 20))
            offset = int(request.args.get("offset", 0))
            filter_args = {"limit": limit, "offset": offset, "search": search}
            return news_item.NewsItemTag.get_list(filter_args)
        except Exception as ex:
            logger.log_debug(ex)
            return "Failed to get Tags", 400


class NewsItem(Resource):
    @auth_required("ASSESS_ACCESS", ACLCheck.NEWS_ITEM_ACCESS)
    def get(self, item_id):
        return news_item.NewsItem.get(item_id).to_dict()

    @auth_required("ASSESS_UPDATE", ACLCheck.NEWS_ITEM_MODIFY)
    def put(self, item_id):
        user = auth_manager.get_user_from_jwt()
        if not user:
            return "Invalid User", 403
        response, code = news_item.NewsItem.update(item_id, request.json, user.id)
        sse_manager.news_items_updated()
        return response, code

    @auth_required("ASSESS_DELETE", ACLCheck.NEWS_ITEM_MODIFY)
    def delete(self, item_id):
        response, code = news_item.NewsItem.delete(item_id)
        sse_manager.news_items_updated()
        return response, code


class NewsItemAggregate(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self, aggregate_id):
        return news_item.NewsItemAggregate.get_by_id(aggregate_id)

    @auth_required("ASSESS_UPDATE")
    def put(self, aggregate_id):
        user = auth_manager.get_user_from_jwt()
        response, code = news_item.NewsItemAggregate.update(aggregate_id, request.json, user)
        sse_manager.news_items_updated()
        return response, code

    @auth_required("ASSESS_DELETE")
    def delete(self, aggregate_id):
        user = auth_manager.get_user_from_jwt()
        response, code = news_item.NewsItemAggregate.delete_by_id(aggregate_id, user)
        sse_manager.news_items_updated()
        return response, code


class UnGroupAction(Resource):
    @auth_required("ASSESS_UPDATE")
    def put(self):
        user = auth_manager.get_user_from_jwt()
        newsitem_ids = request.json
        if not newsitem_ids:
            return {"No aggregate ids provided"}, 400
        response, code = news_item.NewsItemAggregate.ungroup_aggregate(newsitem_ids, user)
        sse_manager.news_items_updated()
        return response, code


class GroupAction(Resource):
    @auth_required("ASSESS_UPDATE")
    def put(self):
        user = auth_manager.get_user_from_jwt()
        aggregate_ids = request.json
        if not aggregate_ids:
            return {"No aggregate ids provided"}, 400
        response, code = news_item.NewsItemAggregate.group_aggregate(aggregate_ids, user)
        sse_manager.news_items_updated()
        return response, code


class DownloadAttachment(Resource):
    @auth_required("ASSESS_ACCESS")
    def get(self, item_data_id, attribute_id):
        user = auth_manager.get_user_from_jwt()
        attribute_mapping = news_item.NewsItemDataNewsItemAttribute.find(attribute_id)
        need_check = attribute_mapping is not None
        attribute = news_item.NewsItemAttribute.find(attribute_id)
        if (
            need_check
            and item_data_id == attribute_mapping.news_item_data_id
            and news_item.NewsItemData.allowed_with_acl(
                attribute_mapping.news_item_data_id,
                user,
                False,
                True,
                False,
            )
        ):
            logger.store_user_activity(user, "ASSESS_ACCESS", str({"file": attribute.value}))
            return send_file(
                io.BytesIO(attribute.binary_data),
                download_name=attribute.value,
                mimetype=attribute.binary_mime_type,
                as_attachment=True,
            )
        else:
            logger.store_auth_error_activity("Unauthorized access attempt to News Item Data")


def initialize(api):
    namespace = Namespace("Assess", description="Assess related operations", path="/api/v1/assess")
    namespace.add_resource(OSINTSourceGroupsAssess, "/osint-source-groups")
    namespace.add_resource(OSINTSourceGroupsList, "/osint-source-group-list")
    namespace.add_resource(OSINTSourcesList, "/osint-sources-list")
    namespace.add_resource(ManualOSINTSources, "/manual-osint-sources")
    namespace.add_resource(AddNewsItem, "/news-items")
    namespace.add_resource(
        NewsItemAggregates,
        "/news-item-aggregates",
    )
    namespace.add_resource(
        NewsItems,
        "/news-items",
    )
    namespace.add_resource(NewsItemAggregateTags, "/tags")
    namespace.add_resource(NewsItemAggregateTagList, "/taglist")

    namespace.add_resource(NewsItem, "/news-items/<int:item_id>")
    namespace.add_resource(NewsItemAggregate, "/news-item-aggregates/<int:aggregate_id>")
    namespace.add_resource(GroupAction, "/news-item-aggregates/group")
    namespace.add_resource(UnGroupAction, "/news-item-aggregates/ungroup")
    namespace.add_resource(
        DownloadAttachment,
        "/news-item-data/<string:item_data_id>/attributes/<int:attribute_id>/file",
    )
    api.add_namespace(namespace)
