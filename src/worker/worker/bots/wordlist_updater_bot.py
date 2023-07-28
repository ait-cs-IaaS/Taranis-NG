import requests

from .base_bot import BaseBot
from worker.log import logger


class WordlistUpdaterBot(BaseBot):
    type = "WORDLIST_UPDATER_BOT"
    name = "Wordlist Updater Bot"
    description = "Bot for updating word lists"

    def parse_csv(self, content):

        pass

    def parse_json(self, content):
        pass

    def execute(self, word_list):
        url = word_list["link"]
        logger.info(f"Updating word list {word_list['name']} from {url}")
        response = requests.get(url=url)
        if not response.ok:
            logger.error(f"Failed to update word list {word_list['name']}")
            return
        content_type = response.headers['content-type']
        entries = {}
        if content_type == "text/csv":
            entries = self.parse_csv(response.content)
        elif content_type == "application/json":
            entries = self.parse_json(response.content)
        else:
            logger.error(f"Unsupported content type {content_type}")
            return
        word_list["entries"] = entries

        self.core_api.update_word_list(word_list)
        logger.info(f"Word list {word_list['name']} updated")
        return f"Word list {word_list['name']} updated"
