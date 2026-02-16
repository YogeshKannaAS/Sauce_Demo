import os
import re
import shutil
import tempfile
import time
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config


def _safe_name(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


@pytest.fixture()
def driver(request):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-features=NetworkServiceSandbox")
    if os.getenv("HEADLESS", "").lower() in ("1", "true", "yes"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    worker_id = os.getenv("PYTEST_XDIST_WORKER", "gw0")
    profile_root = Path(".pytest_chrome_profiles")
    profile_root.mkdir(parents=True, exist_ok=True)
    profile_dir = Path(
        tempfile.mkdtemp(prefix=f"{worker_id}_", dir=str(profile_root))
    )
    options.add_argument(f"--user-data-dir={profile_dir}")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        if config.IMPLICIT_WAIT:
            driver.implicitly_wait(config.IMPLICIT_WAIT)
        request.node.driver = driver
        yield driver
    finally:
        if driver:
            driver.quit()
        shutil.rmtree(profile_dir, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    driver = getattr(item, "driver", None)
    if not driver:
        return

    screenshots_dir = Path("reports") / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{_safe_name(item.nodeid)}_{int(time.time())}.png"
    file_path = screenshots_dir / filename
    driver.save_screenshot(str(file_path))
    allure.attach(
        driver.get_screenshot_as_png(),
        name=_safe_name(item.nodeid),
        attachment_type=allure.attachment_type.PNG,
    )


def pytest_collection_modifyitems(items):
    # Keep all Selenium UI tests on a single worker to reduce flakiness.
    for item in items:
        if "driver" in getattr(item, "fixturenames", []):
            item.add_marker(pytest.mark.xdist_group("ui"))
