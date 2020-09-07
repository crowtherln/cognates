#! python3
# cognate_finder.py

"""
This program finds cognates between two languages as documented on
    Wiktionary. It produces a csv of common ancestor terms alongside
    terms in the descendant languages. Depending on how well-documented
    the chosen languages are on English Wiktionary, it may take anywhere
    from 1–30 minutes to run. Note that the program will open a few URLs
    in your browser."""

import time
start_time = time.time()

import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import webbrowser

# Define functions.
"""
This function finds URLs for all "next pages" in a Wiktionary category
    index. As input, it takes the name of a one-item list. The list item
    is the URL for the first page in the category index. The list needs
    to be created before the function is called."""
def get_wikt_cat_pages(list):
    response = requests.get(list[0])
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    while soup.find(text="next page") is not None:
        try:
            url = wiktionary + soup.find(text="next page").findPrevious(
                "a").get("href")
            list.append(url)
            response = requests.get(url)
            data = response.text
            soup = BeautifulSoup(data, "lxml")
        except:
            break

"""
This function scrapes entries from pages in a Wiktionary category index
    for terms in one language that are derived from an ancestor
    language. Before this function is called, there needs to be a
    non-empty list of pages in the Wiktionary category index, such as
    can be created by running the get_wikt_cat_pages() function, and an
    empty list to which to add the entries. As input, the function takes
    the name of the descendant language, the name of the list of pages
    in the Wiktionary category index, and the name of the empty list to
    which to add the entries."""
def get_wikt_entries(language,
                     wikt_pages_list,
                     wikt_entries_list):
    for page in wikt_pages_list:
        response = requests.get(page)
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        # Create a set of <a> tags within <li tags>/
        tags = soup.select("li a")
        # If the <a> tag is for one of the entries, add it to the list.
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
                                    # Create a dictionary out of the <a>
                                    #   tag and add it to the list.
                                    wikt_entries_list.append({
                                        language: title,
                                        language + " URL": "https://en." +
                                            "wiktionary.org" + href})

"""
This function scrapes Wiktionary entry pages to find words' ancestors in
    the specified ancestor language. Before this function is called, the
    function get_wikt_entries() needs to be called to produce a list of
    dictionaries for Wiktionary entries, and the variable "ancestor_url"
    needs to be assigned to the Wikipedia page for the ancestor
    language. As input, this function takes the name of the descendant
    language, the name of the ancestor language, and the name of the
    list of dictionaries."""
def get_ancestor_roots(language,
                       ancestor,
                       wikt_entries_list):
    for dict in wikt_entries_list:
        response = requests.get(dict[language + " URL"])
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        headers = soup.select("h2 #" + language)
        # Exclude unless there is exactly one <h2> tag for the language.
        if len(headers) != 1:
            # To help the program run faster, remove dictionaries that
            #   cannot be completed.
            wikt_entries_list.remove(dict)
        else:
            try:
                ancestor_url_instance = headers[0].find_next(
                    "a", {"href": ancestor_url})
                tag = ancestor_url_instance.find_next("a")
                href = tag.get("href")
                title = tag.get("title")
                term = tag.text
                if href is None:
                    wikt_entries_list.remove(dict)
                elif title is None:
                    wikt_entries_list.remove(dict)
                elif term is None:
                    wikt_entries_list.remove(dict)
                elif "(page does not exist)" in title:
                    wikt_entries_list.remove(dict)
                else:
                    dict[ancestor + " Root"] = term
                    dict[ancestor + " URL"] = "https://en.wiktionary.org" + href
            except:
                continue
    # Remove any incomplete dictionaries that remain.
    for dict in wikt_entries_list:
        if language not in dict:
            wikt_entries_list.remove(dict)
        elif language + " URL" not in dict:
            wikt_entries_list.remove(dict)
        elif ancestor + " Root" not in dict:
            wikt_entries_list.remove(dict)
        elif ancestor + " URL" not in dict:
            wikt_entries_list.remove(dict)

"""
This function takes a list of dictionaries of Wiktionary terms and their
    ancestors for each of two different languages. Before this function
    is called, the function get_ancestor_roots() needs to be called for
    both languages, and there needs to be an empty list to which to add
    dictionaries for terms in the two languages that share a root. As
    input, this function takes the name of the first language, the name
    of the second language, the name of the ancestor language, the name
    of the list of dictionaries for terms in the first language created
    by running get_ancestor_roots(), the name of the list of
    dictionaries for terms in the second language created by running
    get_ancestor_roots(), and the name of the list to which to add
    dictionaries for terms in the two languages that share a root."""
