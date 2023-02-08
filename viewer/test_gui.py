import time

from django.test import TestCase
from django.db.utils import IntegrityError

# for selenium
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select


# Selenium
# pip install selenium
class StaffFormTestWithSelenium(LiveServerTestCase):

    def test_sign_up_and_login(self):
        selenium = webdriver.Chrome()
        time.sleep(2)
        # Choose your url to visit
        selenium.get('http://127.0.0.1:8000/')
        time.sleep(2)
        # find the elements you need to submit form
        login = selenium.find_element(By.ID, 'id_login')
        login.click()
        time.sleep(2)

        sign_up = selenium.find_element(By.ID, 'id_sign_up')
        sign_up.click()
        time.sleep(2)

        username = selenium.find_element(By.ID, 'id_username')
        password1 = selenium.find_element(By.ID, 'id_password1')
        password2 = selenium.find_element(By.ID, 'id_password2')
        username.send_keys('TestUser')
        time.sleep(2)
        password1.send_keys('MyTestPassword')
        time.sleep(2)
        password2.send_keys('MyTestPassword')
        time.sleep(2)
        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        login = selenium.find_element(By.ID, 'id_login')
        login.click()
        time.sleep(2)

        username = selenium.find_element(By.ID, 'id_username')
        password = selenium.find_element(By.ID, 'id_password')

        username.send_keys('TestUser')
        password.send_keys('MyTestPassword')
        time.sleep(2)

        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        assert 'Welcome in our movie database.' in selenium.page_source


    def test_add_new_staff(self):
        selenium = webdriver.Chrome()
        time.sleep(2)
        # Choose your url to visit
        selenium.get('http://127.0.0.1:8000/')
        time.sleep(2)
        # find the elements you need to submit form
        login = selenium.find_element(By.ID, 'id_login')
        login.click()
        time.sleep(2)

        username = selenium.find_element(By.ID, 'id_username')
        password = selenium.find_element(By.ID, 'id_password')

        username.send_keys('User1')
        password.send_keys('mojeheslo')
        time.sleep(2)

        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        new_staff_link = selenium.find_element(By.ID, 'id_new_staff_link')
        new_staff_link.click()
        time.sleep(2)

        name = selenium.find_element(By.ID, 'id_name')
        surname = selenium.find_element(By.ID, 'id_surname')
        artistname = selenium.find_element(By.ID, 'id_artist_name')
        county = selenium.find_element(By.ID, 'id_country')
        time.sleep(1)
        name.send_keys('Martin')
        time.sleep(1)
        surname.send_keys('Novák')
        time.sleep(1)
        artistname.send_keys('Novy')
        time.sleep(1)
        select_country = Select(selenium.find_element(By.ID, 'id_country'))
        time.sleep(1)
        select_country.select_by_visible_text('CZ')
        time.sleep(3)

        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        assert 'Welcome in our movie database.' in selenium.page_source
