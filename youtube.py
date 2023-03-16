import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import json
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from browser import Browser_Worker


class Youtube_Worker(QThread, Browser_Worker):
    '''Browser Youtube Worker Thread'''
    def __init__(self):
        super().__init__()
        

    def run(self):
        # Get the website URL from the user
        base_url = 'https://www.metal-archives.com'
        # path = input('Enter band name: ')
        path = 'Peste_Noire/12841'

        url = f'{base_url}/bands/{path}'
        print(url)

        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox()

        # Navigate to the website
        driver.get(url)

        # Get the page source and parse it with Beautiful Soup
        page_source = driver.page_source
        # print(page_source)
        soup = BeautifulSoup(page_source, 'html.parser')

        # # Find the data you need in the HTML content
        # Find the discography category list
        discography_list = soup.find('div', {'id': 'band_disco'}).find('ul')


        # Extract the category names and URLs
        # categories = []
        # print(discography_list)
        complete_discography_url = ''
        for item in discography_list.find_all('li'):
            if (item.find('span').text == "Complete discography"):
                complete_discography_url = item.find('a')['href']
                break
                # categories.append({'category': category, 'url': url})
        if complete_discography_url == '':
            exit("error")

        # Navigate to the complete discography 
        driver.get(complete_discography_url)

        page_source = driver.page_source
        # print(page_source)
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the table body
        table_body = soup.find('tbody')

        # Find all rows in the table
        rows = table_body.find_all('tr')

        # Find the data you need in the HTML content
        # Loop through the rows and extract the information
        # print(rows)
        all_albums_dict = {}
        all_albums_dict['albums'] = []
        for row in rows:
            album = {}
            # extract columns
            cols = row.find_all("td")
            # Get the name of the music release
            name = cols[0].find("a").text
            album['name'] = name
            # Get the type of the music release
            _type = cols[1].text
            album['type'] = _type
            # Get the year of the music release
            year = cols[2].text
            album['year'] = year

            href = cols[0].find("a")['href']
            album['href'] = href

            # Print the extracted information
            # print(f"\nName: {name},\t Type: {_type}, Year: {year}")
            # print(href)
            all_albums_dict['albums'].append(album)

        # Close the web browser
        driver.quit()

        # Print the list of categories and URLs
        self.albums_json = json.dumps(all_albums_dict, indent=3)

        print(self.albums_json)



def main():
    app = QApplication(sys.argv)
    youtube_worker = Youtube_Worker()
    json = youtube_worker.getJSON()
    ...

if __name__ == '__main__':
    main()



