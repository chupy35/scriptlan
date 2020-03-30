"""
TP1 - Scripting Languages - INF8007
Polytechnique Montreal

Students:
Isabella Ferreira
Javier Rosales Tovar
Xiaowei Chen
"""

from urllib.request import urlparse, urljoin
import urllib.error
import sys
from bs4 import BeautifulSoup
import requests
import ssl
import sys, getopt
# # Initialize the set of unique links
# URLS = set()

url_queue = set()

# record visited
url_visited = {}

sys.setrecursionlimit(1500)

# Checks whether url is a valid URL.
def is_valid_link(url):
    parsed = urlparse(url)
    return bool(parsed.netloc), bool(parsed.scheme)


# Returns all URLs that are found in a page
def get_links_from(url, domain_name):

    # distinct links in this url
    links = set()

    # if is dead link, return set()
    if is_dead_link(url):
        return links

    # add user_agent
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)

    # Parsing HTML
    soup = BeautifulSoup(r.text, "html.parser")

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
            print("javascript")
            continue
        # if not http/https, skip
        if not href.startswith("http"):
            print("not http")
            continue
        # if not valid link, skip
        if not is_valid_link(href):
            print("not valid link: " + href)
            continue

        # remove parameters from absolute url
        # to avoid same url, but different parameters
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        # if not in the same domain, skip
        if not parsed_href.netloc == domain_name:
            print("not the same domain name: "+ href)
            continue
        else:
            # add links to set
            links.add(href)

    return links


# Gets all the urls in the page and the urls inside it
def geturls(url, domain_name):
    url_visited[url] = True
    links = get_links_from(url, domain_name)
    for link in links:
        if not link in url_visited.keys():
            print("ok:::::")
            if not is_dead_link(link):
                url_queue.add(link)

    if len(url_queue) == 0:
        print("finished")
        # number of visited links
        print(len(url_visited.keys()))
        return
    else:
        url = url_queue.pop()
        geturls(url, domain_name)


# if is dead link, return True and write to file
def is_dead_link(link):
    try:
        req = urllib.request.Request(link, method="HEAD")
        return False
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("404 error~~~~~!!!!!")
            write_dead_link(link)
        return True


# write dead link
def write_dead_link(link):
    with open("dead_link.txt", "w+") as f:
        f.write(link+"\n")



def main(argv):
    # fix [SSL: CERTIFICATE_VERIFY_FAILED] error
    ssl._create_default_https_context = ssl._create_unverified_context
    #given_url = "https://tech.meituan.com/"
    # given_url = "https://www.uniqlo.com/ca/en/"

    # given_url = "https://www.lebalthazar.com/fr"
    # given_url = "https://www.droussel.ca/fr/"
    # given_url = "http://edpinc.com/"
    try:
        opts, args = getopt.getopt(argv,"h:u:",['help', 'url='])
    except getopt.GetoptError:
      print('scrapper.py -u [url]') 
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('scrapper.py -u [url]')
            sys.exit()
        elif opt in ("-u", "--url"):
            #url = arg
            print(arg)
            given_url = arg
            print("URL: ")
            print(given_url)
            domain_name = urlparse(given_url).netloc
            geturls(given_url, domain_name)


#    filename = os.fsdecode(currentPath)
#    print(filename)
#    if filename and allowed_file(filename):
#        jsonresult = processfile(filename)
#        saveresult(jsonresult, randomString())
#    else:
#        pass


if __name__ == "__main__":
    main(sys.argv[1:])
