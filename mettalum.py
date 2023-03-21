import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import json
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from browser import Browser_Worker
import logging


class Metallum_Worker(QThread, Browser_Worker):
    '''Browser Metallum Worker Thread'''

    done_json_signal = pyqtSignal(object)

    def __init__(self, url):
        super().__init__()
        # Get the website URL from the user
        self.url = url

    def run(self):
        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox()

        # Navigate to the website
        driver.get(self.url)

        # Get the page source and parse it with Beautiful Soup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the needed in the HTML content
        all_dict = {}
        
        all_dict['band_name'] = soup.find('div', {'id': 'band_info'}).find('h1', {'class': 'band_name'}).find('a').text
        all_dict['band_pic_link'] = soup.find('div', {'id': 'band_sidebar'}).find('a', {'id': 'logo'})['href']
        
        # Find the discography category list
        discography_list = soup.find('div', {'id': 'band_disco'}).find('ul')
        # Extract the category names and URLs
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

        # Get the page source and parse it with Beautiful Soup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the table body
        table_body = soup.find('tbody')
        # Find all rows in the table
        rows = table_body.find_all('tr')

        # Find the data you need in the HTML content
        # Loop through the rows and extract the information
        all_dict['band_albums'] = []
        for row in rows:
            album = {}
            # extract columns
            cols = row.find_all("td")
            # Get the name of the music release
            album['name'] = cols[0].find("a").text
            # Get the type of the music release
            album['type'] = cols[1].text
            # Get the year of the music release
            album['year'] = cols[2].text
            # Get album website
            href = cols[0].find("a")['href']
            # Navigate to the album website
            driver.get(href)
            # Get the page source and parse it with Beautiful Soup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            # Store the album cover link
            album['album_pic_link'] = soup.find('div', \
                                {'class': 'album_img'}).find('a')['href']

            # append album JSON
            all_dict['band_albums'].append(album)

        # Close the web browser
        driver.quit()
        # emit completion signal
        self.done_json_signal.emit(all_dict)


    def getJSON(self):
        return self.albums_json


def main():
    app = QApplication(sys.argv)
    metallum_worker = Metallum_Worker()
    json = metallum_worker.getJSON()
    ...

if __name__ == '__main__':
    main()



