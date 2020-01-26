#! python3
# piiAndPgFromPie.py - Produce list of links to Wiktionary pages for Proto-Indo-European (PIE) terms inherited by both Proto-Indo-Iranian (PII) and Proto-Germanic (PG)

import requests, time
from bs4 import BeautifulSoup

# Part 1: Create lists
piiLinks = [] # links to Wiktionary pages for PII terms inherited from PIE
pieOriginsOfPii = [] # links to Wiktionary pages for PIE terms inherited by PII
pgLinks = [] # links to Wiktionary pages for PG terms inherited from PIE
pieOriginsOfPg = [] # links to Wiktionary pages for PIE terms inherited by PG
pieOriginsOfPiiAndPg = [] # links to Wiktionary pages for PIE terms inherited by both PII and PG

# Part 2: Fill piiLinks
# Part 2.1: Add to piiLinks from first page of PII terms inherited from PIE
piiUrl1 = "https://en.wiktionary.org/wiki/Category:Proto-Indo-Iranian_terms_inherited_from_Proto-Indo-European"
piiResponse1 = requests.get(piiUrl1)
piiData1 = piiResponse1.text
piiSoup1 = BeautifulSoup(piiData1, 'lxml')
piiTags1 = piiSoup1.find_all('a')
for tag in piiTags1:
    href = tag.get('href')
    if href is not None:
        if href.startswith('/wiki/Reconstruction:Proto-Indo-Iranian/'):
            piiLinks.append(str('https://en.wiktionary.org' + href))

# Part 2.2: Add to piiLinks from second page of PII terms inherited from PIE
piiUrl2 = 'https://en.wiktionary.org/w/index.php?title=Category:Proto-Indo-Iranian_terms_inherited_from_Proto-Indo-European&pagefrom=MANZD%CA%B0HR%C3%81S%0AProto-Indo-Iranian%2Fmanzd%CA%B0Hr%C3%A1s#mw-pages'
piiResponse2 = requests.get(piiUrl2)
piiData2 = piiResponse2.text
piiSoup2 = BeautifulSoup(piiData2, 'lxml')
piiTags2 = piiSoup2.find_all('a')
for tag in piiTags2:
    href = tag.get('href')
    if href is not None:
        if href.startswith('/wiki/Reconstruction:Proto-Indo-Iranian/'):
            piiLinks.append(str('https://en.wiktionary.org' + href))

# Part 2.3: Add to piiLinks from third page of PII terms inherited from PIE
piiUrl3 = 'https://en.wiktionary.org/w/index.php?title=Category:Proto-Indo-Iranian_terms_inherited_from_Proto-Indo-European&pagefrom=%C4%86R%CC%A5HW%C3%81S%0AProto-Indo-Iranian%2F%C4%87r%CC%A5Hw%C3%A1s#mw-pages'
piiResponse3 = requests.get(piiUrl3)
piiData3 = piiResponse3.text
piiSoup3 = BeautifulSoup(piiData3, 'lxml')
piiTags3 = piiSoup3.find_all('a')
for tag in piiTags3:
    href = tag.get('href')
    if href is not None:
        if href.startswith('/wiki/Reconstruction:Proto-Indo-Iranian/'):
            piiLinks.append(str('https://en.wiktionary.org' + href))

# Part 3: Get links to PIE terms inherited by PII to fill pieOriginsOfPii
for i in piiLinks:
    piePiiResponse = requests.get(i)
    piePiiData = piePiiResponse.text
    piePiiSoup = BeautifulSoup(piePiiData, 'lxml')
    piePiiTags = piePiiSoup.find_all('a')
    for tag in piePiiTags:
        href = tag.get('href')
        if href is not None:
            if href.startswith('/wiki/Reconstruction:Proto-Indo-European'):
                pieOriginsOfPii.append(str('https://en.wiktionary.org' + href))
    time.sleep(2)

