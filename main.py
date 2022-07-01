"""
A google scraper by Sanchita Kapur
"""
import json

import requests
from bs4 import BeautifulSoup
from time import sleep
import sys



def google_scraper(query, start=0):
    records = []
    try:
        URL_TO_SCRAPE = "http://www.google.com/search?q=" + query.replace(' ', '+') + "&start=" + str(start * 10) \
                        + '&num=10&pws=0'
        print(URL_TO_SCRAPE)
        print("Checking on page# " + str(start + 1))

        payload = {'api_key': API_KEY, 'url': URL_TO_SCRAPE, 'render': 'false'}

        r = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
        soup = BeautifulSoup(r.text, 'lxml')
        results = soup.select('.yuRUbf > a')
        for result in results:
            heading = result.select('h3')
            records.append({'URL': result['href'], 'TITLE': heading[0].text})
            print(heading[0].text, ' ', result['href'])
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error. Technical Details given below.\n")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error. Technical Details given below.\n")
        print(str(e))
    finally:
        return records


if __name__ == '__main__':
    search_results = []
    NO_PAGES = 2
    args = sys.argv
    if len(args) < 2:
        print('Invalid Format: The correct format is: python main.py <Keyword>')
        exit()
    keyword = args[1]
    with open('API_KEY.txt', encoding='utf8') as f:
        API_KEY = f.read()

    for i in range(NO_PAGES):
        search_results.append({'PAGE_NO': i + 1, 'RESULTS': google_scraper(keyword, i)})
        sleep(5)

    if len(search_results) > 0:
        json_data = json.dumps(search_results)
        with open('google_results.json', 'w', encoding='utf8') as f:
            f.write(json_data)
