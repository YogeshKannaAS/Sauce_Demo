import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
STANDARD_PASSWORD = os.getenv("STANDARD_PASSWORD", "secret_sauce")

PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "20"))
IMPLICIT_WAIT = float(os.getenv("IMPLICIT_WAIT", "0"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))
