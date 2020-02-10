import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import argparse

# initialize the set of links (unique links)
urls = set()
count_urls = 0

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
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a") or soup.findAll("area") or soup.findAll("base") or soup.findAll("link"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if "javascript" in str(href):
            continue
        if  "http" not in str(href[0:4]):
            continue
        if not validate_link(href):
            # not a valid URL
            continue
        if href in urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            print("Link: ")
            print(href)
            urls.add(href)
            continue
        print("Link: ")
        urls.add(href)
        print(href)
    return urls


def geturls(url):
    global count_urls
    count_urls += 1
    links = get_all_links(url)
    for link in links:
        if count_urls > max_urls:
            break
        geturls(link)

url = "https://www.unitec.mx/"
max_urls = 50

geturls(url)
domain_name = urlparse(url).netloc

print("Number of urls taken")
print(len(urls))
print("URLS:")
print(urls)

with open(f"{domain_name}_links.txt", "w") as f:
    for internal_link in urls:
        print(internal_link.strip(), file=f)
