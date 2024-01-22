#!/usr/bin/env python3
import requests
import json
from requests_html import HTMLSession
import time

payload = { #deprecated
    'subject': '198',
    'semester': '12023',
    'campus': 'NB',
    'level': 'U',
    'description': 'Writing',
    'code': '198'
}
courseList = [
    # '06785',
    # '06786',
    # '06787',
    # '06848',
    # '06849',
    # '06830',
    # '06831',
    # '06820',
    # '06821',
    # '06822',
    # '06823',
    '17388',
    '17389',
]

ses = HTMLSession()
req = requests.post("https://sis.rutgers.edu/soc", data=payload)

inputURL = {
    "year": 2024,
    "term": 1,
    "campus": "NB"
}

def loadJar(path):
    cookieJar = requests.cookies.RequestsCookieJar()
    with open(path, 'r') as inputFile:
        for pastry in json.load(inputFile):
            newCookie = requests.cookies.create_cookie(
                name=pastry['name'],
                #httponly=pastry['httpOnly'],
                path=pastry['path'],
                #samesize=pastry['sameSite'],
                secure=pastry['secure'],
                value=pastry['value']
            )
            cookieJar.set_cookie(newCookie)
    for cookie in cookieJar:
        print(f"Name: {cookie.name}")
        print(f"Value: {cookie.value}")
        print(f"Domain: {cookie.domain}")
        print(f"Path: {cookie.path}")
        print(f"Expires: {cookie.expires}")
        print(f"Secure: {cookie.secure}")
        print(f"HttpOnly: {cookie.get_nonstandard_attr('httponly')}")
        print(f"SameSite: {cookie.get_nonstandard_attr('samesite')}")
        print("--------")
    return cookieJar

def altJar(path):
    cookieTray = {}
    with open(path, 'r') as inputFile:
        for pastry in json.load(inputFile):
            cookieTray[pastry['name']] = pastry['value']
    return cookieTray

def headerCreator(cookieTray):
    headerDict = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '329',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f"JSESSIONID={cookieTray['JSESSIONID']}; EssUserTrk={cookieTray['EssUserTrk']};" +
          f"BIGipServereas-prod-webfarm-tcp-80-Pool={cookieTray['BIGipServereas-prod-webfarm-tcp-80-Pool']}",
        'Host': 'sims.rutgers.edu',
        'Origin': 'https://sims.rutgers.edu',
        'Referer': 'https://sims.rutgers.edu/webreg/refresh.htm',
        'sec-ch-ua': '"Chromium";v="116", "Google Chrome";v="116", "Not:A-Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    return headerDict

testPayload = {
    'coursesToAdd[0].courseIndex': '07394',
}

def directPost():
    print("starting")
    url = "https://sims.rutgers.edu/webreg/addCourses.htm"
    #print(loadCookies(r"C:/Users/david/OneDrive/Documents/cookiesTest.json"))
    cookieBasket = altJar(r"C:/Users/david/OneDrive/Documents/cookiesPost.json")
    testPayload = {}
    sesReq = requests.post(url, data=testPayload, headers=headerCreator(cookieBasket), cookies=cookieBasket)
    print(sesReq.reason)
    exit()

#https://sis.rutgers.edu/soc/api/courses.json?year=2022&term=9&campus=NB
#url for fetching all info of all courses

#https://sis.rutgers.edu/soc/api/courses.json      ---returns a json with detailed course information
#https://sis.rutgers.edu/soc/api/openSections.json ---returns a list of all open sections
if __name__ == '__main__':
    timestampCookies = time.time()
    timeInterval = 3 * 3600
    sesReq = ses.post("https://sis.rutgers.edu/soc/api/openSections.json", data=inputURL)
    openSec = sesReq.json()
    while len(courseList) > 0:
        sesReq = ses.post("https://sis.rutgers.edu/soc/api/openSections.json", data=inputURL)
        openSec = sesReq.json()
        for courseIndex in courseList:
            if(courseIndex in openSec):
                exec(open(r"webbernebber.py").read(), {'sectionNums' : courseList, 'sem' : str(inputURL["term"]) + str(inputURL["year"]), 'cookiesRequest': False})
                courseList.remove(courseIndex)
        time.sleep(1)
        if time.time() - timestampCookies > timeInterval:
            exec(open(r"webbernebber.py").read(), {'sectionNums' : courseList, 'sem' : str(inputURL["term"]) + str(inputURL["year"]), 'cookiesRequest': True})
            timestampCookies = time.time()