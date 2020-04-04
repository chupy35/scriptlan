# IDENTIFYING DEAD LINKS ON A WEBSITE

This project is part of the course INF8007 - Langage de script from Polytechnique Montréal.

The goal is to check for the presence of dead links on a website.

Students:
- Isabella Ferreira
- Javier Rosales Tovar
- Xiaowei Chen  

# How to run
Run the command below to identify dead links on a website. 

```
    ./nodeinstaller.sh -g [github repository] -p [port]
```

Obs:
* [github repository] = the link of the github repository. It must contain a node server inside it.
* [port] = the port used to run the server. The default port is 3000.
* All the requirements will be automatically installed in the bash script, but in case you have any problem, please check the "Libraries" section.

# Scrapper

If you would like to run only the scrapper, you can run only the python script as described below.

```
      A Link Scrapper in Python 

 Usage: python scrapper.py [option] [argument] 

 -u, --url = url to crawl 
 -c, --crawl [on/off]  = turn on or off crawl, default=on 
 -f, --file [filepath] = a file path to parse, crawling deactivated in this option  
 -l --lfiles = list of files to parse (each line of the file must be a different file) 
 -w --lwebsite = list of websites to check (each line of the file must be a different website), 
                 crawling deactivated in this option. If localhost, the crawling is deactivated in this option
 -S --stdin [option] for accept stdin input. 
            Available options for --stdin are: "f" to pipe the content of an html file,  
            "p" for a list of files, with "w" a list of websites, example: "cat listofwebsites.txt | python scrapper.py -S w
 
```

Obs:
* When scrapping a website on the localhost, you must specify the port. E.g. python3 scrapper.py -u http://localhost:3000
* When crawling a file (options -l and -f), we might only encounter dead links, since we don't have the domain to validate and the root url to parse and compare.

## Libraries
To run this script, you need to have python3 installed. In addition, you need to install the following libraries:

 - requests
 - BeautifulSoup
 - typing

 If you would like to run a linter on the code, Pylint can be installed. Pylint checks for logical and stylistic errors.

```
     pip3 install pylint
     pylint scrapper.py
```
