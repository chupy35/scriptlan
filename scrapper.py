"""
TP1 - Scripting Languages - INF8007
Polytechnique Montréal

Students: 
    Isabella Ferreira
    Javier Rosales Tovar
    Xiaowei Chen  
"""

import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import sys
import re

# Initialize the set of unique links
urls = set()

"""
Checks whether url is a valid URL.
"""
def validate_link(url):
    parsed = urlparse(url)
    return bool(parsed.netloc), bool(parsed.scheme)

"""
Returns all URLs that are found in a page
"""
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
                urls.add(a_tag)
                print(">>>>>>>>> IT MATCHES STRING TEXT: ", a_tag)
                print("Link: ", a_tag)
            else:
                continue
        
        # Join the URL if it's relative LINK (not absolute link)
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
        if href in urls:
            continue        # already in the set - avoid checking duplicated URLs
        if domain_name not in href:
            print("Link: ", href)
            urls.add(href)
            continue
        urls.add(href)
        print("Link: ", href)
    return urls

"""
Gets all the urls in the page and the urls inside it
"""
def geturls(url, domain_name):
    links = get_all_links(url)
    for link in links:
        if domain_name in link:  # Check if we are analyzing URLs from the same website domain
            geturls(link, domain_name)

if __name__ == '__main__':
    url = sys.argv[2]
    domain_name = urlparse(url).netloc
    print(url)
    geturls(url, domain_name)

    print("Number of URLS:")
    print(len(urls))
    print("URLS:")
    print(urls)

    # Save output with found links
    with open(f"{domain_name}_links.txt", "w") as f:
        for internal_link in urls:
            print(internal_link.strip(), file=f)
