"""
TP - Scripting Languages - INF8007
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
from os import path
from typing import Dict, Tuple, Sequence, Set

url_queue = set()

url_visited = {}
dead_links = set()

node_path = "node_server/" 

sys.setrecursionlimit(1500)

# Checks whether url is a valid URL.
def is_valid_link(url: str) -> [bool, bool]:
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc), bool(parsed.scheme)
    except Exception as err:
        print(f'Failed to parse url: {err}')
        return bool(0), bool(0)

# Returns all URLs that are found in a page - no matter if they are dead or not... we check it in the function geturls
def get_links_from(url: str, domain_name: str) -> set:
    print("URL: ", url)

    links = set()       # distinct links in this url

    # Requesting website
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}  
        r = requests.get(url, headers=headers)
        r.raise_for_status()                    # If the response was successful, no Exception will be raised
    except Exception as err:
        print(f'Error occurred during URL Request: {err}')
    else:
        print('URL request == Success! ', url)

    # Parsing HTML
    try: 
        soup = BeautifulSoup(r.text, "html.parser")
        tags_contain_href = soup.find_all(href=True)             # Checking for html tags that contain link and text
    
        if len(tags_contain_href) > 0:
            for tag in tags_contain_href:
                href = tag.attrs.get("href")

                # if href is absolute link
                if href.startswith("http") or href.startswith("https"):
                    href = href
                else:
                    href = urljoin(url, href)

                # if message, skip
                # if href.find("javascript") != -1:
                #     print("javascript")
                #     continue
                # # if not http/https, skip
                # if not (href.startswith("http") or href.startswith("https")):
                #     print("not http: ", href)
                #     continue
                # # if not valid link, skip
                # if not is_valid_link(href):
                #     print("not valid link: " + href)
                #     continue

                # remove parameters from absolute url
                # to avoid same url, but different parameters
                parsed_href = urlparse(href)
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

                # if not in the same domain, skip
                if not parsed_href.netloc == domain_name:
                    print("Not the same domain name: "+ href)
                    continue
                else:       # same domain, valid link
                    # add links to set
                    if is_valid_link(href):
                        links.add(href)
        else:
            print("No tags were identified when parsing the url: ", url)

    except Exception as err:
        print ("Error occurred during BeautifulSoup parsing:", err)
    

    return links

# Gets all the urls in the page and the urls inside it
def geturls(url: str, domain_name: str, crawl: bool) -> None:
    print("\n\nGetting URLS...\n\n")
    url_visited[url] = True
    
    print("url: ", url)
    print("domain name: ", domain_name)
    print("\n\n")

    output_file : str = "dead_links/dead_links_" + domain_name + ".txt"

    if not path.exists("dead_links"):
        os.mkdir("dead_links")
    
    with open(output_file, "a+") as f:
        if not is_dead_link(url):
            links = get_links_from(url, domain_name)
            print("\nlinks: ", links)
            print("\n")
            if len(links) > 0:
                for link in links:
                    print("\n\n")
                    print("TESTING LINK: ", link)
                    if link in url_visited:
                        print("IS URL VISITED: %s ||| %s " % (url_visited[link], link))
                    if not link in url_visited.keys():
                        print("ok::::: URL NOT VISITED YET: ", link)
                        if not is_dead_link(link):
                            print("NOT A DEAD LINK")
                            url_queue.add(link)             # Has all valid links
                        else: 
                            print("Dead link: ", link)
                            if link not in dead_links:
                                dead_links.add(link)
                                f.write("%s\n" % (link))
            else:
                print("No links were found in the website: ", url)
        else:
            if url not in dead_links:
                dead_links.add(url)
                f.write("%s\n" % (url))
                print("Dead link: ", url)
        
    # Checking sublinks of the links found in the main page
    if crawl == 1:
        url = url_queue.pop()
        if len(url_queue) == 0:
            print("\n\n******************* Finished crawling all links and sublinks *******************")
            print("Number of visited links: ", len(url_visited.keys()))                  # number of visited links
            print("Number of dead links: ", len(dead_links))                             # number of dead links
        else:
            geturls(url, domain_name, crawl)

  # if is dead link, return True and write to file

def is_dead_link(link: str) -> bool:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}  
        r = requests.get(link, headers=headers)
        r.raise_for_status()                    # If the response was successful, no Exception will be raised
        return False
    except Exception as err:
        print(f'Error occurred during URL Request: {err}')
        return True
    else:
        print('URL request == Success!')
        return False

# Fucntion to process the stdin, return...
def process_stdin(stdin):
    buffer = ""
   # for li in stdin:
   #     buffer = buffer + li
    for chunk in iter(lambda: fp.read(stdin), ''):
        buffer = buffer + chunk

    print(buffer)

def process_lwebsites(input_file, given_url, crawl):
    print("Input file: ", input_file)
    with open(input_file, "r") as f:
        info = f.readlines()
        for url in info:
            domain_name = urlparse(url).netloc
            print("Normal website to test: ", domain_name)
            geturls(given_url, domain_name, crawl)

def printandexit(message):
    print(message)
    sys.exit(2)


# - your script accept an argument to tel what url to use (1 point) - ok
# - your script accept argument to check a local file to parse. there cannot be any crawling here since there is no domain. (1 point) - ok
# - your script accept argument to activate/desactivate crawling. (same as doing a search with a depth of 1) (1 point) - ok
# - your script accept data in stdin in the 3 following form (2 point) :
    # - the std:in can receive an HTML page to parse and check. - ok
    # - the std:in can receive a list of website to check - TODO
    # - the std:in can receive a list of file to check - TODO
    # - an argument can be used to choose the form of data expected in std:in. - ok
def main(argv):
    ssl._create_default_https_context = ssl._create_unverified_context

    help_message = 'Usage: python scrapper.py \n -u, --url = url to crawl \n -c, --crawl [on/off]  = turn on or off crawl, default=on \n -f, --file [filepath] = a file path to parse, crawling deactivated in this option  \n -l --lfiles = list of files to check (each line of the file must be a different file) \n -w --lwebsite = list of websites to check (each line of the file must be a different website), crawl deactivated in this option\n'
    badargument_message_url = "The only option to be use with -u, --url is --crawl, -c"
    badargument_message_lwebsite = "The only option  -l, --lwebsite is provide a listofwebsites, shouldnt be used with other parameter"

    badargument_message_stdin = "-S cannot be used with file "
    try:
        opts, args = getopt.getopt(argv,"h:u:c:f:w:S:l:",['help', 'url=', 'crawl=', 'file=', 'lfiles=', 'stdin', 'lwebsite='])
    except getopt.GetoptError:
        printandexit(help_message)

    port : int = 3000
    crawl : bool = 1
    lwebsite : bool = 0
    urlselected : bool = 0
    fselect : bool = 0
    stdin : bool = 0
    given_url : str = "http://localhost"
    for opt, arg in opts:

        if opt == '-h':                         # help message
            printandexit(help_message)
       
        elif opt in ("-c", "--crawl"):          # activate/deactivate crawling
            if arg == "on":
                crawl = 1
            if arg == "off":
                crawl = 0
        elif opt in ("-f", "--file"):             # File path to parse
            fselect = 1
            crawl = 0                             # There is no crawling here, since there is no domain
            print(arg)
            fname = ntpath.basename(arg)
            try:
                dst = node_path + "index.html"
                copyfile(arg, dst)              #DONE but we have to test with the node server
            except IOError:
                print("Please choose a valid file path")
                sys.exit()
        elif opt in ("-u", "--url"):                 # url to crawl, decide whether it's a normal website or localhost
            urlselected = 1
            given_url = arg
            print("URL to crawl: ", given_url)
            #if "localhost" in given_url:
                # domain_name = "http://localhost:"
                # given_url = domain_name + str(port)
                # print("Give url: ", given_url)
                # geturls(given_url, domain_name, crawl)
            #else:
            domain_name = urlparse(given_url).netloc
            print("Normal website to test: ", domain_name)
        elif opt in ("-S", "--Stdin"):
            print("SIMIONAAAAAAA!!!!!!")
            stdin = 1
            #geturls(given_url, domain_name, crawl)
        elif opt in ("-w", "--lwebsite"):
            print("TODO: List of websites")         # TODO
            print("arg: ", arg)
            input_file = arg
            lwebsite = 1
#            print("Input file: ", input_file)
#            with open(input_file, "r") as f:
#                info = f.readlines()
#                for url in info:
#                    domain_name = urlparse(url).netloc
#                    print("Normal website to test: ", domain_name)
#                    geturls(given_url, domain_name, crawl)
        elif opt in ("-l", "--lfiles"):
            print("TODO: List of files")            # TODO
        else:
            print("Parameter not recognized: %s !\n" % opt)
            print(help_message)

    if (urlselected == 1 and fselect == 1) and (urlselected == 1 and lwebsite == 1) and (urlselected == 1 and stdin == 1):
        printandexit(badargument_message_url)

    if (lwebsite == 1 and stdin == 1) and (lwebsite == 1 and fselect == 1):
        printandexit(badargument_message_lwebsite)


    if lwebsite == 1:
        crawl = 0
        process_lwebsites(input_file, given_url, crawl)
    if fselect == 1:
        domain_name = "http://localhost:"
        given_url = domain_name + str(port)
        crawl = 0
    if stdin == 1:
        domain_name = "http://localhost:"
        given_url = domain_name + str(port)
        crawl = 0
        process_stdin(sys.stdin)
    if urlselected == 1:
        geturls(given_url, domain_name, crawl)
#    filename = os.fsdecode(currentPath)
#    print(filename)
#    if filename and allowed_file(filename):
#    else:
#        pass

if __name__ == "__main__":
    main(sys.argv[1:])
