import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def getDatePosted(soup):
    date_posted = soup.find("script", {"type": "application/ld+json"})
    date_posted = date_posted.contents[0] if date_posted else ""
    date_posted = re.search('"datePosted" : "(.*?)"', date_posted)
    date_posted = date_posted.group(1) if date_posted else ""
    formatted_date = datetime.strptime(date_posted, '%Y-%m-%d').strftime('%b %d, %Y')
    return formatted_date

def getLocation(soup):
    job_location = soup.find("script", {"type": "application/ld+json"})
    job_location = job_location.contents[0] if job_location else ""
    job_locality = re.search('"addressLocality" : "(.*?)"', job_location)
    city = job_locality.group(1).split(' -')[0] if job_locality else ""

    job_country = soup.find("script", {"type": "application/ld+json"})
    job_country = job_country.contents[0] if job_country else ""
    job_country = re.search('"addressCountry" : "(.*?)"', job_country)
    job_country = job_country.group(1) if job_country else ""
    output = city+ ", " + job_country
    return(output)

def eligible(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    description_meta_tag = soup.find('meta', {'name': 'description'})

    # Check if the meta tag is found
    jobDesc = []

    if description_meta_tag:
        # Extract the content attribute of the meta tag
        description_content = description_meta_tag['content'].strip()
        match = re.search(r'(Minimum Qualifications|Requirements)(.*?)(Preferred Qualifications|Nice to Have)', description_content, re.DOTALL | re.IGNORECASE)
        if match:
            qualifications_substring = match.group(2).strip()
            experience_pattern = re.compile(r'(?:year|yr|yrs|years|PhD)')
            matches = experience_pattern.findall(qualifications_substring)
            if len(matches) == 0:
                title_meta_tag = soup.find('meta', {'property': 'og:title'})
                title = title_meta_tag.get('content') if title_meta_tag else None
                datePosted = getDatePosted(soup)
                location = getLocation(soup)
                jobDesc.append("Snapchat")
                jobDesc.append(title)
                jobDesc.append(location)
                jobDesc.append(url)
                jobDesc.append(datePosted)
                # print(jobDesc)
        else:
            print("Qualifications not found. Here is the url", url)
            print(description_content)
            print("___________")
    else:
        print("Description meta tag not found. Here is the url", url)
        print("___________")
    return jobDesc 


def getSnapJobs(role="Engineering"):
    snapChatUrl = 'https://careers.snap.com/jobs?role=' + role
    snapJobList = []
    page = requests.get(snapChatUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements_with_class = soup.find_all(class_="css-p814w8")

    # This gets rid of the table header
    elements_with_class.pop(0)

    # Checks if there any experience reqs stated in title
    for element in elements_with_class:
        if not any(char.isdigit() for char in element.text):
            if element.find('a'):
                url = element.find('a')['href']
                jobData = eligible(url)
                if len(jobData):
                    snapJobList.append(jobData)
    return snapJobList
# if __name__ == "__main__":
#     getSnapJobs()