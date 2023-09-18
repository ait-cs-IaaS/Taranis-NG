from .base_bot import BaseBot
from worker.log import logger
import py3langid
import torch
from flair.data import Sentence
from flair.nn import Classifier


class NLPBot(BaseBot):
    type = "NLP_BOT"
    name = "NLP Bot"
    description = "Bot for naturale language processing of news items"

    def __init__(self):
        super().__init__()
        logger.debug("Setup NER Model...")
        self.ner_model = Classifier.load("flair/ner-multi")
        torch.set_num_threads(1)  # https://github.com/pytorch/pytorch/issues/36191
        self.extraction_text_limit = 5000

    def execute(self, parameters=None):
        if not parameters:
            return
        try:
            filter_dict = self.get_filter_dict(parameters)

            data = self.core_api.get_news_items_aggregate(filter_dict)
            if not data:
                logger.critical("Error getting news items")
                return

            all_keywords = {k: v for news_item in data for k, v in news_item["tags"].items()}

            update_result = {}

            logger.debug(f"All Keywords: {all_keywords}")
            for aggregate in data:
                current_keywords = self.extract_keywords(aggregate, all_keywords)
                all_keywords |= current_keywords
                update_result[aggregate["id"]] = current_keywords
            self.core_api.update_tags(update_result)

        except Exception:
            logger.log_debug_trace(f"Error running Bot: {self.type}")

    def extract_keywords(self, aggregate: dict, all_keywords: dict) -> dict:
        current_keywords = aggregate.get("tags", {})
        # drop "name" from current_keywords
        current_keywords = {k: v for k, v in current_keywords.items() if k != "name"}
        aggregate_content = " ".join(news_item["news_item_data"]["content"] for news_item in aggregate["news_items"])
        current_keywords |= self.extract_ner(aggregate_content[: self.extraction_text_limit], all_keywords)

        logger.debug(current_keywords)
        return current_keywords

    def extract_ner(self, text: str, all_keywords) -> dict:
        ner_model = self.ner_model
        sentence = Sentence(text)
        ner_model.predict(sentence)
        current_keywords = {}
        for ent in sentence.get_labels():
            tag = ent.data_point.text
            if len(tag) > 2 and ent.score > 0.98:
                tag_type = all_keywords[tag]["tag_type"] if tag in all_keywords else ent.value
                current_keywords[tag] = {"tag_type": tag_type}

        return current_keywords

    def detect_language(self, text) -> str:
        return py3langid.classify(text)[0]

    # def not_in_stopwords(self, keyword: str) -> bool:
    #    return keyword not in stopwords.words(self.language)
