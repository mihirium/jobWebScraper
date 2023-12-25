import argparse
from tabulate import tabulate
from appleWebScrape import *


def main():
    parser = argparse.ArgumentParser(description="Apple Jobs Scraper")
    parser.add_argument("--sort", default="relevance", help="Sorting type (default: relevance)")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape (default: 1)")
    args = parser.parse_args()

    data = (getAppleJobs(args.sort, args.pages))
    headers = ['Company','Title', 'Link']
    table = tabulate(data, headers, tablefmt='pipe')
    with open('output.md', 'w') as file:
        file.write(table)

if __name__ == "__main__":
    main()
