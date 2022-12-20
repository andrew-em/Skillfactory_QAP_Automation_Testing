import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome('c:/IT/QA/chromedriver.exe')
    # Устанавливаем неявное ожидание
    driver.implicity_wait(10)
    # Переходим на страницу авторизации
    driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('givve@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('lederid2022')



def test_show_my_pets(driver):
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Устанавливаем неявное ожидание
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
       assert images[i].get_attribute('src') != ''
       assert names[i].text != ''
       assert descriptions[i].text != ''
       assert ', ' in descriptions[i]
       parts = descriptions[i].text.split(", ")
       assert len(parts[0]) > 0
       assert len(parts[1]) > 0






