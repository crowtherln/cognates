This project scrapes Wiktionary to find cognates between different
    languages.

persian_english_cognates.py does this for Persian and English. The raw,
    uncleaned results from that program are in
    persian_english_cognates.csv

cognate_finder.py built on that program and can find cognates between
    any two languages that have Wiktionary category pages for terms in
    those languages derived from a common ancestor.

cognate_finder_results.csv lists the results of testing
    cognate_finder.py with different languages, in terms of how long
    the program took and how many pairs of cognates it found.

The remaining csv files include the raw, uncleaned results from running
    cognate_finder.py for different sets of languages.
