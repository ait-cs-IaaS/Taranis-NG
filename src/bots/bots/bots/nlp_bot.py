from .base_bot import BaseBot
from bots.managers.log_manager import logger
import datetime
from keybert import KeyBERT
from nltk.corpus import stopwords


class NLPBot(BaseBot):
    type = "NLP_BOT"
    name = "NLP Bot"
    description = "Bot for naturale language processing of news items"

    def execute(self):
        try:
            source_group = self.parameters.get("SOURCE_GROUP", None)
            language = self.parameters["LANGUAGE"].lower()

            if language == "en":
                kw_model = KeyBERT("all-MiniLM-L6-v2")
            elif language == "de":
                kw_model = KeyBERT("paraphrase-mpnet-base-v2")

            limit = self.history()
            logger.log_debug(f"LIMIT: {limit}")

            data = self.core_api.get_news_items_aggregate(source_group, limit)
            if not data:
                logger.critical(f"Error getting news items")
                return

            for aggregate in data:
                findings = {}
                for news_item in aggregate["news_items"]:
                    content = news_item["news_item_data"]["content"]

                    findings[news_item["id"]] = self.generateKeywords(language, kw_model, content)

                for news_id, keywords in findings.items():
                    keyword = [i[0] for i in keywords]
                    logger.log_debug(f"news_id: {news_id}, keyword: {keyword}")
                    self.core_api.update_news_item_tags(news_id, keyword)

        except Exception as error:
            logger.log_debug_trace(f"Error running Bot: {self.type}")

    def execute_on_event(self, event_type, data):
        try:
            # source_group = preset.parameter_values["SOURCE_GROUP"]
            # keywords = preset.parameter_values["KEYWORDS"]
            pass
        except Exception as error:
            logger.log_debug_trace(f"Error running Bot: {self.type}")

    def generateKeywords(self, language, kw_model, text):
        if language == "en":
            keywords = kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words="english",
                use_mmr=True,
                diversity=0.8,
                top_n=15,
            )
        elif language == "de":
            german_stop_words = stopwords.words("german")
            keywords = kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words=german_stop_words,
                use_mmr=True,
                diversity=0.8,
                top_n=15,
            )

        return keywords
