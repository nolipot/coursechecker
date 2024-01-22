#!/usr/bin/env python3
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

DRIVER_PATH = r'C:\Users\david\Downloads\chromedriver-win64\chromedriver.exe'

def printSomething():
    print("ur face looks like a mild face kiddo")

def saveCookies(path, driver):
    with open(path, 'w') as outputFile:
        json.dump(driver.get_cookies(), outputFile, indent="")

def loadCookies(path, driver):
    with open(path, 'r') as inputFile:
        for pastry in json.load(inputFile):
            driver.add_cookie(pastry)

def save_cookie(driver, path):
    with open(path, 'w') as filehandler:
        json.dump(driver.get_cookies(), filehandler)

def bakeCookies():
    chromeOptions = Options()
    chromeOptions.add_experimental_option("detach", True)
    serviceObj = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(service=serviceObj, options=chromeOptions)
    url = "https://cas.rutgers.edu/login"
    driver.get(url)
    driver.implicitly_wait(10)
    userText = driver.find_element(By.ID, "username")
    userText.send_keys("daf217")
    passText = driver.find_element(By.ID, "password")
    # print(os.environ.values)
    passText.send_keys("")
    btn = driver.find_element(By.CLASS_NAME, "btn-submit")
    btn.click()
    btn = driver.find_element(By.CLASS_NAME, "other-options-link")
    btn.click()
    btn = driver.find_element(By.XPATH, "//*[@data-testid='test-id-phone']")
    btn.click()
    trustBtn = driver.find_element(By.ID, "trust-browser-button")
    trustBtn.click()
    passed = driver.find_element(By.XPATH, "//header[@role='banner']")
    print(driver.current_url)
    if (passed):
        saveCookies(r"C:/Users/david/OneDrive/Documents/cookieKeys.json", driver)
    driver.get('https://sims.rutgers.edu/webreg/chooseSemester.htm')
    passed = driver.find_element(By.XPATH, "//h1[text()='Web Registration System']")
    if (passed):
        saveCookies(r"C:/Users/david/OneDrive/Documents/cookieTemp.json", driver)
    currentTime = time.strftime("%d-%m-%Y %H:%M:%S")
    print("Baked cookies: " + currentTime)
    driver.close()


def beginRegistering(semesterid, courseList):
    chromeOptions = Options()
    chromeOptions.add_experimental_option("detach", True)
    serviceObj = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(service=serviceObj, options=chromeOptions)
    urlbuilder = "https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection=" + semesterid + "&indexList="
    for sectionid in courseList:
        urlbuilder += sectionid + ","
    urlbuilder = urlbuilder[:-1]
    driver.get(urlbuilder)
    loadCookies(r'C:/Users/david/OneDrive/Documents/cookieKeys.json', driver)
    driver.refresh()
    driver.implicitly_wait(10)
    addCourseBtn = driver.find_element(By.CLASS_NAME, "btn-submit")
    if addCourseBtn.is_enabled():
        addCourseBtn.click()
    else:
        print("ERROR: add course option not available")
        driver.close()
        return False
    currentTime = time.strftime("%d-%m-%Y %H:%M:%S")
    print("Registered: " + currentTime)
    driver.close()
    return True

#driver.add_cookie({r"name": r"urfacebrodie", r'value': r'THIS IS THE VAL', r"expiry": 983451231})

if __name__ == '__main__':
    sectionNums = ['06785','06786','06787','06848','06849','06830','06831','06820','06822','06823',]
    sectionNums = ['17388', '17389']
    sem = "12024"
    bakeCookies()
    beginRegistering("12024", sectionNums)
    exit()

if cookiesRequest: # given by webberReq
    bakeCookies()
    exit()
result = beginRegistering(sem, sectionNums)
if (not result):
    bakeCookies()
    beginRegistering(sem, sectionNums)
print(sem, sectionNums)