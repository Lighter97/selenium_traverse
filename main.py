import csv
import logging
import time
from datetime import datetime
from random import randint, shuffle

from selenium import webdriver

from config import (CHROME_DRIVER_URL, COURSES_URL, LOGIN_URL, LOGOUT_URL,
                    USERS_FILE, LOGS_DIR)

# Logging initializing
log_name = datetime.today().replace(microsecond=0).strftime("%d.%m.%Y_%H.%M")
logging.basicConfig(
    filename=f"{LOGS_DIR}\\moodle_{str(log_name)}.log",
    level=logging.INFO,
    format="%(message)s",
    filemode="w",
)

# Log the script start time
script_started = datetime.today().replace(microsecond=0)
logging.info(f"Script start - {script_started}")

# Initialize WebDriver
web = webdriver.Chrome(CHROME_DRIVER_URL)

# Open users list and shuffle it
with open(USERS_FILE, newline="") as users_file:
    reader = csv.reader(users_file, delimiter=",")
    users_dict = {k: v for k, v in reader}
    usernames = list(users_dict.keys())
    shuffle(usernames)

# Log the overall users count
users_count = len(users_dict)
logging.info(f"Readed {users_count} entries in {USERS_FILE}")

# Register the time of user started traverse
user_started = datetime.today().replace(microsecond=0)

# Variables for logging
errors_count = 0
bad_logins = []

# Traverse each user
for username in usernames:
    password = users_dict[username]
    visited = 0

    # Get login page
    web.get(LOGIN_URL)
    if "508" in web.title:
        while "508" in web.title:
            time.sleep(5)
            web.refresh()
            errors_count += 1

    # Login to user's account
    web.find_element_by_name("username").send_keys(username)
    web.find_element_by_name("password").send_keys(password)
    web.find_element_by_id("loginbtn").click()
    # This condition checks if site is down and showing HTTP 508 error
    # due to highload and counts errors for future statistics
    if "508" in web.title:
        while "508" in web.title:
            time.sleep(5)
            web.refresh()
            errors_count += 1

    # Bad login fallback
    if "Вход на сайт" in web.title:
        bad_logins.append(username)
        web.refresh()
        continue

    # Log the start of user's traverse
    logging.info(f"{username} - started")

    # Get courses page
    web.get(COURSES_URL)
    if "508" in web.title:
        while "508" in web.title:
            time.sleep(5)
            web.refresh()
            errors_count += 1

    # Get links to all user's courses
    courses = web.find_elements_by_xpath("//h3[@class='coursename']/a[1]")
    courses_links = [e.get_attribute("href") for e in courses]

    # Visit all courses' links
    for link in courses_links:
        web.get(link)
        if "508" in web.title:
            while "508" in web.title:
                time.sleep(5)
                web.refresh()
                errors_count += 1
        visited += 1
        time.sleep(10)

    # Sleep between different users
    time_to_sleep = randint(30, 180)
    time.sleep(time_to_sleep)
    logging.info(f"{username} - sleep by {time_to_sleep} after user")

    # Logout from current user's account
    web.get(LOGOUT_URL)
    logout_btn = web.find_element_by_xpath("//form/button[@type='submit']")
    logout_btn.click()

    # Log finish time and visited courses of user
    user_finished = datetime.today().replace(microsecond=0)
    logging.info(f"{username} - {visited} courses")
    logging.info(f"{username} - {user_finished - user_started}")

# Close the WebDriver
web.quit()

# Log the overall traverses users
bad_users = len(bad_logins)
traversed_users = users_count - bad_users
logging.info(f"Users - {traversed_users}/{users_count}")

# Log script-aware information
script_finished = datetime.today().replace(microsecond=0)
logging.info(f"Script end - {script_finished}")
logging.info(f"Script time - {script_finished - script_started}")
logging.info(f"HTTP 508 - {errors_count} ")
logging.info(f"Bad logins - {str(bad_logins)}")
