from abc import ABC, abstractmethod

import requests as r
from bs4 import BeautifulSoup
from nosql_db import NoSqlDB

class BaseCrawler(ABC):

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...


class BaseSeleniumCrawler(BaseCrawler, ABC):
    def __init__(self, db: NoSqlDB) -> None:
        self.db = db
    
    def get_soup_from_url(self, url: str) -> BeautifulSoup:
        page_source = r.get(url).text
        if url == 'https://gazebosim.org/docs/latest/getstarted/':
            print(page_source)
        return BeautifulSoup(page_source, "html.parser")
                
    def parse_title(self, title_element) -> str | None:
        if not title_element:
            return None
        # remove headerlink
        headerlink = title_element.find('a', class_='headerlink')
        if headerlink:
            headerlink.decompose()
            
        return title_element.get_text().strip()