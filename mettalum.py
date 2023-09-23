from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver


class Metallum_Worker(QThread):
    '''Browser Metallum Worker Thread'''

    done_json_signal = pyqtSignal(object)

    def __init__(self, url, with_image: bool):
        super().__init__()
        # Get the website URL from the user
        self.url = url
        self.with_image = with_image

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
        
        all_dict['band_name'] = soup.find('div', {'id': 'band_info'}).find('h1', {'class': 'band_name'}).find('a').text # type: ignore
        all_dict['band_pic_link'] = soup.find('div', {'id': 'band_sidebar'}).find('a', {'id': 'logo'})['href'] # type: ignore
        
        # Find the discography category list
        discography_list = soup.find('div', {'id': 'band_disco'}).find('ul') # type: ignore
        # Extract the category names and URLs
        complete_discography_url = ''
        for item in discography_list.find_all('li'): # type: ignore
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
        rows = table_body.find_all('tr') # type: ignore

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
            
            if self.with_image:
                # Get album website
                href = cols[0].find("a")['href']
                # Navigate to the album website
                driver.get(href)
                # Get the page source and parse it with Beautiful Soup
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                try:
                    # Store the album cover link
                    album['album_pic_link'] = soup.find('div', \
                                        {'class': 'album_img'}).find('a')['href'] # type: ignore
                except:
                    album['album_pic_link'] = ''
            else: # no album image
                album['album_pic_link'] = ''

            # append album JSON
            all_dict['band_albums'].append(album)

        # Close the web browser
        driver.quit()
        # emit completion signal
        self.done_json_signal.emit(all_dict)


def main():
    ...

if __name__ == '__main__':
    main()



