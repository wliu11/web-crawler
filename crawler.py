#!/usr/bin/env python3
# __author__ Wendy Liu
import argparse
import math
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue, Empty

import requests
from bs4 import BeautifulSoup as soup


def send_request(url):
    response = requests.get(url)
    return response


class Crawler:

    def __init__(self, limit, url):
        self.limit = limit

        # We use a set to record each URL we visit only once, and searching a set is fast
        self.visited_urls = set()

        # We use a queue because we want to maintain the ordering of URLs, and this is best for multithreaded processes
        self.to_visit = Queue()

        # Add our base URL
        self.to_visit.put(url)

        # Initialize the ThreadPoolExecutor with a few workers
        self.pool = ThreadPoolExecutor(max_workers=5)

    # Keep crawling until we either crawled all the URLs stemming from our base URL, or we reached our limit
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

                    # Suspend the thread temporarily
                    time.sleep(2)

            except Empty:
                return
            except Exception as e:
                print(e)
                continue

    # Send the request to a URL, download the response, and parse the HTML for links
    def crawl(self, url):
        response = send_request(url)

        # Return is only for testing, since the spec asks us to print to console
        return self.get_urls(response.text, url)

    # Scrape the HTML file for URLs
    def get_urls(self, html, url):
        # Print the base URL without indent
        print(url)
        page_soup = soup(html, "html.parser")

        # Filter only links that begin with 'http' or 'https', ignoring relative paths
        search_criteria = re.compile("^(http|https)://")

        results = page_soup.findAll('a', attrs={'href': search_criteria})

        # Only for testing
        links = []

        for unedited_link in results:
            link = unedited_link.get('href')

            # Print the children URLs with a single indent
            print('\t' + link)

            links.append(link)

            if link not in self.visited_urls:
                
                # If this link has not yet been visited, add to the list of links we need to parse
                self.to_visit.put(link)

        return links


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

    # Run the web crawler
    crawler.run()
