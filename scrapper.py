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

node_path = "html/" 

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
def get_links_from(url: str, domain_name: str, is_file: bool) -> set:
    print("URL: ", url)

    links = set()       # distinct links in this url

    if is_file == 0:                # if it's a url, I request the URL and parse the result of the results
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

                    parsed_href = urlparse(href)

                    # if not in the same domain, skip
                    #print("parsed_href.netloc: ", parsed_href.netloc)
                    #print("domain name: ", domain_name)
                    if not parsed_href.netloc == domain_name:
                        print("Not the same domain name: "+ href)
                        continue
                    else:       # same domain, valid link
                        if is_valid_link(url=href):
                            links.add(href)
            else:
                print("No tags were identified when parsing the url: ", url)

        except Exception as err:
            print ("Error occurred during BeautifulSoup parsing:", err)
   
    elif is_file == 1:           # it's a file
        print("IT'S A FILE - GETTING URLS")
        with open(url, "r") as html_file:
            contents = html_file.read()

            try:
                soup = BeautifulSoup(contents, 'html.parser')
                tags_contain_href = soup.find_all(href=True)             # Checking for html tags that contain link and text
        
                if len(tags_contain_href) > 0:
                    for tag in tags_contain_href:
                        href = tag.attrs.get("href")

                        # if href is absolute link
                        if href.startswith("http") or href.startswith("https"):
                            href = href
                        else:
                            href = urljoin(url, href)

                            parsed_href = urlparse(href)

                        # if not in the same domain, skip
                        if not parsed_href.netloc == domain_name:
                            print("Not the same domain name: "+ href)
                            continue
                        else:       # same domain, valid link
                            if is_valid_link(url=href):
                                links.add(href)
                else:
                    print("No tags were identified when parsing the url: ", url)

            except Exception as err:
                print ("Error occurred during BeautifulSoup parsing:", err)

        
    return links

# Gets all the urls in the page and the urls inside it
def geturls(url: str, domain_name: str, crawl: bool, is_file: bool) -> None:
    print("\n\nGetting URLS...\n\n")
    url_visited[url] = True
    
    print("url: ", url)
    print("domain name: ", domain_name)
    print("crawl: ", crawl)
    print("\n\n")

    output_file : str = "dead_links_" + domain_name + ".txt"

    if not path.exists("dead_links"):
        os.mkdir("dead_links")

    output_file = "dead_links/"+output_file

    if "localhost" in domain_name:
        # doing this to match same domain in get_links_from function
        domain_name = domain_name.replace("http://","").replace("https://","").replace("/","")
        #output_file = "dead_links/"+"dead_links_"+domain_name.replace("/", "_")
        output_file = "dead_links/"+"dead_links_"+domain_name
        print("output_file: ", output_file)
    
    with open(output_file, "a+") as f:

        if (is_file == 0) and (not is_dead_link(link=url)):             # it's a url and not a dead link
            links = get_links_from(url=url, domain_name=domain_name, is_file=is_file)
        elif (is_file == 0) and (is_dead_link(link=url)):               # it's a url and deadlink, add it to the set of dead link and return
            if url not in dead_links:
                dead_links.add(url)
                f.write("%s\n" % (url))
                print("Dead link: ", url)
                return
        elif (is_file == 1):            # we are parsing a file
            links = get_links_from(url=url, domain_name=domain_name, is_file=is_file)

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
                if not is_dead_link(link=link):
                    print("NOT A DEAD LINK")
                    url_queue.add(link)             # Has all valid links
                else: 
                    print("Dead link: ", link)
                    if link not in dead_links:
                        dead_links.add(link)
                        f.write("%s\n" % (link))
        else:
            print("No links were found in the website: ", url)

        
        # Checking sublinks of the links found in the main page
        if crawl == 1:
            try: 
                url = url_queue.pop()
                if len(url_queue) == 0:
                    print("\n\n******************* Finished crawling all links and sublinks *******************")
                    print("Number of visited links: ", len(url_visited.keys()))                  # number of visited links
                    print("Number of dead links: ", len(dead_links))                             # number of dead links
                else:
                    geturls(url=url, domain_name=domain_name, crawl=crawl, is_file=0)           # is_file will always be 0 here because we cannot crawl file
            except Exception as err:
                print ("Error occurred during popping queue of websites:", err)
        else:
            print("\n\n******************* Finished crawling all links and sublinks *******************")
            print("Number of visited links: ", len(url_visited.keys()))                  # number of visited links
            print("Number of dead links: ", len(dead_links))                             # number of dead links

# if is dead link, return True
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

# Function to process the stdin, return...
def process_stdin(stdin, option):
    given_url : str = "http://localhost"
    buffer = ""
    file_counter = 0
    documents = []
    for li in stdin:
        if option == "lsites":
            print("TODO list of sites")
        if option == "stdin_file":
            # if it fins an end of line
            if li is None:
                documents.append(buffer)
            buffer = ""
            buffer = buffer + li
    documents.append(buffer)
    for doc in documents:
        print(doc)
        with open('html/index.html', 'w') as filehandle:
            filehandle.write(buffer)
        domain_name = urlparse(given_url).netloc
        geturls(url=given_url, domain_name=domain_name, crawl=1, is_file=0)     # TODO: @Javier, please verify if the value of is_file is correct here

