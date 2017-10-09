import os.path as path
import requests
import pandas as pd
import privateSchools as priv
from bs4 import BeautifulSoup
from common import religiousSchoolsNameChanges

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
    schoolNames = []
    for i in range(1, numOfPages+1):
        page = requests.get(RELIGIOUS_SCHOOLS_BASE_URL + RELIGIOUS_SCHOOLS_QUERY + '&page={}'.format(i))
        soup = BeautifulSoup(page.content, 'html.parser')
        schoolNames.extend(map(lambda s: s.text, soup.select('h2.search-result-entity-name')))
    return schoolNames

def readSchoolsFromCsv():
    return pd.read_csv(PERSISTED_LIST_FILE)

def writeCsv(schoolsDf):
    schoolsDf.to_csv(PERSISTED_LIST_FILE, header=True, index=False)

def religiousSchoolNames():
    if path.exists(PERSISTED_LIST_FILE):
        return readSchoolsFromCsv()
    else:
        schoolNames = pd.DataFrame(loadSchoolsFromWeb(), columns=['SchoolName']) \
            .sort_values(by='SchoolName') \
            .drop_duplicates()
        writeCsv(schoolNames)
        return schoolNames

def schools(startingYr: int = 2007, minStudentsEveryYr: int = 0):
    privateSchools = priv.schools(startingYr, minStudentsEveryYr) \
                        .replace({'SchoolName': religiousSchoolsNameChanges()}, regex=True)
    religiousSchools = religiousSchoolNames().replace(religiousSchoolsNameChanges(), regex=True).drop_duplicates()
    return pd.merge(privateSchools, religiousSchools, how='inner', on='SchoolName')
