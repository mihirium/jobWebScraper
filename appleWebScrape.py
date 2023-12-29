import requests
from bs4 import BeautifulSoup
import re


def eligible(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    qualifications_list = str(soup.find('div', {'id': 'jd-key-qualifications'}).find('ul', {'class': 'jd__list'}))
    experience_pattern = re.compile(r'(?:year|yr|yrs|years)')
    jobDesc = []
    matches = experience_pattern.findall(qualifications_list)
    if len(matches) == 0:
        title = soup.find('h1', {'class': 'jd__header--title'}).text
        datePosted = soup.find('time', {'id': 'jobPostDate'}).text
        location_div = soup.find('div', {'id': 'job-location-name'})

        if location_div:
            locality = location_div.find('span', {'itemprop': 'addressLocality'}).text
            region = location_div.find('span', {'itemprop': 'addressRegion'}).text
            country = location_div.find('span', {'itemprop': 'addressCountry'}).text
        location = locality + ', ' + region + ', ' + country
        jobDesc.append("Apple")
        jobDesc.append(title)
        jobDesc.append(location)
        jobDesc.append("[Link](" + url +")")
        jobDesc.append(datePosted)
    return jobDesc 

def getAppleJobs(sort="newest", numPages=1):
    appleJobList = []

    appleJobURL = "https://jobs.apple.com"
    
    for x in range(1, numPages + 1):
        page = requests.get("https://jobs.apple.com/en-us/search?search=software%20engineer&sort=" + sort + "&location=united-states-USA&page=" + str(x))
        soup = BeautifulSoup(page.content, 'html.parser')

        elements_with_class = soup.find_all(class_="table--advanced-search__title")

        for element in elements_with_class:
            href_content = element.get("href")
            myUrl = appleJobURL + href_content
            myPage = requests.get(myUrl)
            if(myPage.status_code == 200):
                jobData = eligible(myUrl)
                if len(jobData) != 0:
                    appleJobList.append(jobData)
    print("APPLE DONE")
    return appleJobList