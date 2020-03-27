"""
TP1 - Scripting Languages - INF8007
Polytechnique Montreal

Students:
Isabella Ferreira
Javier Rosales Tovar
Xiaowei Chen
"""

from urllib.request import urlparse, urljoin
import sys
import re
from bs4 import BeautifulSoup
import requests

# Initialize the set of unique links
URLS = set()

sys.setrecursionlimit(1500)

# Checks whether url is a valid URL.
def is_valid_link(url):
    parsed = urlparse(url)
    return bool(parsed.netloc), bool(parsed.scheme)


# Returns all URLs that are found in a page
def get_all_links(url):

    # Domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    # Parsing HTML
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    # Checking for html tags that contain link and text
    tags_contain_href = soup.find_all(href=True)

    for tag in tags_contain_href:
        href = tag.attrs.get("href")
        # if href is absolute link
        if href.startswith("http"):
            print("absolute: "+href)
        # if href is relative url, append to be absolute url
        if href.startswith("/"):
            print("relative: " + href)
            href = urljoin(url, href)
            print("absolute: "+href)

        # if message, skip
        if href.find("javascript") != -1:
            continue
        # if not http/https, skip
        if not href.startswith("http"):
            continue
        # if not valid link, skip
        if not is_valid_link(href):
            continue

        # remove parameters from absolute url
        # to avoid same url, but different parameters
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        # already in the set - avoid checking duplicated URLs
        if href in URLS:
            continue
        if domain_name not in href:
            print("Link: ", href)
            URLS.add(href)
            continue
        URLS.add(href)
        print("Link: ", href)
    return URLS


# Gets all the urls in the page and the urls inside it
def geturls(url, domain_name):
    links = get_all_links(url)
    for link in links:  # Check sub-links recursively
        #if domain_name in link:  # Check if we are analyzing URLs from the same website domain
        geturls(link, domain_name)


if __name__ == '__main__':
    # URL = sys.argv[2]
    URL = "https://tech.meituan.com/"
    DOMAIN_NAME = urlparse(URL).netloc
    print(URL)
    geturls(URL, DOMAIN_NAME)

    print("Number of URLS:")
    print(len(URLS))
    print("URLS:")
    print(URLS)

    # Save output with found links
    with open(f"{DOMAIN_NAME}_links.txt", "w") as f:
        for internal_link in URLS:
            print(internal_link.strip(), file=f)
