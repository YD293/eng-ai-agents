from crawlers.base import BaseSeleniumCrawler
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin
from nosql_db import NoSqlDB
from clearml import Task, Logger

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    parsed = parsed._replace(fragment="")
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    parsed = parsed._replace(path=path)
    return urlunparse(parsed)


class ROS2(BaseSeleniumCrawler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited_links = set()
        self.ignored_suffixes = [".zip", ".pdf", ".gif", ".png", ".jpg", ".jpeg", ".svg"]

    def crawl(self, start_url: str, url_prefix: str, doc_type: str) -> None:
        task = Task.init(project_name="RAG Project", task_name=f"crawl {doc_type} documents")
        logger = Logger.current_logger()
        try:
            self.extract(start_url, url_prefix, doc_type)
        except Exception as e:
            logger.report_text(f"Error during crawling: {e}")
        task.close()

    def extract(self, raw_url: str, url_prefix: str, doc_type: str) -> None:
        url = normalize_url(raw_url)

        if url in self.visited_links or self.is_ignored_url(url):
            return

        self.visited_links.add(url)
        self.visited_links.add(raw_url)
        logger = Logger.current_logger()
        old_doc = self.db.find(url=url)
        if old_doc is not None:
            logger.report_text(f"Document already exists in the database: {url}")
            return

        logger.report_text(f"Starting scrapping ROS2 document: {url}")
        try:
            soup = self.get_soup_from_url(url)
            content = soup.get_text().strip()
            if not content:
                logger.report_text(f"Skip url: {url}")

            document = {
                "title": self.parse_title(soup.find("h1")),
                "subtitle": self.parse_title(soup.find("h2")),
                "content": content,
                "doc_type": doc_type
            }
            
            if document['title'] == '404' and 'Page not found' in document['content']:
                logger.report_text(f"Page not found: {url}")
                return

            success = self.db.insert(url, document)

            logger.report_text(
                f"Scraped and saved Document for [{url}] result: {'success' if success else 'failed'}"
            )

            self.recursively_find_links(raw_url, url_prefix, doc_type, soup)
        except Exception as e:
            logger.report_text(f"Error while processing URL [{url}]: {e}")

    def is_ignored_url(self, url: str) -> bool:
        for suffix in self.ignored_suffixes:
            if url.endswith(suffix):
                return True
        return False

    def recursively_find_links(
        self,
        base_url: str,
        url_prefix: str,
        doc_type: str,
        soup: BeautifulSoup,
    ) -> None:
        logger = Logger.current_logger()
        for link_tag in soup.find_all("a", href=True):
            href = link_tag.get("href")
            full_url = normalize_url(urljoin(base_url, href))
            if full_url.startswith(url_prefix):
                if full_url not in self.visited_links and not self.is_ignored_url(full_url):
                    logger.report_text(f"Found new link to crawl: {full_url}")
                    self.extract(full_url, url_prefix, doc_type)


if __name__ == "__main__":
    db_config = {
        "mongo_uri": "mongodb://localhost:27017/",
        "db_name": "nosql_db",
        "collection_name": "ros2_doc",
    }
    db = NoSqlDB(db_config)
    db.delete_all()
    ros2 = ROS2(db)
    ros2.crawl("https://www.ros.org/blog/why-ros", "https://www.ros.org/blog", "ros2")
    ros2.crawl("https://docs.nav2.org/", "https://docs.nav2.org/", "nav2")
    ros2.crawl("https://moveit.picknik.ai/main/doc/tutorials/getting_started/getting_started.html", "https://moveit.picknik.ai/main/doc/", "moveit")
    ros2.crawl("https://gazebosim.org/docs/latest/getstarted/", "https://gazebosim.org/docs/latest/", "gazebo")
