from .base_bot import BaseBot
from worker.log import logger
import spacy
import spacy.cli
import py3langid
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from polyfuzz import PolyFuzz
from polyfuzz.models import TFIDF
from pandas import DataFrame
import numpy
import nltk
import torch


class NLPBot(BaseBot):
    type = "NLP_BOT"
    name = "NLP Bot"
    description = "Bot for naturale language processing of news items"

    def __init__(self):
        super().__init__()
        logger.debug("Setup NER Model...")
        self.ner_model = spacy.load("xx_ent_wiki_sm")
        torch.set_num_threads(1)  # https://github.com/pytorch/pytorch/issues/36191
        self.polyfuzz_model = PolyFuzz(TFIDF(model_id="TF-IDF", clean_string=False, n_gram_range=(3, 3), min_similarity=0))  # type: ignore
        self.wordnet_lemmatizer = WordNetLemmatizer()
        nltk.download("wordnet")
        nltk.download("stopwords")
        self.language = ""
        self.extraction_text_limit = 5000
        self.patch_bert_logger()

    def patch_bert_logger(self):
        import logging

        bert_logger = logging.getLogger("BERTopic")

        class IgnoreSpecificLogFilter(logging.Filter):
            def filter(self, record: logging.LogRecord) -> bool:
                return "Ran model with model id" not in record.getMessage()

        bert_logger.addFilter(IgnoreSpecificLogFilter())

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
        aggregate_content = ""

        for news_item in aggregate["news_items"]:
            content = news_item["news_item_data"]["content"]
            aggregate_content += content

            language = news_item["news_item_data"]["language"]
            if language == "":
                self.language = self.detect_language(content)
                self.core_api.update_news_item_data(news_item["news_item_data"]["id"], {"language": self.language})
            else:
                self.language = language

        current_keywords.update(self.extract_ner(aggregate_content[: self.extraction_text_limit]))
        current_keywords.update(self.lemmatize(current_keywords))

        from_list, to_list = self.polyfuzz(list(all_keywords.keys()), list(current_keywords.keys()))
        current_keywords = self.update_keywords_from_polyfuzz(from_list, to_list, all_keywords, current_keywords)
        current_keywords = self.cleanup_keywords(current_keywords)
        logger.debug(current_keywords)
        return current_keywords

    def extract_ner(self, text: str) -> dict:
        ner_model = self.ner_model
        doc = ner_model(text)
        return {
            ent.text.lower(): {"tag_type": ent.label_, "sub_forms": []}
            for ent in doc.ents
            if 16 > len(ent.text) > 2 and self.not_in_stopwords(ent.text)
        }

    def lemmatize(self, keywords: dict) -> dict:
        result = {}
        for keyword in keywords:
            baseform = self.wordnet_lemmatizer.lemmatize(keyword)
            result[baseform] = keywords[keyword]
            if baseform != keyword:
                result[baseform]["sub_forms"].append(keyword)
        return result

    def detect_language(self, text) -> str:
        return py3langid.classify(text)[0]

    def not_in_stopwords(self, keyword: str) -> bool:
        return keyword not in stopwords.words(self.language)

    def cleanup_keywords(self, keywords: dict) -> dict:
        keyword_names = set(keywords.keys())
        for keyword in keywords.values():
            keyword["sub_forms"] = list({sub_form for sub_form in keyword["sub_forms"] if sub_form not in keyword_names})
        return keywords

    def polyfuzz(self, from_list: list[str], to_list: list[str]) -> tuple[list, list]:
        if len(from_list) < 2 or len(to_list) < 2:
            logger.debug("Not enough keywords to run polyfuzz")
            return [], []
        self.polyfuzz_model.match(from_list, to_list).group(link_min_similarity=0.75)
        df: DataFrame = DataFrame(self.polyfuzz_model.get_matches())
        values = df[df["Similarity"] >= 0.65]
        values = values.replace(numpy.nan, None)
        return values["From"].tolist(), values["To"].tolist()

    def update_keywords_from_polyfuzz(self, values_from, values_to, all_keywords: dict, current_keywords: dict) -> dict:
        for i, matching_value in enumerate(values_from):
            matching_entry = all_keywords[matching_value]
            if matching_value in current_keywords:
                current_keywords[matching_value]["sub_forms"] += matching_entry["sub_forms"]
            if values_to[i] in current_keywords:
                matching_entry["sub_forms"] += [values_to[i]]
                current_keywords[values_to[i]] = matching_entry

        return current_keywords
