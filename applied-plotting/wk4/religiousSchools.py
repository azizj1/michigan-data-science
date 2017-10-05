import requests
from bs4 import BeautifulSoup

RELIGIOUS_SCHOOLS_BASE_URL = 'https://www.niche.com/k12/search/best-schools/s/wisconsin/'
RELIGIOUS_SCHOOLS_QUERY = '?type=private&religion=muslim&religion=jewish&religion=christian&religion=catholic' + \
                          '&gradeLevel=high'

def getNumberOfPages():
    page = requests.get(RELIGIOUS_SCHOOLS_BASE_URL + RELIGIOUS_SCHOOLS_QUERY)
    soup = BeautifulSoup(page.content, 'html.parser')
    return len(soup.select('.pagination__pages__selector option'))

def getReligiousSchools():
    numOfPages = getNumberOfPages()
    schools = []
    for i in range(1, numOfPages+1):
        page = requests.get(RELIGIOUS_SCHOOLS_BASE_URL + RELIGIOUS_SCHOOLS_QUERY + '&page={}'.format(i))
        soup = BeautifulSoup(page.content, 'html.parser')
        schools.extend(map(lambda s: s.text, soup.select('h2.search-result-entity-name')))
    return schools
