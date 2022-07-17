This project scrapes [Wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Main_Page 'Wiktionary, the free dictionary') to find cognates between different languages. [__cognate\_finder.py__](https://github.com/crowtherln/cognates/blob/master/cognate_finder.py 'cognates/cognate_finder.py at master • crowtherln/cognates') is the main program, which users can run to find cognates between any two languages that have Wiktionary category pages for terms in those languages derived from a common ancestor.

I tested 15 language pairs. For each language pair, [__cognate\_finder\_results.csv__](https://github.com/crowtherln/cognates/blob/master/cognate_finder_results.csv 'cognates/cognate_finder_results.csv at master • crowtherln/cognates') shows how many cognate pairs were found and how long the program took to run. Program duration ranged from 1–46 minutes, depending largely on how well-documented the chosen languages were on English Wiktionary.

_cognate\_finder.py_ was built from my earlier program, [__persian\_english\_cognates.py__](https://github.com/crowtherln/cognates/blob/master/persian_english_cognates.py 'cognates/persian_english_cognates.py at master • crowtherln/cognates'), which does the same thing but just for Persian and English.

The raw, uncleaned output from both programs is in the [__example\_results__ folder](https://github.com/crowtherln/cognates/tree/master/example_results 'cognates/example_results at master • crowtherln/cognates').

[wiktionary\_derived\_terms\_categories.csv__](https://github.com/crowtherln/cognates/blob/master/wiktionary_derived_terms_categories.csv 'cognates/wiktionary_derived_terms_categories.csv at master • crowtherln/cognates') lists Wiktionary category pages for terms in one language derived from another. The Python script I wrote to scrape that data is not currently in this repository.
