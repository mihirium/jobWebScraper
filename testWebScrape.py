import argparse
from tabulate import tabulate
from appleWebScrape import *
from snapWebScrape import *
from blockWebScrape import *

def date_key(sub_array):
    return datetime.strptime(sub_array[4], '%b %d, %Y')

def main():
    parser = argparse.ArgumentParser(description="Jobs Scraper")
    # parser.add_argument("--sort", default="newest", help="Sorting type (default: newest)")
    # parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape (default: 1)")
    args = parser.parse_args()

    snap = getSnapJobs()
    apple = getAppleJobs()
    block = getBlockJobs()
    combined = snap + apple + block


    sorted_data = sorted(combined, key=date_key, reverse=True)

    headers = ['Company','Title', 'Location', 'Link','Date Posted']

    table = tabulate(sorted_data, headers, tablefmt='pipe')
    with open('README.md', 'w') as file:
        file.write(table)

if __name__ == "__main__":
    main()
