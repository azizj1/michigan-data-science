import os.path as path
import requests
import pandas as pd
from bs4 import BeautifulSoup

RELIGIOUS_SCHOOLS_BASE_URL = 'https://www.niche.com/k12/search/best-schools/s/wisconsin/'
RELIGIOUS_SCHOOLS_QUERY = '?type=private&religion=muslim&religion=jewish&religion=christian&religion=catholic' + \
                          '&gradeLevel=high'
PERSISTED_LIST_FILE = './data/religious-schools.csv'

def getNumberOfPages():
    page = requests.get(RELIGIOUS_SCHOOLS_BASE_URL + RELIGIOUS_SCHOOLS_QUERY)
    soup = BeautifulSoup(page.content, 'html.parser')
    return len(soup.select('.pagination__pages__selector option'))

def loadSchoolsFromWeb():
    numOfPages = getNumberOfPages()
    schools = []
    for i in range(1, numOfPages+1):
        page = requests.get(RELIGIOUS_SCHOOLS_BASE_URL + RELIGIOUS_SCHOOLS_QUERY + '&page={}'.format(i))
        soup = BeautifulSoup(page.content, 'html.parser')
        schools.extend(map(lambda s: s.text, soup.select('h2.search-result-entity-name')))
    return schools

def readSchoolsFromCsv():
    return pd.read_csv(PERSISTED_LIST_FILE)

def writeCsv(schools):
    schools.to_csv(PERSISTED_LIST_FILE, header=True, index=False)

def getReligiousSchools():
    if path.exists(PERSISTED_LIST_FILE):
        return readSchoolsFromCsv()
    else:
        schools = pd.Series(loadSchoolsFromWeb(), name='SchoolName')
        writeCsv(schools)
        return schools
