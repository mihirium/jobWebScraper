import argparse
import requests
from bs4 import BeautifulSoup
import re

def eligible(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    qualifications_list = str(soup.find('div', {'id': 'jd-key-qualifications'}).find('ul', {'class': 'jd__list'}))
    experience_pattern = re.compile(r'(?:year|yr|yrs|years)')

    matches = experience_pattern.findall(qualifications_list)
    if len(matches) == 0:
        return True
    return False

def getAppleJobs(sort, numPages=1):
    appleJobURL = "https://jobs.apple.com"
    
    for x in range(1, numPages + 1):
        page = requests.get("https://jobs.apple.com/en-us/search?search=software%20engineer&sort=" + sort + "&location=united-states-USA&page=" + str(x))
        soup = BeautifulSoup(page.content, 'html.parser')

        elements_with_class = soup.find_all(class_="table--advanced-search__title")

        for element in elements_with_class:
            href_content = element.get("href")
            myUrl = appleJobURL + href_content
            if eligible(myUrl):
                print(myUrl)

def main():
    parser = argparse.ArgumentParser(description="Apple Jobs Scraper")
    parser.add_argument("--sort", default="relevance", help="Sorting type (default: relevance)")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape (default: 3)")
    args = parser.parse_args()

    getAppleJobs(args.sort, args.pages)

if __name__ == "__main__":
    main()
