from pathlib import Path

# Directories
USERS_DIR = Path("users")
LOGS_DIR = "logs"

# URLs
SITE_URL = "http://test.com"
# I used to keep URL of this particular site in secret
# This is only demostration of how i'm writing and styling code
LOGIN_URL = SITE_URL + "/login/index.php"
LOGOUT_URL = SITE_URL + "/login/logout.php"
COURSES_URL = SITE_URL + "/?redirect=0"
USERS_FILE = Path(USERS_DIR, "dummy.csv")

# Titles
SITE_TITLE = "Портал дистанционного обучения"
LOGIN_TITLE = SITE_TITLE + ": Вход на сайт"

# Software
CHROME_DRIVER_URL = "chromedriver.exe"
