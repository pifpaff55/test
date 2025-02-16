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

def test_create_ad(driver):
    """Тест на создание объявления"""
    driver.find_element(By.XPATH, "//button[contains(text(), 'Создать')]").click()
    time.sleep(1)  # Даем время на появление модального окна

    driver.find_element(By.NAME, "name").send_keys("Проверочное объявление")
    driver.find_element(By.NAME, "price").send_keys("-5000")
    driver.find_element(By.NAME, "description").send_keys("Описание проверочного объявления")
    driver.find_element(By.NAME, "imageUrl").send_keys("https://ru.freepik.com/free-photo/morskie-oko-tatry_1286255.htm#fromView=keyword&page=1&position=0&uuid=7b871d09-1186-42f6-ac38-9f8547ad1e3e&query=%D0%9A%D1%80%D0%B0%D1%81%D0%B8%D0%B2%D1%8B%D0%B5")

    driver.find_element(By.XPATH, "//button[contains(text(), 'Сохранить')]").click()
    time.sleep(2)  # Ждём завершения сохранения

    # Переходим в поле поиска и очищаем его
    search_field = driver.find_element(By.XPATH, "//input[@placeholder='Поиск по объявлениям']")
    search_field.clear()  # Очищаем поле, если в нем что-то есть
    search_field.send_keys("Проверочное объявление")
    search_field.send_keys(Keys.RETURN)

    # Ждем немного, чтобы результаты загрузились
    time.sleep(2)

    # Проверяем, что объявление найдено
    assert "Проверочное объявление" in driver.page_source
