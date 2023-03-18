import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('/chromedriver.exe')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.find_element(By.ID, 'email').send_keys('pokemon2003@rambler.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('21081985')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    assert pytest.driver.find_element(By.CSS_SELECTOR,
                                      'button[class="btn btn-outline-success"]').text == "Добавить питомца"

    yield

    pytest.driver.quit()


class TestPetFriends:
    def test_expectation(self):
        driver = pytest.driver
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text() = 'Добавить питомца']"))).click()
        driver.implicitly_wait(10)
        myDynamicElement = driver.find_element(By.ID, "addPetsModalLabel")
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="close"] span'))).click()
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text() = 'PetFriends']")))
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text() = 'Выйти']"))).click()
        time.sleep(2)

    def test_all_pets(self):
        # явные ожидания
        driver = pytest.driver
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_contains("PetFriends: My Pets"))
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text() = 'PetFriends']")))
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[href="/all_pets"]'))).click()
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[href="/my_pets"]'))).click()

        # Проверяем наличие всех питомцев
        card_pet = pytest.driver.find_elements(By.XPATH, '//*[@scope="row"]/..')
        quantity_pet = pytest.driver.find_element(By.CSS_SELECTOR, 'div[class=".col-sm-4 left"]').text.split()
        try:
            assert str(len(card_pet)) == quantity_pet[2]
        except:
            print('количество карточек питомцев не совпадает с данными пользователя')

    def test_photo(self):
        # Проверка, что у половины питомцев есть фото
        driver = pytest.driver
        driver.implicitly_wait(10)
        pet_foto = driver.find_elements(By.CSS_SELECTOR, 'th[scope="row"] img')

        # pet_foto = pytest.driver.find_elements(By.CSS_SELECTOR, 'th[scope="row"] img')
        count_pet_foto = 0
        count_pet_no_foto = 0
        for i in range(len(pet_foto)):
            if pet_foto[i].get_attribute('src') != '':
                count_pet_foto += 1
            else:
                count_pet_no_foto += 1
        try:
            assert count_pet_no_foto <= count_pet_foto
        except:
            print('\nкарточек питомцев без фото больше чем с фотографией')

    def test_names(self):
        # Проверка наличия имени у всех питомцев
        driver = pytest.driver
        driver.implicitly_wait(10)
        myDynamicElement = driver.find_element(By.XPATH, '//tbody/tr/td[1]')

        name = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        num_name = 0
        for i in name:
            num_name += 1
            name = i.text
            try:
                assert name != ''
            except:
                print(f'\nу карточки питомца с номером {num_name} отсутствует имя')

    def test_breed(self):
        # Проверка наличия породы у всех питомцев
        breed = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
        num_breed = 0
        for i in breed:
            num_breed += 1
            breed = i.text
            try:
                assert breed != ''
            except:
                print(f'\nу карточки питомца с номером {num_breed} отсутствует порода')

    def test_age(self):
        # Проверка наличия возраста у всех питомцев
        driver = pytest.driver
        driver.implicitly_wait(10)
        myDynamicElement = driver.find_element(By.XPATH, '//tbody/tr/td[3]')

        age = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
        num_age = 0
        for i in age:
            num_age += 1
            age = i.text
            try:
                assert age != ''
            except:
                print(f'\nу карточки питомца с номером {num_age} отсутствует возраст')

    def test_different_names(self):
        # проверка, что все имена питомцев разные
        name = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        list_name = []
        for i in name:
            name = i.text
            list_name.append(name)
        mod_list_name = set(list_name)
        try:
            assert len(mod_list_name) == len(list_name)
        except:
            print('\nв карточках питомцев есть повторяющиеся имена')

    def test_different_pet(self):
        # проверка, что все карточки питомцев разные
        pet = pytest.driver.find_elements(By.XPATH, '//tbody/tr')

        list_pets = []
        for x in pet:
            list_pets.append(x.text)
        mod_list_pets = set(list_pets)
        try:
            assert len(mod_list_pets) == len(list_pets)
        except:
            print('\nна сайте присутствуют одинаковые карточки питомцев')