# Part 4: Fill pgLinks
# Part 4.1: Add to pgLinks from first page of PG terms inherited from PIE
pgUrl1 = "https://en.wiktionary.org/wiki/Category:Proto-Germanic_terms_inherited_from_Proto-Indo-European"
pgResponse1 = requests.get(pgUrl1)
pgData1 = pgResponse1.text
pgSoup1 = BeautifulSoup(pgData1, 'lxml')
pgTags1 = pgSoup1.find_all('a')
for tag in pgTags1:
    href = tag.get('href')
    if href is not None:
        if href.startswith('/wiki/Reconstruction:Proto-Germanic/'):
            pgLinks.append(str('https://en.wiktionary.org' + href))

# Part 4.2: Add to pgLinks from second page of PG terms inherited from PIE
pgUrl2 = 'https://en.wiktionary.org/w/index.php?title=Category:Proto-Germanic_terms_inherited_from_Proto-Indo-European&pagefrom=HAFRAZ%0AProto-Germanic%2Fhafraz#mw-pages'
pgResponse2 = requests.get(pgUrl2)
pgData2 = pgResponse2.text
pgSoup2 = BeautifulSoup(pgData2, 'lxml')
pgTags2 = pgSoup2.find_all('a')
for tag in pgTags2:
    href = tag.get('href')
    if href is not None:
        if href.startswith('/wiki/Reconstruction:Proto-Germanic/'):
            pgLinks.append(str('https://en.wiktionary.org' + href))

# Part 4.3: Add to pgLinks from third page of PG terms inherited from PIE
pgUrl3 = 'https://en.wiktionary.org/w/index.php?title=Category:Proto-Germanic_terms_inherited_from_Proto-Indo-European&pagefrom=SA%0AProto-Germanic%2Fsa#mw-pages'
pgResponse3 = requests.get(pgUrl3)
pgData3 = pgResponse3.text
pgSoup3 = BeautifulSoup(pgData3, 'lxml')
pgTags3 = pgSoup3.find_all('a')
for tag in pgTags3:
    href = tag.get('href')
    if href is not None:
        if href.startswith('/wiki/Reconstruction:Proto-Germanic/'):
            pgLinks.append(str('https://en.wiktionary.org' + href))

# Part 4.4: Add to pgLinks from fourth page of PG terms inherited from PIE
pgUrl4 = 'https://en.wiktionary.org/w/index.php?title=Category:Proto-Germanic_terms_inherited_from_Proto-Indo-European&pagefrom=%C3%9EWERANAN%0AProto-Germanic%2F%C3%BEweran%C4%85#mw-pages'
pgResponse4 = requests.get(pgUrl4)
pgData4 = pgResponse4.text
pgSoup4 = BeautifulSoup(pgData4, 'lxml')
pgTags4 = pgSoup4.find_all('a')
for tag in pgTags4:
    href = tag.get('href')
    if href is not None:
        if href.startswith('/wiki/Reconstruction:Proto-Germanic/'):
            pgLinks.append(str('https://en.wiktionary.org' + href))

# Part 5: Get links to PIE terms inherited by PG to fill pieOriginsOfPg
for i in pgLinks:
    piePgResponse = requests.get(i)
    piePgData = piePgResponse.text
    piePgSoup = BeautifulSoup(piePgData, 'lxml')
    piePgTags = piePgSoup.find_all('a')
    for tag in piePgTags:
        href = tag.get('href')
        if href is not None:
            if href.startswith('/wiki/Reconstruction:Proto-Indo-European'):
                pieOriginsOfPg.append(str('https://en.wiktionary.org' + href))
    time.sleep(2)

# Part 6: Find common elements between pieOriginsOfPii and pieOriginsOfPg to fill pieOriginsOfPiiAndPg
for i in set(pieOriginsOfPii) & set(pieOriginsOfPg):
    pieOriginsOfPiiAndPg.append(i)

pieOriginsOfPiiAndPg.sort()

for i in pieOriginsOfPiiAndPg:
    print(i)
