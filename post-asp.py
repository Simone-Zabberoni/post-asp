#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Create an authenticated session to a ASP site, then post data to a form
# without breaking VIEWSTATE and EVENTVALIDATION

import requests
from bs4 import BeautifulSoup

loginURL = "http://www.targetsite.com/AspPrjXYZ/Login.aspx"
username = "foo"
password = "bar"

# Create the session object, then connect to the login page
s = requests.Session()
r = s.get(loginURL)

# Parse the page with soup, extract the ASP parameters
soup = BeautifulSoup(r.content, "html.parser")
VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']

# Create a dict with the correct parameters for logon and POST it
login_data = {
    "__VIEWSTATE": VIEWSTATE,
    "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
    "__EVENTVALIDATION": EVENTVALIDATION,
    "txtUser": username,
    "txtPassword": password,
    "cmbChooseLanguage": "1",
    "btnLogin": "Login"
}

# WARN: no logon status check, lots of aspx pages will return 200/OK even
# if logon fails, with the error message inside the html page
r = s.post(loginURL, data=login_data)

# Print session cookies.
# If login is successful there should be a .ASPXAUTH cookie
print s.cookies
print ("-------------------------------------")


# We use the same logic for POSTing data, using the same session object
# which contains the authenticated session cookies

# Load the page with the form we want to send
postURL = "http://www.targetsite.com/AspPrjXYZ/SomeForm.aspx"
r = s.get(postURL)
soup = BeautifulSoup(r.content, "html.parser")

# Parse the page with soup, extract the ASP parameters
VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']

# Create a dict with the post data according to the form and POST it
post_data = {
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": VIEWSTATE,
    "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
    "__EVENTVALIDATION": EVENTVALIDATION,
    "ctl01$plcPageContent$SSTab$tab00$SomeParameter": "Some String",
    "ctl01$plcPageContent$SSTab$tab00$AnotherOne": "42",
    "ctl01$plcPageContent$buttonBar$btnSubmit": "Submit"
}

print ("Posting...")
r = s.post(postURL, data=post_data)
print r

# Optional: print the resulting page
# print r.text
