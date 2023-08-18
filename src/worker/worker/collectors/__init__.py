from worker.collectors.base_collector import BaseCollector
from worker.collectors.email_collector import EmailCollector
from worker.collectors.rss_collector import RSSCollector
from worker.collectors.twitter_collector import TwitterCollector

# from worker.collectors.web_collector import WebCollector

__all__ = [
    "BaseCollector",
    "EmailCollector",
    "RSSCollector",
    "TwitterCollector",
    # "WebCollector",
]