def find_shared_roots(lang_1,
                      lang_2,
                      ancestor,
                      lang_1_dicts,
                      lang_2_dicts,
                      shared_roots_list):
    for dict_1 in lang_1_dicts:
        for dict_2 in lang_2_dicts:
            try:
                if dict_1[ancestor + " Root"] == dict_2[ancestor + " Root"]:
                    shared_root = {
                        ancestor + " Root": dict_1[ancestor + " Root"],
                        lang_1 + " Word": dict_1[lang_1],
                        lang_2 + " Word": dict_2[lang_2],
                        ancestor + " URL": dict_1[ancestor + " URL"],
                        lang_1 + " URL": dict_1[lang_1 + " URL"],
                        lang_2 + " URL": dict_2[lang_2 + " URL"]}
                    if shared_root not in shared_roots_list:
                        shared_roots_list.append(shared_root)
            except:
                continue

"""
This function prints the time elapsed since the beginning of the
    program. Before this function is called, the variable "elapsed_time"
    needs to be assigned."""
def elapsed_time():
    elapsed_time = round(time.time() - start_time)
    if elapsed_time < 60:
        print("Elapsed time: " + str(elapsed_time) + " seconds")
    else:
        print("Elapsed time: " + str(round(elapsed_time/60)) + " minutes")

# Create variables for the start of Wiktionary and Wikipedia URLs as
#   shortcuts.
wiktionary = "https://en.wiktionary.org"
wikipedia = "https://en.wikipedia.org"

# Get the first language.
print("""
Greetings. This program scrapes Wiktionary to find cognates between two
    languages. What is the first language you would like to compare?""")

lang_1 = input()
lang_1_url_component = lang_1.replace(" ", "_")

# Get the second language.
print("""
Thank you. What is the second language you would like to compare?""")

lang_2 = input()
lang_2_url_component = lang_2.replace(" ", "_")

# Get the ancestor language and guess its Wikipedia URL.
print("""
Thank you. What is the most recent common ancestor of those languages?""")

ancestor = input()
ancestor_url_component = ancestor.replace(" ", "_") + "_language"
ancestor_url = f"{wikipedia}/wiki/{ancestor_url_component}"

# Guess the URL for the Wiktionary category index for terms in the first
#   language that are derived from the ancestor language.
lang_1_title = f"Category:{lang_1} terms derived from {ancestor}"
lang_1_url_component = lang_1_title.replace(" ", "_")
lang_1_url = f"{wiktionary}/wiki/{lang_1_url_component}"

# Guess the URL for the Wiktionary category index for terms in the first
#   language that are derived from the ancestor language.
lang_2_title = f"Category:{lang_2} terms derived from {ancestor}"
lang_2_url_component = lang_2_title.replace(" ", "_")
lang_2_url = f"{wiktionary}/wiki/{lang_2_url_component}"

url_correction_instructions = f"""
If the URL redirects or otherwise is not correct, please paste the
    correct URL below and press "Enter". If the URL is correct, simply
    press "Enter"."""

# Confirm lang_1_url.
print(f"""
Thank you. Your browser will now open a URL that might be for the
    Wiktionary category page for terms in {lang_1} that are derived
    from {ancestor}.""")
webbrowser.open(lang_1_url)
print(url_correction_instructions)
lang_1_url_response = input()
if lang_1_url_response != "":
    lang_1_url = lang_1_url_response

# Confirm lang_2_url.
print(f"""
Thank you. Your browser will now open a URL that might be for the
    Wiktionary category page for terms in {lang_2} that are derived
    from {ancestor}.""")
webbrowser.open(lang_2_url)
print(url_correction_instructions)
lang_2_url_response = input()
if lang_2_url_response != "":
    lang_2_url = lang_2_url_response

# Confirm ancestor_url.
print(f"""
Thank you. Your browser will now open a URL that might be for the
    Wikipedia page for {ancestor}.""")
