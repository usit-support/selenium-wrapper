from typing import Optional, List, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from faker import Faker
import yaml
from pathlib import Path

class ChromeBrowser:
    """Chrome browser wrapper following SOLID principles."""
    
    def __init__(self, config_path: str = 'chrome.yml', base_url: str = None):
        self.config = self._load_config(config_path)
        self.driver = self._initialize_driver()
        self.faker = Faker('fr_FR')
        if base_url:
            self.driver.get(base_url)

    def _load_config(self, config_path: str) -> dict:
        """Load chrome configuration from YAML file."""
        try:
            with open(config_path, 'r') as chrome_file:
                return yaml.safe_load(chrome_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

    def _initialize_driver(self) -> webdriver.Chrome:
        """Initialize Chrome driver with configuration."""
        chrome_service = Service(executable_path=self.config['EXECUTABLE_PATH'])
        print(self.config['EXECUTABLE_PATH'])

        chrome_options = Options()
        for arg in self.config['LIST_ARGUMENT']:
            chrome_options.add_argument(arg)
            
        return webdriver.Chrome(service=chrome_service, options=chrome_options)

    def click_element(self, element_xpath: str) -> Optional[WebElement]:
        """Click element by xpath."""
        try:
            element = self.driver.find_element(By.XPATH, element_xpath)
            element.click()
            return element
        except NoSuchElementException:
            raise NoSuchElementException(f"Element not found: {element_xpath}")

    def click_menu(self, menu_text: str) -> Optional[WebElement]:
        """Click menu item by text."""
        elements = self.driver.find_elements(By.XPATH, ".//a")
        for element in elements:
            if element.get_attribute('text') == menu_text:
                element.click()
                return element
        raise NoSuchElementException(f"Menu item not found: {menu_text}")

    def set_value(self, element_xpath: str, value: str) -> bool:
        """Set value in field, supporting fake data generation."""
        try:
            element = self.driver.find_element(By.XPATH, element_xpath)
            fake_value = self._generate_fake_value(value)
            element.send_keys(fake_value)
            return True
        except NoSuchElementException:
            raise NoSuchElementException(f"Element not found: {element_xpath}")

    def _generate_fake_value(self, value_type: str) -> str:
        """Generate fake data based on type."""
        fake_data_map = {
            "fake.name": self.faker.name,
            "fake.company": self.faker.company,
            "fake.job": self.faker.job,
            "fake.email": self.faker.email,
            "fake.address": self.faker.address,
            "fake.text": self.faker.text
        }
        return fake_data_map.get(value_type, lambda: value_type)()

    def get_element_info(self, element: WebElement) -> dict:
        """Get element information."""
        return {
            "id": element.get_attribute("id"),
            "class": element.get_attribute("class"),
            "tag_name": element.tag_name,
            "displayed": element.is_displayed(),
            "location": element.location,
            "size": element.size,
            "text": element.text
        }

    def find_element(self, element_xpath: str, get_parent: bool = False) -> WebElement:
        """Find element by xpath."""
        try:
            element = self.driver.find_element(By.XPATH, element_xpath)
            return element.find_element(By.XPATH, "..") if get_parent else element
        except NoSuchElementException:
            raise NoSuchElementException(f"Element not found: {element_xpath}")

    def close(self) -> None:
        """Close browser instance."""
        self.driver.quit()