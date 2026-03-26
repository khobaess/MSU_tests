import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации WebDriver Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def screenshot_dir():
    """Фикстура для получения директории скриншотов"""
    screenshot_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots_msu")
    os.makedirs(screenshot_path, exist_ok=True)
    return screenshot_path

def make_screenshot(driver, name, screenshot_dir):
    """Функция для создания скриншота"""
    filepath = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(filepath)
    print(f"Скриншот сохранен: {filepath}")