import argparse
from tabulate import tabulate
from appleWebScrape import *


def main():
    parser = argparse.ArgumentParser(description="Apple Jobs Scraper")
    parser.add_argument("--sort", default="newest", help="Sorting type (default: newest)")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape (default: 1)")
    args = parser.parse_args()

    data = (getAppleJobs(args.sort, args.pages))
    headers = ['Company','Title', 'Location', 'Link','Date Posted']
    table = tabulate(data, headers, tablefmt='pipe')
    with open('output.md', 'w') as file:
        file.write(table)

if __name__ == "__main__":
    main()
