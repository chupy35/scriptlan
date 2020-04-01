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
import os
from shutil import copyfile
import ntpath
# # Initialize the set of unique links
# URLS = set()

url_queue = set()

# record visited
url_visited = {}

# Node Server Path
node_path = "node_server/" 

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
def geturls(url, domain_name, crawl):
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
        if crawl != 0:
            url = url_queue.pop()
            geturls(url, domain_name, 1)


# if is dead link, return True and write to file
def is_dead_link(link):
    try:
        req = urllib.request.Request(link, method="HEAD")
        return False
    except urllib.error.HTTPError:
        write_dead_link(link)
        return True


# write dead link
def write_dead_link(link):
    with open("dead_link.txt", "w+") as f:
        f.write(link+"\n")



# - your script accept an argument to tel what url to use (1 point) - ok
# - your script accept argument to check a local file to parse. there cannot be any crawling here since there is no domain. (1 point) - ok
# - your script accept argument to activate/desactivate crawling. (same as doing a search with a depth of 1) (1 point) - ok

# - your script accept data in stdin in the 3 following form (2 point) :
    # - the std:in can receive an HTML page to parse and check. - ok
    # - the std:in can receive a list of website to check - TODO
    # - the std:in can receive a list of file to check - TODO
    # - an argument can be used to choose the form of data expected in std:in. - ok

def main(argv):
    # fix [SSL: CERTIFICATE_VERIFY_FAILED] error
    ssl._create_default_https_context = ssl._create_unverified_context
    #given_url = "https://tech.meituan.com/"
    # given_url = "https://www.uniqlo.com/ca/en/"

    # given_url = "https://www.lebalthazar.com/fr"
    # given_url = "https://www.droussel.ca/fr/"
    # given_url = "http://edpinc.com/"

    help_message = 'Usage: python scrapper.py \n -u, --url = url to crawl, default=localhost \n -c, --crawl [on/off]  = turn on or off crawl, default=on \n -f, --file [filepath] = a file path to parse \n -p --port [port] = specify a port if the server is running in other than default \n -lf --list_files = list of files to check (each line of the file must be a different file) \n -lw --list_website = list of websites to check (each line of the file must be a different website)\n' 
    try:
        opts, args = getopt.getopt(argv,"h:u:c:f:p:lf:lw",['help', 'url=', 'crawl=', 'file=', 'port=', 'list_files=', 'list_website'])
    except getopt.GetoptError:
      print(help_message) 
      sys.exit(2)

    port = 3000
    crawl = 1
    fselect = 0
    given_url = "http://localhost"
    
    for opt, arg in opts:

        if opt == '-h':                         # help message
            print(help_message)
            sys.exit()
       
        elif opt in ("-c", "--crawl"):          # activate/deactivate crawling
            if arg == "on":
                crawl = 1
            if arg == "off":
                crawl = 0
       
        elif opt in ("-p", "--port"):           # port. TODO: Check if it's needed
            if arg.isdigit():
                port = arg
            else:
                print("Please insert a valid port.")
                sys.exit()
       
        elif opt in ("-f", "--file"):             # File path to parse
            fselect = 1
            crawl = 0                             # There is no crawling here, since there is no domain
            print(arg)
            fname = ntpath.basename(arg)
            try:
                dst = node_path + fname
                copyfile(arg, dst)                  # TODO: run script
            except IOError:
                print("Please choose a valid file path")
                sys.exit()
       
        elif opt in ("-u", "--url"):                 # url to crawl, decide whether it's a normal website or localhost
            given_url = arg
            crawl = 1
            print("URL: ")
            print(given_url)
            if "localhost" in given_url:
                domain_name = "http://localhost:"
                given_url = domain_name + str(port)
                geturls(given_url, domain_name, crawl)
            else:
                domain_name = urlparse(given_url).netloc
                geturls(given_url, domain_name, crawl)

        elif opt in ("-lf", "--list_files"):
            print("TODO: List of files")            # TODO

        elif opt in ("-lw", "--list_website"):
            print("TODO: List of websites")         # TODO

        else:
            print("Parameter not recognized: %s !\n" % opt)
            print(help_message)
    
    # if fselect == 1:
    #     domain_name = "http://localhost:"
    #     given_url = domain_name + str(port)
    #     geturls(given_url, domain_name, crawl)


#    filename = os.fsdecode(currentPath)
#    print(filename)
#    if filename and allowed_file(filename):
#    else:
#        pass

if __name__ == "__main__":
    main(sys.argv[1:])