webbrowser.open(ancestor_url)
print(url_correction_instructions)
ancestor_url_response = input()
if ancestor_url_response != "":
    ancestor_url = ancestor_url_response

# Specify the directory to which the csv file is to be saved.
print(f"""
Thank you. This program will produce a csv file listing {ancestor}
    terms alongside their {lang_1} and {lang_2} descendants.
    Please provide the path to the folder where you would like to save
    the file. In the file path, please replace each backslash with a
    double backslash (for example,
    "C:\\\\Users\\\\jdoe\\\\Documents").""")
path = input()

# Confirm filename.
filename = f"{lang_1}_{lang_2}_cognates.csv".lower()
print(f"""
Thank you. By default, the file will have the following name:
    {filename}
    If you are fine with that, simply press "Enter". If you would like to
    specify a different name, please enter it now. (Make sure to include
    the .csv extension in the name.)""")
filename_response = input()
if filename_response != "":
    filename = filename_response

# Alert the user that the program may take a while and get approval to
#   proceed.
print("""
Thank you. Note that this program may take up to 30 minutes to run. If
    you are ready to proceed, please press "Enter".""")
input()

start_time_2 = time.time()

# Run functions for the first language.
print(f"Finding category pages for {lang_1} terms derived from {ancestor}...")
elapsed_time()
lang_1_cat_pages = [lang_1_url]
get_wikt_cat_pages(lang_1_cat_pages)

print(f"Getting entries for {lang_1} terms derived from {ancestor}...")
elapsed_time()
lang_1_entries = []
get_wikt_entries(lang_1,
                 lang_1_cat_pages,
                 lang_1_entries)

print(f"Getting {ancestor} roots for {lang_1} terms...")
elapsed_time()
get_ancestor_roots(lang_1,
                   ancestor,
                   lang_1_entries)

# Run functions for the second language.
print(f"Finding category pages for {lang_2} terms derived from {ancestor}...")
elapsed_time()
lang_2_cat_pages = [lang_2_url]
get_wikt_cat_pages(lang_2_cat_pages)

print(f"Getting entries for {lang_2} terms derived from {ancestor}...")
elapsed_time()
lang_2_entries = []
get_wikt_entries(lang_2,
                 lang_2_cat_pages,
                 lang_2_entries)

print(f"Getting {ancestor} roots for {lang_2} terms...")
elapsed_time()
get_ancestor_roots(lang_2,
                   ancestor,
                   lang_2_entries)

# Find shared roots.
print("Finding shared roots...")
elapsed_time()
shared_roots= []
find_shared_roots(lang_1,
                  lang_2,
                  ancestor,
                  lang_1_entries,
                  lang_2_entries,
                  shared_roots)

print("Writing the file...")
elapsed_time()
# Change to the directory in which to save the csv.
os.chdir(path)
# Create a dataframe out of shared_roots.
df = pd.DataFrame(shared_roots)
# Write the dataframe to csv.
df.to_csv(filename, encoding="utf-8-sig")

# Figure out how long the input process took.
end_time = time.time()
input_duration = round(start_time_2 - start_time)
if input_duration < 60:
    input_duration = str(input_duration) + " seconds"
else:
    input_duration = str(round(input_duration/60)) + " minutes"
# Figure out how long the post-input process took.
post_input_duration = round(end_time - start_time_2)
if post_input_duration < 60:
    post_input_duration = str(post_input_duration) + " seconds"
else:
    post_input_duration = str(round(post_input_duration/60)) + " minutes"
# Figure out how long the program took to run in total.
total_duration = end_time - start_time
if total_duration < 60:
    total_duration = str(total_duration) + " seconds"
else:
    total_duration = str(round(total_duration/60)) + " minutes"

# Provide stats.
cognate_pairs = str(len(shared_roots))
lang_1_no = str(len(lang_1_entries))
lang_2_no = str(len(lang_2_entries))
print(f"""
Process complete. This program found {cognate_pairs} pairs of cognates
    between {lang_1} and {lang_2}. Overall, the program looked at
    {lang_1_no} {lang_1} terms and {lang_2_no} {lang_2} terms and found
    {cognate_pairs} pairs of cognates. It took {total_duration} in total
    to run: {input_duration} to receive the input, and
    {post_input_duration} thereafter to produce the csv file.

Thank you for using this program. To close this program, please press
    "Enter".""")

input()
