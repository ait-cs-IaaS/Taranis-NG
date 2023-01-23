import datetime

from bots.managers.log_manager import logger
from shared.schema import bot
from shared.schema.parameter import Parameter, ParameterType
from bots.remote.core_api import CoreApi


class BaseBot:
    type = "BASE_BOT"
    name = "Base Bot"
    description = "Base abstract type for all bots"

    parameters = [
        Parameter(
            0,
            "REFRESH_INTERVAL",
            "Refresh Interval",
            "How often is this bot doing its job",
            ParameterType.NUMBER,
        )
    ]

    def __init__(self):
        self.core_api = CoreApi()
        self.bots = []

    def get_info(self):
        info_schema = bot.BotSchema()
        return info_schema.dump(self)

    def execute(self, source):
        pass

    def execute_on_event(self, preset, event_type, data):
        pass

    @staticmethod
    def print_exception(preset, error):
        logger.log_debug(f"Bot Preset ID: {preset.id}\tName: {preset.name}")
        logger.log_debug_trace(error)

    @staticmethod
    def history(interval):
        if interval[0].isdigit() and ":" in interval:
            limit = datetime.datetime.now() - datetime.timedelta(days=1)
        elif interval[0].isalpha():
            limit = datetime.datetime.now() - datetime.timedelta(weeks=1)
        elif int(interval) > 60:
            hours = int(interval) // 60
            minutes = int(interval) - hours * 60
            limit = datetime.datetime.now() - datetime.timedelta(days=0, hours=hours, minutes=minutes)

        else:
            limit = datetime.datetime.now() - datetime.timedelta(days=0, hours=0, minutes=int(interval))

        limit = limit.strftime("%d.%m.%Y - %H:%M")
        return limit

    def refresh(self):
        logger.log_info(f"Core API requested a refresh Bot {self.type}...")
        response, code = self.core_api.get_bots()

        if code != 200 or response is None:
            logger.log_debug(f"HTTP {code}: Got the following reply: {response}")
            return

        try:
            bot_schema = bot.BotSchema(many=True)
            self.bots = bot_schema.load(response)

            for bot in self.bots:
                self.execute(bot)

        except Exception:
            logger.log_debug_trace()
