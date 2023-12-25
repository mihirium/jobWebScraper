import argparse
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
        jobDesc.append(title)
        jobDesc.append(url)
    return jobDesc

def getAppleJobs(sort, numPages=1):
    appleJobList = []

    appleJobURL = "https://jobs.apple.com"
    
    for x in range(1, numPages + 1):
        page = requests.get("https://jobs.apple.com/en-us/search?search=software%20engineer&sort=" + sort + "&location=united-states-USA&page=" + str(x))
        soup = BeautifulSoup(page.content, 'html.parser')

        elements_with_class = soup.find_all(class_="table--advanced-search__title")

        for element in elements_with_class:
            href_content = element.get("href")
            myUrl = appleJobURL + href_content
            # print("THIS IS THE URL ACCESSING", myUrl)
            myPage = requests.get(myUrl)
            if(myPage.status_code == 200):
                jobData = eligible(myUrl)
                if len(jobData) != 0:
                    appleJobList.append(jobData)
    return appleJobList

def main():
    parser = argparse.ArgumentParser(description="Apple Jobs Scraper")
    parser.add_argument("--sort", default="relevance", help="Sorting type (default: relevance)")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape (default: 1)")
    args = parser.parse_args()

    print(getAppleJobs(args.sort, args.pages))

if __name__ == "__main__":
    main()
