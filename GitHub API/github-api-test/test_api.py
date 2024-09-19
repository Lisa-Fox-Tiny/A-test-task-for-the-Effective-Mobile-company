import os
import time
import requests
import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получение данных из переменных окружения
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

# Уникальное имя для репозитория
def generate_unique_repo_name(base_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base_name}-{timestamp}"

REPO_NAME = generate_unique_repo_name("test-repo")

# Заголовки для аутентификации
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_repo():
    """Создание нового репозитория на GitHub"""
    url = f"{BASE_URL}/user/repos"
    data = {
        "name": REPO_NAME,
        "description": "Тестовый репозиторий",
        "private": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Репозиторий '{REPO_NAME}' успешно создан.")
        return True
    else:
        print(f"Ошибка при создании репозитория: {response.json()}")
        return False

def check_repo_exists():
    """Проверка наличия репозитория в списке репозиториев пользователя"""
    url = f"{BASE_URL}/user/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = [repo['name'] for repo in response.json()]
        if REPO_NAME in repos:
            print(f"Репозиторий '{REPO_NAME}' уже существует.")
            return True
        else:
            print(f"Репозиторий '{REPO_NAME}' не найден.")
            return False
    else:
        print(f"Ошибка при проверке репозиториев: {response.json()}")
        return False

def delete_repo():
    """Удаление репозитория"""
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Репозиторий '{REPO_NAME}' успешно удалён.")
    else:
        print(f"Ошибка при удалении репозитория: {response.json()}")

if __name__ == "__main__":
    # Шаг 1: Проверяем, существует ли репозиторий
    if not check_repo_exists():
        # Шаг 2: Создаем новый репозиторий
        if create_repo():
            # Подождем немного перед проверкой
            time.sleep(5)
            # Шаг 3: Удаляем репозиторий
            delete_repo()