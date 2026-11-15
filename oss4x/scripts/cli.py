"""
CLI module
"""

from datetime import timedelta

from oss4x.scripts.scripts import (
    add_projects_to_listing,
    data_publication,
    discover_projects,
    format_all_files,
    repository_scraping,
    update_listing_of_listings,
)
from oss4x.scripts.src import utils
from oss4x.src.log import log_info


def add():
    """Adds a resource to the index

    :param url: URL to add to the index
    """
    urls_to_add = []
    x = "?"
    while x != "":
        x = input("Enter URL to be added (ENTER to stop adding): ")
        # Removing whitespaces
        x = x.strip()
        if len(x) > 0:
            urls_to_add.append(x)
    log_info(f"Adding {urls_to_add}")
    add_projects_to_listing(urls_to_add)


def format():
    """Formats I/O files"""
    format_all_files()


def discover():
    """Generates an index"""
    ttl_cache = timedelta(days=7)
    update_listing_of_listings()
    discover_projects(cache_lifetime=ttl_cache)
    format_all_files()


def publish():
    """Publishes the data to an online FTP"""
    data_publication.publish_to_ftp()


def generate_listing():
    """Generates the updated listing"""
    repository_scraping.scrape_all()


def download_data():
    """Downloads the latest listing"""
    utils.download_data()
