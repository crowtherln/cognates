#! python3
# persian_english_cognates.py

"""
This program produces a csv of Proto-Indo-European roots that have
    modern descendants in both Persian and English, along with those
    descendants. This program takes about 10 minutes to run.
"""

import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Get URLs for all pages in the Wiktionary category "Persian terms
#   derived from Proto-Indo-European".

# Create a group with the URL for the first page in the category, to 
#   which to add other pages in the category.
persian_category_pages = [
    "https://en.wiktionary.org/wiki/Category:" +
    "Persian_terms_derived_from_Proto-Indo-European"
    ]
# Get the URLs for other pages in the category and add them to
#   persian_category_pages.
response = requests.get(persian_category_pages[0])
data = response.text
soup = BeautifulSoup(data, "lxml")
while soup.find(text="next page") is not None:
    persian_category_page = "https://en.wiktionary.org" + soup.find(
        text="next page").findPrevious("a").get("href")
    persian_category_pages.append(persian_category_page)
    response = requests.get(persian_category_page)
    data = response.text
    soup = BeautifulSoup(data, "lxml")

# Create a list to which to add dictionaries created from the entries on
#   all category pages.
persian_dicts = []

# Create dictionaries from the entries on all category pages.
for page in persian_category_pages:
    response = requests.get(page)
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    # Create a set of <a> tags within <li> tags.
    tags = soup.select("li a")
    # If the <a> tag is for one of the entries, add it to persian_dicts.
    for tag in tags:
        href = tag.get("href")
        title = tag.get("title")
        # Exclude <a> tags with no href.
        if href is not None:
            # Exclude <a> tags with no title.
            if title is not None:
                # Include <a> tags only if the href starts with
                #   "/wiki/".
                if href.startswith("/wiki/"):
                    # Exclude <a> tags that link to category pages.
                    if not href.startswith("/wiki/Category"):
                        # Exclude <a> tags that link to general
                        #   Wiktionary pages.
                        if not href.startswith("/wiki/Wiktionary"):
                            # Exclude <a> tags that link to special
                            #   pages.
                            if not href.startswith("/wiki/Special"):
                                # Create a dictionary out of the <a> tag
                                #   and add it to persian_dicts.
                                persian_dicts.append({
                                    "Persian": title,
                                    "Persian URL": "https://en.wiktionary.org"
                                        + href})

# Visit each page to search for the Proto-Indo-European root.
for dict in persian_dicts:
    response = requests.get(dict["Persian URL"])
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    persian_headers = soup.select("h2 #Persian")
    # Exclude unless there is exactly one <H2> tag with the ID
    #   "Persian".
    if len(persian_headers) != 1:
        # To help the program run faster, remove dictionaries that
        #   cannot be completed.
        persian_dicts.remove(dict)
    else:
        for header in persian_headers:
            # Find the next link to the Wikipedia page for the Proto-
            #   Indo-European language.
            pie_link = header.find_next(
                "a",
                {"href": "https://en.wikipedia.org/wiki/" +
                     "Proto-Indo-European_language"}
                )
        # Exclude unless there is exactly one matching link after the
        #   <h2> tag.
        if len(pie_link) != 1:
            persian_dicts.remove(dict)
        else:
            # Find the <a> tag after the link.
            tag = pie_link.find_next("a")
            href = tag.get("href")
            title = tag.get("title")
            term = tag.text
            if href is None:
                persian_dicts.remove(dict)
            elif title is None:
                persian_dicts.remove(dict)
            elif term is None:
                persian_dicts.remove(dict)
            elif "(page does not exist)" in title:
                persian_dicts.remove(dict)
            else:
                # Add the term and its URL to the dictionary.
                dict["PIE Root"] = term
                dict["PIE URL"] = "https://en.wiktionary.org" + href

# Remove any incomplete dictionaries that remain.
for dict in persian_dicts:
    if "Persian" not in dict:
        persian_dicts.remove(dict)
    elif "Persian URL" not in dict:
        persian_dicts.remove(dict)
    elif "PIE Root" not in dict:
        persian_dicts.remove(dict)
    elif "PIE URL" not in dict:
        persian_dicts.remove(dict)
    
# Get URLs for all pages in the category "English terms derived from
#   Proto-Indo-European".

# Create a group with the URL from the first page in the category, to
#   which to add other pages in the category.
english_category_pages = [
    "https://en.wiktionary.org/wiki/Category:" +
    "English_terms_derived_from_Proto-Indo-European"
    ]

