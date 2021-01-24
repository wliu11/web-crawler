import re
import unittest
from crawler import Crawler
from bs4 import BeautifulSoup as soup


class TestCrawler(unittest.TestCase):
    def test_rescale_homepage(self):
        crawler = Crawler(limit=2, url="http://rescale.com")
        script_links = crawler.crawl("http://rescale.com")
        test_links = []
        print("length of script link is ", len(script_links))

        with open('rescale_html.html') as f:
            page_soup = soup(f, "html.parser")
            search_criteria = re.compile("^(http|https)://")
            results = page_soup.findAll('a', attrs={'href': search_criteria})

            for unedited_link in results:
                link = unedited_link.get('href')
                test_links.append(link)

        assert len(script_links) == len(test_links)
        assert script_links == test_links

    def test_rescale_resouces(self):
        crawler = Crawler(limit=2, url="https://resources.rescale.com")
        script_links = crawler.crawl("https://resources.rescale.com")
        test_links = []
        print("length of script link is ", len(script_links))

        with open('rescale_resources_html.html') as f:
            page_soup = soup(f, "html.parser")
            search_criteria = re.compile("^(http|https)://")
            results = page_soup.findAll('a', attrs={'href': search_criteria})

            for unedited_link in results:
                link = unedited_link.get('href')
                test_links.append(link)

        assert len(script_links) == len(test_links)
        assert script_links == test_links


unittest.main()
