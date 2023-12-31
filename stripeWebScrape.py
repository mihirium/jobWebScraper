import requests
from bs4 import BeautifulSoup
import re

job_links = []
url = "https://stripe.com/jobs/search?teams=Banking+as+a+Service&teams=Climate&teams=Connect&teams=Crypto&teams=Data+%26+Data+Science&teams=Indie+Hackers&teams=Infrastructure+%26+Corporate+Tech&teams=Mobile&teams=New+Financial+Products&teams=Payments&teams=Platform&teams=Revenue+%26+Financial+Automation&teams=Tax&teams=Tech+Programs&teams=Terminal&teams=University"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# What this does is gets the total page numbers for all the jobs in stripes list.
# It's because they restrict the amount of jobs per web page by 100, so I need to get
# all the possible webpages to scrape all the data.
li_elements = soup.select('ul.JobsPagination__list li')
els = []
for li in li_elements:
    els.append(li.get_text(strip=True))
filtered_list = [int(x) for x in els if x.isdigit()]

pageNums = max(filtered_list)

# This goes through all the page nums and gets all the job links I can now use.
skip = 100
for x in range(1,pageNums+1):

    matching_elements = soup.find_all('tr', class_='TableRow', attrs={'data-js-controller': 'TableRow'})
    for element in matching_elements:
        job_link = element.find('a', class_='Link JobsListings__link')
        if job_link:
            job_links.append(job_link['href'])
    url = "https://stripe.com/jobs/search?teams=Banking+as+a+Service&teams=Climate&teams=Connect&teams=Crypto&teams=Data+%26+Data+Science&teams=Indie+Hackers&teams=Infrastructure+%26+Corporate+Tech&teams=Mobile&teams=New+Financial+Products&teams=Payments&teams=Platform&teams=Revenue+%26+Financial+Automation&teams=Tax&teams=Tech+Programs&teams=Terminal&teams=University&skip=" + str(skip)
    skip += 100
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')


for url in job_links:
    jobUrl = "https://stripe.com" + url
    print(jobUrl)


