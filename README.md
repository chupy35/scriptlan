# IDENTIFYING DEAD LINKS ON A WEBSITE

This project is part of the course INF8007 - Langage de script from Polytechnique Montréal.

The goal is to check for the presence of dead links on a website.

Students:
- Isabella Ferreira
- Javier Rosales Tovar
- Xiaowei Chen  

# How to run
Run the command below to identify links on a website. *{url}* refers to the url of the website to be tested.

```
    python3 scrapper.py -u {url}
```

## Libraries
To run this script, you need to have python3 installed. In addition, you need to install the following libraries:

 - requests
 - BeautifulSoup

 If you would like to run a linter on the code, Pylint can be installed. Pylint checks for logical and stylistic errors.

```
     pip3 install pylint
     pylint scrapper.py
```

# Approach

We start by scrapping the main webpage and then each sub-link. For that, we parse the HTML using the BeautifulSoup library and we check for HTML tags related to links (e.g. *a*,*area*, *base*, *link*) and text (e.g. *b*, *strong*, *mark*, *em* etc). Then, we check if there is the attribute *href* in the found tag. If yes, we get the relative link and check whether it's a valid URL. If not, we check if the text has a URL following the pattern:

```
    http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+
```

Every time we find a valid link, we add them to our set of links. Finally, we go over our set of links and print the found links in a txt file named {domain_name}_links.txt, where *{domain_name}* is the domain of the analyzed website.
