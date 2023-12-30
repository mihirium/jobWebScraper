import requests
import json

url = "https://api.greenhouse.io/v1/boards/sherwoodmedia/jobs"
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Now you can work with the JSON data as a Python dictionary
    jobs = data["jobs"]
    for job in jobs:
        print("Title:", job["title"])
        print("Location:", job["location"]["name"])
        print("Absolute URL:", job["absolute_url"])
        print("---")
else:
    print("Error:", response.status_code)

url = "https://api.greenhouse.io/v1/boards/robinhood/jobs"
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Now you can work with the JSON data as a Python dictionary
    jobs = data["jobs"]
    for job in jobs:
        print("Title:", job["title"])
        print("Location:", job["location"]["name"])
        print("Absolute URL:", job["absolute_url"])
        print("---")
else:
    print("Error:", response.status_code)
