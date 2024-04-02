import time

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup


class Browser:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = 'https://nn.hh.ru/search/vacancy'

    def search(self, post):
        self.browser.implicitly_wait(3)
        self.browser.get(self.url)
        time.sleep(3)
        input_text = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'a11y-search-input')))
        time.sleep(1)
        input_text.send_keys(post)
        time.sleep(3)
        self.browser.execute_script("window.scrollTo(0, 13500)")
        time.sleep(1)
        region = self.browser.find_element(By.XPATH, "//span[@data-qa='serp__novafilter-item-text' and descendant::span[@data-qa='serp__novafilter-title' and text()='Москва']]")
        time.sleep(3)
        region.click()
        time.sleep(3)
        self.browser.execute_script("window.scrollTo(0, 0)")
        time.sleep(1)
        button_search = self.browser.find_element(By.XPATH, '//*[@id="supernova_search_form"]/div/div[2]/button')
        time.sleep(3)
        button_search.click()
        time.sleep(3)

    def parse(self):
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        time.sleep(2)
        all_vacancies = soup.find_all(attrs={'class': "vacancy-serp-item-body__main-info"})
        return all_vacancies

    def clear_search(self, position):
        self.browser.execute_script("window.scrollTo(0, 0)")
        time.sleep(1)
        self.browser.find_element(By.ID, 'a11y-search-input').click()
        self.browser.find_element(By.ID, 'a11y-search-input').clear()
        time.sleep(1)
        self.browser.find_element(By.ID, 'a11y-search-input').send_keys(position)
        time.sleep(1)
        search = self.browser.find_element(By.XPATH, '//*[@id="supernova_search_form"]/div/div[2]/button')
        time.sleep(2)
        search.click()

    def to_next_page(self, next_button):
        self.browser.execute_script("window.scrollTo(0, 14500)")
        next_page = self.browser.find_element(By.XPATH, f"//a[@class='bloko-button' and @data-qa='pager-page']//span[text()='{next_button}']")
        next_page.click()

    def exit(self):
        self.browser.quit()
