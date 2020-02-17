import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import sys
import re

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
    Returns all URLs that are found in a page
    """

    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    #print ("soup: ", soup)

    # checking for html tags that contain link and text
    for a_tag in soup.findAll("a") or soup.findAll("area") or soup.findAll("base") or soup.findAll("link") or soup.findAll("b") or soup.findAll("strong") or soup.findAll("i") or soup.findAll("em") or soup.findAll("mark") or soup.findAll("small") or soup.findAll("del") or soup.findAll("ins") or soup.findAll("sub") or soup.findAll("sup") or soup.findAll("p") or soup.findAll("big") or soup.findAll("pre"):

        href = a_tag.attrs.get("href")
        #print("href: ", href)

        if href == "" or href is None:
            # href empty tag. Test if it's in a text
            if url_pattern.match(str(a_tag)):
                urls.add(a_tag)
                print(">>>>>>>>> IT MATCHES STRING TEXT: ", a_tag)
                print("Link: ", a_tag)
            else:
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
            # already in the set - avoid checking duplicated URLs
            continue
        if domain_name not in href:
            print("Link: ", href)
            urls.add(href)
            continue
        urls.add(href)
        print("Link: ", href)
    return urls


def geturls(url):
    """
    Gets all the urls in the page and the urls inside it
    """
    links = get_all_links(url)
    for link in links:
        geturls(link)


if __name__ == '__main__':
    url = sys.argv[2]
    print(url)
    geturls(url)
    domain_name = urlparse(url).netloc

    print("Number of URLS:")
    print(len(urls))
    print("URLS:")
    print(urls)

    with open(f"{domain_name}_links.txt", "w") as f:
        for internal_link in urls:
            print(internal_link.strip(), file=f)
