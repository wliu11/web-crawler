#!/usr/bin/env python3
import argparse
import math
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue, Empty

import requests
from bs4 import BeautifulSoup as soup


def send_request(url):
    # print("sending new request")
    response = requests.get(url)
    return response


class Crawler:

    def __init__(self, limit, url):
        self.limit = limit
        self.visited_urls = set()
        self.to_visit = Queue()
        self.to_visit.put(url)
        self.pool = ThreadPoolExecutor(max_workers=12)

    def run(self):

        while len(self.visited_urls) < self.limit:
            try:
                # Take the next URL on the ordered list for the crawl
                url = self.to_visit.get()

                if url not in self.visited_urls:

                    # Add this URL to the list of URLs that we have visited so we do not repeat crawling here
                    self.visited_urls.add(url)

                    # # Start the crawl
                    self.pool.submit(self.crawl, url)

                    time.sleep(2)

            except Empty:
                return
            except Exception as e:
                print(e)
                continue

    def crawl(self, url):
        response = send_request(url)
        self.get_urls(response.text, url)

    def get_urls(self, html, url):
        print(url)
        page_soup = soup(html, "html.parser")
        search_criteria = re.compile("http://|https://")
        links = []

        results = page_soup.findAll('a', attrs={'href': search_criteria})
        for unedited_link in results:

            link = unedited_link.get('href')
            print('\t' + link)
            links.append(link)
            if link not in self.visited_urls:
                self.to_visit.put(link)


if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser()

    # Accepts the base URL to crawl
    parser.add_argument('url', nargs='*')

    # Accepts a limit of websites to crawl
    parser.add_argument('-l', '--limit', type=int, default=math.inf)

    args = parser.parse_args()

    # Instantiate the Crawling class with the arguments supplied
    crawler = Crawler(limit=args.limit, url=args.url[0])

    crawler.run()