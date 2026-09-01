import requests
import config


# 1. Получаем список всех существующих задач
response = requests.get(f"{config.BASE_URL}/tasks")
                        
tasks = response.json()

# 2. В цикле удаляем каждую задачу по её ID
for task in tasks:
    task_id = task["id"]
    del_res = requests.delete(f"{config.BASE_URL}/tasks/{task_id}")
    print(f"Задача ID {task_id} удалена: {del_res.status_code}")

print("Очистка базы завершена!")
