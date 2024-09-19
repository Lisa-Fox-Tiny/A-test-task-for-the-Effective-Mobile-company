from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Данные для авторизации
LOGIN = "standard_user"
PASSWORD = "secret_sauce"
URL = "https://www.saucedemo.com/"


# Настройка браузера (В данном случае используется Chrome)
def setup_browser():
    options = webdriver.ChromeOptions()
    # Укажите путь к Opera GX

    # Устанавливаем нужный драйвер
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# Тест на покупку товара
def test_purchase():
    driver = setup_browser()

    try:
        # Открыть сайт
        driver.get(URL)

        # Авторизация
        driver.find_element(By.ID, "user-name").send_keys(LOGIN)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()

        # Подождать, пока страница загрузится и будет виден товар
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )

        # Добавление товара в корзину (например, "Sauce Labs Backpack")
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        # Переход в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Проверка, что товар добавлен в корзину
        cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        assert cart_item.text == "Sauce Labs Backpack", "Товар не был добавлен в корзину!"

        # Оформление заказа
        driver.find_element(By.ID, "checkout").click()

        # Заполнение данных для оформления
        driver.find_element(By.ID, "first-name").send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        # Подтверждение заказа
        driver.find_element(By.ID, "finish").click()

        # Добавляем ожидание для появления сообщения о завершении заказа
        confirmation_message_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )

        # Выводим сообщение для проверки
        confirmation_message = confirmation_message_element.text
        print(f"Текст подтверждения: {confirmation_message}")

        # Проверяем сообщение
        assert confirmation_message.lower() == "thank you for your order!".lower(), f"Ожидалось: 'THANK YOU FOR YOUR ORDER', но получено: '{confirmation_message}'"

        print("Тест пройден успешно! Покупка завершена.")

    finally:
        # Закрытие браузера
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    test_purchase()