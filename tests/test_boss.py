from schemas import TaskSchema
import config
import pytest
import requests
# import clear_t

url=config.BASE_URL
password=config.ADMIN_PASSWORD
name = config.ADMIN_USERNAME


@pytest.fixture(scope="module")
def test_setup():
    session= requests.session()
    login_user= {
        "password": password,
        "username": name
    }
    responce=session.post(f"{url}/login", json = login_user, timeout = config.TIMEOUT)
    assert responce.status_code == 200


    role = responce.json()["user"]["role"]

    session.headers.update({"x-user-role": role})

    yield session

    session.close()

def test_title_task(test_setup):
    # Генерируем данные НА ЛЕТУ, прямо внутри теста!
    random_title = config.fake.sentence(nb_words=3)
    random_text = config.fake.text(max_nb_chars=50)

    config.logger.info(f"Сгенерированы данные задачи. Название: '{random_title}', Описание: '{random_text}'")

    text_title = {
        "title": random_title,
        "description": random_text
    }

    config.logger.info(f"Отправка POST-запроса на создание задачи по адресу: {url}/tasks")


    response = test_setup.post(f"{url}/tasks", json=text_title, timeout=config.TIMEOUT)

    config.logger.info(f"Получен ответ от сервера. Статус-код: {response.status_code}")
    config.logger.info(f"Тело ответа сервера (JSON): {response.text}")

    assert response.status_code == 201

    info_response = response.json()
    # Проверяем динамические переменные, которые создались в этой итерации
    assert info_response["title"] == random_title
    assert info_response["description"] == random_text

    try:
        TaskSchema(**response.json())
    except Exception as e:
        pytest.fail(f"Ответ сервера не соответствует схеме API! Ошибка: {e}")


def test_get_single_task_by_id(test_setup):

    random_title = config.fake.sentence(nb_words=2)

    text_title = {
            "title": random_title
    }

    responce = test_setup.post(f"{url}/tasks", json=text_title , timeout=config.TIMEOUT)
    assert responce.status_code == 201

    created_id= responce.json()["id"]
    config.logger.info(f"Создана базовая задача для теста GET по ID. Присвоен ID: {created_id}")
    config.logger.info(f"Отправка GET-запроса по ID на адрес: {url}/tasks/{created_id}")

    response_get=test_setup.get(f"{url}/tasks/{created_id}", timeout=config.TIMEOUT)

    config.logger.info(f'Получен ответ карточки задачи. Статус-код: {response_get.status_code}')
    config.logger.info(f"Тело ответа карточки задачи: {response_get.text}")
    assert response_get.status_code == 200
    task_data=response_get.json()
    assert task_data["id"] == created_id
    assert task_data["title"] == random_title



    try:
        TaskSchema(**task_data)
        config.logger.info("JSON-контракт карточки задачи успешно проверен через Pydantic!")
    except Exception as e:
        config.logger.error(f"Ошибка валидации карточки задачи: {e}")
        pytest.fail(f"Схема карточки задачи нарушена! Ошибка: {e}")