# Function that receive a list of websites and process them.
def process_lwebsites(input_file, given_url, crawl):
    print("Input file: ", input_file)
    print("Given url: ", given_url)
    print("Crawl:  ", crawl)

    with open(input_file, "r") as f:
        info = f.readlines()
        for url in info:
            print("Processing url: ", url)
            domain_name = urlparse(url).netloc
            if "localhost" in url:
                crawl = 0
                geturls(url=given_url, domain_name=domain_name, crawl=crawl, is_file=0)
            else:
                geturls(url=url, domain_name=domain_name, crawl=crawl, is_file=0)

#Function that prints a message and exit of the application
def printandexit(message):
    print(message)
    sys.exit(2)

def main(argv):
    ssl._create_default_https_context = ssl._create_unverified_context

    help_message = 'Usage: python scrapper.py \n -u, --url = url to crawl \n -c, --crawl [on/off]  = turn on or off crawl, default=on \n -f, --file [filepath] = a file path to parse, crawling deactivated in this option  \n -l --lfiles = list of files to check (each line of the file must be a different file) \n -w --lwebsite = list of websites to check (each line of the file must be a different website), crawl deactivated in this option\n'
    badargument_message_url = "The only option to be use with -u, --url is --crawl, -c"
    badargument_message_lwebsite = "The only option  -l, --lwebsite is provide a list of websites, shouldnt be used with other parameter"

    try:
        opts, args = getopt.getopt(argv,"h:u:c:f:w:Sl:",['help', 'url=', 'crawl=', 'file=', 'lfiles=', 'stdin=', 'lwebsite='])
    except getopt.GetoptError:
        printandexit(message=help_message)

    port : int = 3000
    crawl : bool = 1
    lwebsite : bool = 0
    urlselected : bool = 0
    fselect : bool = 0
    stdin : bool = 0
    given_url : str = "http://localhost"
    
    for opt, arg in opts:

        if opt == '-h':                         # help message
            printandexit(message=help_message)
       
        elif opt in ("-c", "--crawl"):          # activate/deactivate crawling
            if arg == "on":
                crawl = 1
            if arg == "off":
                crawl = 0
    
        elif opt in ("-f", "--file"):             # File path to parse - # TODO: Test: -f name of file
            print("It's a file!")
            fselect = 1
            crawl = 0                             # There is no crawling here, since there is no domain
            file_path = arg
            print("File path: ", file_path)
            fname = ntpath.basename(arg)
            print("fname: ", fname)
            try:
                dst = node_path + "index.html"
                print("dest: ", dst)
                copyfile(arg, dst)                      # TODO @Javier: Why do we need to do that? I'm using the path that the user passed on the command line
                geturls(url=file_path, domain_name="", crawl=crawl, is_file=1)  
            except IOError:
                print("Please choose a valid file path")
                sys.exit()
    
        elif opt in ("-u", "--url"):                 # url to crawl, decide whether it's a normal website or localhost
            urlselected = 1
            given_url = arg
            domain_name = urlparse(given_url).netloc
       
        elif opt in ("-S", "--Stdin"):
            print("")
            stdin = 1
       
        elif opt in ("-w", "--lwebsite"):
            input_file = arg
            lwebsite = 1

        elif opt in ("-l", "--lfiles"):
            print("TODO: List of files")                    # TODO Function. Do it similar to the list of websites   
       
        else:
            print("Parameter not recognized: %s !\n" % opt)
            print(help_message)

    if (urlselected == 1 and fselect == 1) and (urlselected == 1 and lwebsite == 1) and (urlselected == 1 and stdin == 1):
        printandexit(message=badargument_message_url)

    if (lwebsite == 1 and stdin == 1) and (lwebsite == 1 and fselect == 1):
        printandexit(message=badargument_message_lwebsite)

    if lwebsite == 1:
        crawl = 0
        process_lwebsites(input_file=input_file, given_url=given_url, crawl=crawl)          # TODO Confirm: It's not always localhost, can be a list of normal websites. So, we cannot decide crawl and given url here. Treating that inside the function. File with list of normal websites: NOT OK / File with 1 localhost : TODO
    
    if fselect == 1:                                            
        crawl = 0                                              
    
    if stdin == 1:
        domain_name = "http://localhost:"
        given_url = domain_name + str(port)
        crawl = 0
        option= "stdin_file"
        process_stdin(stdin=sys.stdin, option=option)
    
    if urlselected == 1:              
        if "localhost" not in given_url:
            geturls(url=given_url, domain_name=domain_name, crawl=crawl, is_file=0)          
        else: # For localhost, it needs to pass the port. Eg: time python3 scrapper.py -u http://localhost:3000
            crawl = 0 
            geturls(url=given_url, domain_name=given_url, crawl=crawl, is_file=0)

if __name__ == "__main__":
    main(sys.argv[1:])