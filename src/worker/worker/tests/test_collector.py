import worker.collectors as collectors
from testdata import news_items
from testdata import source_include_list, source_empty_wordlist, source_exclude_list, source_include_list_exclude_list
import pytest


@pytest.fixture
def rss_collector():
    return collectors.RSSCollector()


def test_initalize_collectors():
    collectors.RSSCollector()


@pytest.mark.parametrize("input_news_items",
                         [news_items, news_items[2:], news_items[::len(news_items) - 1], [news_items[-1]]])
def test_filter_by_word_list_empty_wordlist(rss_collector, input_news_items):
    emptylist_results = (
        rss_collector.filter_by_word_list(input_news_items, source_empty_wordlist))

    assert emptylist_results == input_news_items


@pytest.mark.parametrize("input_news_items,expected_news_items",
                         [(news_items, news_items[:2]), (news_items[2:], []),
                          (news_items[::len(news_items) - 1], [news_items[0]]), ([news_items[-1]], [])])
def test_filter_by_word_list_include_list(rss_collector, input_news_items, expected_news_items):
    include_list_results = (
        rss_collector.filter_by_word_list(input_news_items, source_include_list))

    assert include_list_results == expected_news_items


@pytest.mark.parametrize("input_news_items,expected_news_items",
                         [(news_items, news_items[::len(news_items) - 1]), (news_items[2:], [news_items[-1]]),
                          (news_items[::len(news_items) - 1], news_items[::len(news_items) - 1]),
                          ([news_items[-1]], [news_items[-1]])])
def test_filter_by_word_list_exclude_list(rss_collector, input_news_items, expected_news_items):
    exclude_list_results = (
        rss_collector.filter_by_word_list(input_news_items, source_exclude_list))

    assert exclude_list_results == expected_news_items


@pytest.mark.parametrize("input_news_items,expected_news_items",
                         [(news_items, [news_items[0]]), (news_items[2:], []),
                          (news_items[::len(news_items) - 1], [news_items[0]]), ([news_items[-1]], [])])
def test_filter_by_word_list_include_exclude_list(rss_collector, input_news_items, expected_news_items):
    include_exclude_list_results = (
        rss_collector.filter_by_word_list(input_news_items, source_include_list_exclude_list))

    assert include_exclude_list_results == expected_news_items
