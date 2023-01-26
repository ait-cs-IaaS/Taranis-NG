from .base_collector import BaseCollector


class ManualCollector(BaseCollector):
    type = "MANUAL_COLLECTOR"
    name = "Manual Collector"
    description = "Collector for manual input of news items"

    def collect(self, source):
        pass
