import requests
from bs4 import BeautifulSoup
import re


def eligible(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # job_description_div = soup.find('div', {'data-automation-id': 'jobPostingDescription'})
    # if job_description_div:
    #     print(job_description_div)
    # else:
    #     print("nope")
    description_meta_tag = soup.find('meta', {'name': 'description'})

    # Check if the meta tag is found
    if description_meta_tag:
        # Extract the content attribute of the meta tag
        description_content = description_meta_tag['content'].strip()
        match = re.search(r'(Minimum Qualifications|Requirements)(.*?)(Preferred Qualifications|Nice to Have)', description_content, re.DOTALL | re.IGNORECASE)
        if match:
            qualifications_substring = match.group(1).strip()
            # print(qualifications_substring)
        else:
            print("Qualifications not found. Here is the url", url)
            print(description_content)
        print("___________")
    else:
        print("Description meta tag not found. Here is the url", url)
        print("___________")


def getSnapJobs(role):
    snapChatUrl = 'https://careers.snap.com/jobs?role=Engineering'

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
                # print(element.text,url)
                eligible(url)
            # print(element.text)

if __name__ == "__main__":
    getSnapJobs('engineer')