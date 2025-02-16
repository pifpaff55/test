from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://tech-avito-intern.jumpingcrab.com/advertisements/")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_search_ads(driver):
    """Тест на поиск объявлений"""
    search_field = driver.find_element(By.XPATH, "//input[@placeholder='Поиск по объявлениям']")

    def clear_search_field():
        """Очищает поле поиска"""
        search_field.clear()
        search_field.send_keys(Keys.CONTROL + "a")  # Выделить весь текст
        search_field.send_keys(Keys.BACKSPACE)      # Удалить выделенный текст

    # Тест 1: Поиск существующего объявления по точному названию
    clear_search_field()
    search_field.send_keys("Проверочное объявление")
    search_field.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "Проверочное объявление" in driver.page_source, "Тест 1: Поиск по точному названию не удался"

    # Тест 2: Поиск по общему слову "Объявление"
    clear_search_field()
    search_field.send_keys("Объявление")
    search_field.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "Объявление" in driver.page_source, "Тест 2: Поиск по общему слову не удался"

    # Тест 3: Поиск несуществующего объявления
    clear_search_field()
    search_field.send_keys("Рыба")
    search_field.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "Рыба" in driver.page_source, "Тест 3: Поиск рыбы не удался"

    # Тест 4: Поиск по цене объявления
    clear_search_field()
    search_field.send_keys("5000")
    search_field.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "5000" in driver.page_source, "Тест 4: Поиск по цене не удался"

    # Тест 5: Поиск по слову из описания
    clear_search_field()
    search_field.send_keys("Красивые")
    search_field.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "Красивые" in driver.page_source, "Тест 5: Поиск по слову из описания не удался"