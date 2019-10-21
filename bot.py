import sys, os, pathlib
from selenium import webdriver
from time import sleep
from typing import Union, List
# from getpass import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_profile import  FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import MoveTargetOutOfBoundsException
# print(sys.path)
# print(pathlib.Path(__file__).parent)
# print(__file__)

class Selenium_bot():
    def __init__(self, javascript=True):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 0)
        profile.set_preference('general.useragent.vendor', 'Linux Mint')
        profile.DEFAULT_PREFERENCES['frozen']['dom.webnotifications.serviceworker.enabled'] = False
        profile.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = javascript
        opts = Options()
        opts.profile = profile
        caps = DesiredCapabilities.FIREFOX
        caps['marionette'] = True
        # caps['firefox_profile'] = profile.encoded
        path_to_driver = 'static/geckodriver'
        bin = FirefoxBinary(path_to_driver)
        self.driver = webdriver.Firefox(executable_path=path_to_driver,
                                        options=opts,
                                        capabilities=caps, )
        self.action = ActionChains(self.driver)
    
   
    def go_to(self, url):
        self.driver.get(url)

    def how_much_elements(self, element):
        return len(self.driver.find_elements_by_xpath(element))
    
    def check_click_check(self, label:str, button:str, i:int):
        # check the valua of the label
        check = self.driver.find_elements_by_xpath(label)[i].text
        # check if the button is there
        button_display = self.driver.find_elements_by_xpath(button)[i].is_displayed()
        # click in the button
        self.driver.find_elements_by_xpath(button)[i].click()
        # check the value of the label before click in button
        check2 = self.driver.find_elements_by_xpath(label)[i].text

        return [check, check2, button_display]

    def measure_scroll_check():
        pass
    
    def click_check(self):
        pass


    
    def write_check(self, xpath, text):
        # get element
        element_text = self.driver.find_element_by_xpath(xpath)
        # click and send text
        # self.action.click(element_text)
        # self.action.send_keys(text) 
        self.action.send_keys_to_element(element_text, text)
        self.action.perform()
        # self.action.perform()
        # get text element
        text_in_field =  self.driver.find_element_by_xpath(xpath).get_attribute('value')
        # print(text_in_field)
        return text_in_field.strip()
    
    def write(self, xpath, text):
        element = self.driver.find_element_by_xpath(xpath)
        self.action.double_click(element)
        self.action.send_keys_to_element(element, text)
        
       



    def get_text(self, selector):
        pass



if __name__== '__main__' :
   bot = Selenium_bot()
   
