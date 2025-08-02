# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
from time import sleep

class InstaDL:
    """A class to download Instagram reels and photos using Selenium."""
    def __init__(self):
        pass

    def _configure_chrome(self) -> webdriver.Chrome:
        """Configures and returns a headless Chrome WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("headless")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        return webdriver.Chrome(options=chrome_options)

    def _get_data(self, url) -> soup:
        """Fetches the HTML content of the Instagram page and returns a BeautifulSoup object."""
        driver = self._configure_chrome()
        try:
            driver.get("https://clipdown.app/en")
            sleep(1)
            input_element = driver.find_element(By.ID, "s_input")
            input_element.send_keys(url)
            driver.execute_script("document.getElementById('btn_start').click();")
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "download-box"))
            )
            html_source = driver.page_source
            return soup(html_source, "html.parser")
        except Exception as e:
            raise e
        finally:
            driver.quit()

    def Reel(self, url) -> dict:
        """Downloads an Instagram reel from the provided URL."""
        data = self._get_data(url)
        res = []
        try:
            row = data.find("div", {"id": "download-result"}).find("ul", {"class": "download-box"})
            link = row.find("li").find("a", {"title": "Download Video"})
            res.append(link.get("href"))
            return {"status": True, "url": res, "type": "reel"}
        except AttributeError:
            return {"status": False, "url": res, "type": "reel"}

    def Photo(self, url) -> dict:
        """Downloads an Instagram photo from the provided URL."""
        data = self._get_data(url)
        res = []
        try:
            row = data.find("div", {"id": "download-result"}).find("ul", {"class": "download-box"})
            links = row.find_all("li")
            for link in links:
                link = link.find("a")
                res.append(link.get("href"))
            return {"status": True, "url": res, "type": "photo"}
        except AttributeError:
            return {"status": False, "url": res, "type": "photo"}