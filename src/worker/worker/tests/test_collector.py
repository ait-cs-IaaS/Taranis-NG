import worker.collectors as collectors
from testdata import news_items
from testdata import source_include_list, source_empty_wordlist, source_exclude_list, source_include_list_exclude_list
import pytest


@pytest.fixture
def rss_collector():
    return collectors.RSSCollector()


def test_initalize_collectors():
    collectors.RSSCollector()


def test_filter_by_word_list_empty_wordlist(rss_collector):
    whitelist_results = (
        rss_collector.filter_by_word_list(news_items, source_empty_wordlist))

    assert whitelist_results == news_items


def test_filter_by_word_list_include_list(rss_collector):
    include_list_results = (
        rss_collector.filter_by_word_list(news_items, source_include_list))

    assert include_list_results == news_items[:2]


def test_filter_by_word_list_exclude_list(rss_collector):
    exclude_list_results = (
        rss_collector.filter_by_word_list(news_items, source_exclude_list))

    assert exclude_list_results == news_items[::len(news_items) - 1]


def test_filter_by_word_list_include_exclude_list(rss_collector):
    include_exclude_list_results = (
        rss_collector.filter_by_word_list(news_items, source_include_list_exclude_list))

    assert include_exclude_list_results == [news_items[0]]