# Get the URLs for other pages in the category and add them to
#   english_category_pages.
response = requests.get(english_category_pages[0])
data = response.text
soup = BeautifulSoup(data, "lxml")
while soup.find(text="next page") is not None:
    english_category_page = "https://en.wiktionary.org" + soup.find(
        text="next page").findPrevious("a").get("href")
    english_category_pages.append(english_category_page)
    response = requests.get(english_category_page)
    data = response.text
    soup = BeautifulSoup(data, "lxml")

# Create a list to which to add dictionaries created from the entries on
#   all category pages.
english_dicts = []

# Create dictionaries from the entries on all category pages.
for page in english_category_pages:
    response = requests.get(page)
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    # Create a set of <a> tags within <li> tags.
    tags = soup.select("li a")
    # If the <a> tag is for one of the entries, add it to english_dicts.
    for tag in tags:
        href = tag.get("href")
        title = tag.get("title")
        # Exclude <a> tags with no href.
        if href is not None:
            # Exclude <a> tags with no title.
            if title is not None:
                # Include <a> tags only if the href starts with
                #   "/wiki/".
                if href.startswith("/wiki/"):
                    # Exclude <a> tags that link to category pages.
                    if not href.startswith("/wiki/Category"):
                        # Exclude <a> tags that link to general
                        #   Wiktionary pages.
                        if not href.startswith("/wiki/Wiktionary"):
                            # Exclude <a> tags that link to special
                            #   pages.
                            if not href.startswith("/wiki/Special"):
                                # Create a dictionary out of the <a> tag
                                #   and add it to persian_dicts.
                                english_dicts.append({
                                    "English": title,
                                    "English URL": "https://en.wiktionary.org"
                                    + href})

# Visit each page to search for the Proto-Indo-European root.
for dict in english_dicts:
    response = requests.get(dict["English URL"])
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    english_headers = soup.select("h2 #English")
    # Exclude unless there is exactly one <H2> tag with the ID
    #   "English".
    if len(english_headers) != 1:
        # To help the program run faster, remove dictionaries that
        #   cannot be completed.
        english_dicts.remove(dict)
    else:
        for header in english_headers:
            # Find the next link to the Wikipedia page for the Proto-
            #   Indo-European language.
            pie_link = header.find_next(
                "a",
                {"href": "https://en.wikipedia.org/wiki/" +
                     "Proto-Indo-European_language"}
                )
        # Exclude unless there is exactly one matching link after the
        #   <h2> tag.
        if len(pie_link) != 1:
            english_dicts.remove(dict)
        else:
            # Find the <a> tag after the link.
            tag = pie_link.find_next("a")
            href = tag.get("href")
            title = tag.get("title")
            term = tag.text
            if href is None:
                english_dicts.remove(dict)
            elif title is None:
                english_dicts.remove(dict)
            elif term is None:
                english_dicts.remove(dict)
            elif "(page does not exist)" in title:
                english_dicts.remove(dict)
            else:
                # Add the term and its URL to the dictionary.
                dict["PIE Root"] = term
                dict["PIE URL"] = "https://en.wiktionary.org" + href

# Remove any incomplete dictionaries that remain.
for dict in english_dicts:
    if "English" not in dict:
        english_dicts.remove(dict)
    elif "English URL" not in dict:
        english_dicts.remove(dict)
    elif "PIE Root" not in dict:
        english_dicts.remove(dict)
    elif "PIE URL" not in dict:
        english_dicts.remove(dict)

# Create a list to which to add Proto-Indo-European terms that have
#   modern descendants in both Persian and English, along with those
#   descendants.
shared_roots = []

for persian_dict in persian_dicts:
    for english_dict in english_dicts:
        try:
            if persian_dict["PIE Root"] == english_dict["PIE Root"]:
                shared_root = {
                    "PIE Root": persian_dict["PIE Root"],
                    "Persian Word": persian_dict["Persian"],
                    "English Word": english_dict["English"],
                    "PIE URL": persian_dict["PIE URL"],
                    "Persian URL": persian_dict["Persian URL"],
                    "English URL": english_dict["English URL"]
                    }
                if shared_root not in shared_roots:
                    shared_roots.append(shared_root)
        except:
            continue

# Change to the directory in which to save the csv.
os.chdir("C:\\Users\\username\\Documents")
# Create a dataframe out of shared_roots.
df = pd.DataFrame(shared_roots)
# Write the dataframe to csv.
df.to_csv("persian_english_cognates.csv", encoding="utf-8-sig")
