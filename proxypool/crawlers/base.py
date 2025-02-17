from retrying import retry
import requests
from loguru import logger


class BaseCrawler(object):
    urls = []
    kwargs = {}

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)
    def fetch(self, url, **kwargs):
        try:
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                return response.text
        except requests.ConnectionError:
            return

    @logger.catch
    def crawl(self):
        """
        crawl main method
        """
        for url in self.urls:
            logger.info(f'fetching {url}')
            html = self.fetch(url, **self.kwargs)
            for proxy in self.parse(html):
                logger.info(f'fetched proxy {proxy.__str__()} from {url}')
                yield proxy

    def parse(self, html) -> str:
        pass
