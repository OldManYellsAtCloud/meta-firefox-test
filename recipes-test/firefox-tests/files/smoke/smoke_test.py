import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

def test_smoke():
    driver = webdriver.Firefox()
    driver.get("https://www.example.com")
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    expected_text = "This domain is for use in documentation examples without needing permission. Avoid use in operations."
    actual_text = paragraphs[0].text
    driver.quit()
    assert actual_text == expected_text, "Could not load example.com. Actual text: %s" % actual_text

