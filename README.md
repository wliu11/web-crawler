# web-crawler

To run this web crawler, download crawler.py, navigate to the directory it has been downloaded to, and execute the terminal command "./crawler.py", followed by the full URL of the webpage you wish to crawl. You may also specify a limit on the number of pages you would like to crawl, by adding "-l" and the number of pages to the end of the terminal command. 


For example, to crawl 5 URLs starting from the Rescale website, we would enter "./crawler.py https://rescale.com -l 5".


This web crawler utilizes a few public libraries offered by Python, described below.

Argument Parser: This allows us to add an argument for the number of pages we would like to parse. Depending on the base URL specified, our web crawler can crawl infinitely, so having a limit on the pages to crawl can help us avoid having to forcibly shut down the crawling process via keyboard interrupt.  

BeautifulSoup: Used to parse the HTML obtained by the Python Request. We combine this with Python's Regex library to locate absolute URLs within each HTML page.

ThreadPoolExecutor: In order to avoid slow loading times for each URL, we parallelize the crawling process on a number of different threads. I decided to use 5 workers for this web crawler. 

In total, this project took me probably around 3.5 continuous hours of work. I did attempt to start the project using urllib to download and parse the HTML files, but found that BeautifulSoup helped avoid the HTTP errors that I often came across. It was a very enjoyable learning process. Please let me know if you have any problems building this crawler. 
