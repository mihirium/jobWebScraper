import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def eligible(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    element = soup.find('div', class_='wysiwyg', itemprop='qualifications').text
    experience_pattern = re.compile(r'(?:year|yr|yrs|years|PhD)')
    matches = experience_pattern.findall(element)
    jobDesc = []
    if len(matches) == 0:
        meta_tag = soup.find('meta', property='og:title')
        title = meta_tag.get('content')
        meta_tag = soup.find('meta', itemprop='datePosted')
        date_posted = meta_tag.get('content')
        date_posted = datetime.strptime(date_posted, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_posted = date_posted.strftime("%b %d, %Y")
        formatted_address_span = soup.find('span', itemprop='address')
        formatted_address = formatted_address_span.find('spl-job-location').get('formattedaddress')
        jobDesc.append("Block")
        jobDesc.append(title)
        jobDesc.append(formatted_address)
        jobDesc.append(url)
        jobDesc.append(date_posted)
    return jobDesc


def getBlockJobs(role="Software Engineering"):
    url = "https://careers.squareup.com/ca/en/jobs"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # This gets literally all roles available
    elements = soup.find_all('div', class_='pad-vert-line border-bottom')
    blockJobList = []
    # TODO: Add later for filtering for all roles
    # jobRoles = []
    # for x in elements:
    #     job_role = x.get('data-job-role')
    #     if(job_role not in jobRoles):
    #         jobRoles.append(job_role)

    for x in elements:
        job_role = x.get('data-job-role')
        if(str(job_role) == role):
            link = x.find('a')['href']
            jobData = eligible(link)
            if (len(jobData) != 0):
                blockJobList.append(jobData)
    print("BLOCK DONE")
    return blockJobList

