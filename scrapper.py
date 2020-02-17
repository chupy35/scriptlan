"""
TP1 - Scripting Languages - INF8007
Polytechnique Montréal

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

sys.setrecursionlimit(3000)

# Initialize the set of unique links
URLS = set()


# Checks whether url is a valid URL.
def validate_link(url):
    parsed = urlparse(url)
    return bool(parsed.netloc), bool(parsed.scheme)


# Returns all URLs that are found in a page
def get_all_links(url):

    # Pattern to match URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # Domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    # Parsing HTML
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    # Checking for html tags that contain link and text
    for a_tag in soup.findAll("a") or soup.findAll("area") or soup.findAll("base") or soup.findAll("link") or soup.findAll("b") or soup.findAll("strong") or soup.findAll("i") or soup.findAll("em") or soup.findAll("mark") or soup.findAll("small") or soup.findAll("del") or soup.findAll("ins") or soup.findAll("sub") or soup.findAll("sup") or soup.findAll("p") or soup.findAll("big") or soup.findAll("pre"):

        href = a_tag.attrs.get("href")

        if href == "" or href is None:  # href empty tag. Test if it's in a text
            if url_pattern.match(str(a_tag)):
                URLS.add(a_tag)
                print(">>>>>>>>> IT MATCHES STRING TEXT: ", a_tag)
                print("Link: ", a_tag)
            else:
                continue
        # Join the URL if it's relative link (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        # Remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if "javascript" in str(href):
            continue
        if  "http" not in str(href[0:4]):
            continue
        if not validate_link(href):
            continue            # not a valid URL
        if href in URLS:
            continue        # already in the set - avoid checking duplicated URLs
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
        if domain_name in link:  # Check if we are analyzing URLs from the same website domain
            geturls(link, domain_name)

if __name__ == '__main__':
    URL = sys.argv[2]
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
