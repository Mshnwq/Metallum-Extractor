import time

from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver import (Chrome, ChromeOptions, Firefox, FirefoxOptions,
                                FirefoxProfile)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Youtube_Worker(QThread):
    '''Browser Youtube Worker Thread'''
    done_signal = pyqtSignal()
    
    def __init__(self, selected):
        super().__init__()
        self.selected = selected

    def run(self):

        driver = webdriver.Chrome()
        # Create a new Firefox profile and set it to incognito mode
        # profile = FirefoxProfile()
        # profile.set_preference("browser.privatebrowsing.autostart", True)

        # # Set Firefox options to use the new profile
        # options = FirefoxOptions()
        # options.profile = profile

        # # Create a new Firefox browser instance with the specified options
        # driver = Firefox(options=options)

        # # Navigate to YouTube and search for the query
        ''' This is buffer for the following, apparently the first query in fails alot'''
        driver.get("https://www.youtube.com/")
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(self.selected['band_name'])
        search_box.send_keys(Keys.ENTER)
        # Open the first video in a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])

        # Loop over the albums in the band_dict
        for album in self.selected["band_albums"]:
            # Construct the search query
            search_query = f"{self.selected['band_name']} {album['name']} {album['year']}"

            # Navigate to YouTube and search for the query
            driver.get("https://www.youtube.com/")
            search_box = driver.find_element(By.NAME, "search_query")
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.ENTER)

            # Wait for the search results to load
            time.sleep(1)

            # Open the first video in a new tab
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])

        self.done_signal.emit()


def main():
    ...

if __name__ == '__main__':
    main()