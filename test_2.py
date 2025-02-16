from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://tech-avito-intern.jumpingcrab.com/advertisements/")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_edit_ad(driver):
    """Тест на редактирование объявления с входом в его карточку"""
    # Находим поле поиска, вводим название объявления и ищем его
    search_field = driver.find_element(By.XPATH, "//input[@placeholder='Поиск по объявлениям']")
    search_field.clear()
    search_field.send_keys("Проверочное объявление")
    search_field.send_keys(Keys.RETURN)

    # Ожидание, пока появится хотя бы одно объявление
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Проверочное объявлен')]"))
    )

    # Находим все объявления с таким заголовком
    ads = driver.find_elements(By.XPATH, "//h4[contains(text(), 'Проверочное объявлен')]")

    if not ads:
        print("Ошибка: Объявление не найдено!")
        print(driver.page_source)  # Вывести HTML-страницы в консоль для диагностики
        return

    # Кликаем по первому объявлению
    ads[0].click()

    # Ожидание загрузки страницы объявления
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='css-nb383z']"))
    )

    # Кликаем по path в SVG (путь редактирования)
    path_button = driver.find_element(By.XPATH, "//div[@class='css-nb383z']//svg/path")
    path_button.click()

    time.sleep(2)
    # Меняем название, описание и цену
    name_field = driver.find_element(By.NAME, "name")
    name_field.clear()
    name_field.send_keys("Измененное проверочное объявление")

    price_field = driver.find_element(By.NAME, "price")
    price_field.clear()
    price_field.send_keys("150000")

    description_field = driver.find_element(By.NAME, "description")
    description_field.clear()
    description_field.send_keys("Описание измененного объявления")

    # Ожидание, пока кнопка "галочка" станет кликабельной
    save_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//svg[@style='cursor: pointer;']"))
    )
    save_button.click()

    # Ждем, пока изменения сохранятся
    time.sleep(2)

    # Ожидаем и кликаем на кнопку "Объявления"
    ads_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='css-3yj86i' and text()='Объявления']"))
    )
    ads_button.click()

    # Ждём, пока появится поле поиска
    search_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Поиск по объявлениям']"))
    )

    # Проверяем, что новое название и цена отображаются
    search_field.clear()
    search_field.send_keys("Измененное проверочное объявление")
    search_field.send_keys(Keys.RETURN)

    # Ждем загрузки обновленного объявления
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Измененное проверочное объявление')]"))
    )

    # Проверяем, что новое название и цена отображаются
    assert "Измененное проверочное объявление" in driver.page_source
    assert "150000" in driver.page_source
    assert "Описание измененного объявления" in driver.page_source