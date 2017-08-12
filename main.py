#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import csv
from general import *

start_url_list = ["https://sacramento.craigslist.org/search/cpg?query=web%20developer&sort=date&is_paid=yes&searchNearby=2",
                  "https://sacramento.craigslist.org/search/cpg?query=web%20designer&sort=date&is_paid=yes&searchNearby=2",
                  "https://sacramento.craigslist.org/search/cpg?query=web%20design&sort=date&is_paid=yes&searchNearby=2",
                  "https://sacramento.craigslist.org/search/cpg?query=web%20professional&sort=date&is_paid=yes&searchNearby=2"]
base_url = "https://sacramento.craigslist.org"
keywords = ["web developer", "web designer", "web design", "web professional"]

def request_html(url_list):
    """
    Requests the html of each url in list and returns the html in a list named
    'soup' which can be passed to a parsing function.
    """
    url_list = list_to_set(url_list)
    url_list = set_to_list(url_list)
    global base_url
    soup = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/53.0.1345.76 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,image/webp,*/*;q=0.8"}

    for link in url_list:
        try:
            url = link
            print("Downloading page {}...".format(url))
            req = requests.get(url, headers=headers)
            soup.append(BeautifulSoup(req.text, 'lxml'))
        except requests.exceptions.MissingSchema:
            url = base_url + link
            print("Downloading page {}...".format(url))
            req = requests.get(url, headers=headers)
            soup.append(BeautifulSoup(req.text, "lxml"))
    return soup


def parse_titles(soup):
    """
    Takes a list of html codes from Craigslist category search pages and returns
    a list of links to individual post pages as 'page_links'.
    """
    global keywords
    page_links = []
    print(len(soup))
    for elem in soup:
        page_content = []
        title_links = elem.find_all("a", class_="result-title hdrlnk")
        link_href = (link.get("href") for link in title_links)
        page_links.append(link_href)
    return page_links


def parse_page(soup):
    """
    Takes a list of html codes from Craigslist post pages and returns
    a list containing the title, post body, and compensation as 'page_info'.
    """
    page_info = []
    for elem in soup:
        page_content = []
        page_content.append(elem.find("span", id="titletextonly").text.strip())
        # save the body content for further data normalization
        content = elem.find("section", id="postingbody")
        content.div.decompose()
        page_content.append(content.text.strip())
        page_content.append(elem.find("p", class_="attrgroup").b.extract().text.strip())
        page_info.append(page_content)
    return page_info


def gather_posts():
    """
    Gathers info from individual post pages.
    """
    return parse_page(request_html(parse_titles(request_html(start_url_list))))


print(request_html(start_url_list))
# TODO save list to csv

# add data into existing file
def append_to_file(path, data):
     with open(path, "a") as file:
         file.write(data + "\n")


if __name__ == "__main__":
    # category_html = request_html(start_url_list)
    # titles = parse_titles(category_html)
    # pages_html = request_html(titles)
    # page_text = parse_page(pages_html)
    print(gather_posts())