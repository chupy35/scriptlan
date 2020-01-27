import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import argparse

# initialize the set of links (unique links)
urls = set()

def validate_link(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not validate_link(href):
            # not a valid URL
            continue
        if href in urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            print("External link")
            urls.add(href)
            continue
        print("Internal Link")
        urls.add(href)
    return urls

parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
parser.add_argument("url", help="The URL to extract links from.")
parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
args = parser.parse_args()
url = ""
max_urls = 50

global total_urls_visited
total_urls_visited += 1
links = get_all_website_links(url)
for link in links:
    if total_urls_visited > max_urls:
        break
    crawl(link, max_urls=max_urls)
domain_name = urlparse(url).netloc

print("Number of urls taken")
print(len(urls))
print("URLS:")
print(urls)
