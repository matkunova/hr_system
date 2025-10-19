# Система учёта работников компании

Внутренняя HR-система для ведения учёта сотрудников: добавление, просмотр, обновление, управление статусами, импорт из Excel.
Реализована на Django 4.2 + DRF с REST API и админ-панелью.

## Технологии

Python 3.10+
Django 4.2 (LTS)
Django REST Framework
Poetry
SQLite
openpyxl

## Запуск проекта

1. Клонировать репозиторий
```
git clone https://github.com/matkunova/hr-system.git
cd hr-system
```
2. Установить зависимости через Poetry
```
poetry install
```
3. Активировать виртуальное окружение
```
eval "$(poetry env activate)"
```
4. Выполнить миграции
```
python3 manage.py migrate
```
5. Создать суперпользователя
```
python3 manage.py createsuperuser
```
6. Запустить сервер
```
python manage.py runserver
```
Сервер будет доступен по адресу: http://127.0.0.1:8000

## Пользователи и роли

В системе две роли:
- Обычный пользователь (is_staff = False) — только чтение через API (GET /api/workers/)
- Администратор (is_staff = True) — полный доступ: CRUD через API и полный контроль в админке

Создание пользователей:
Администратор создаётся командой createsuperuser. Действующий администратор может наделять админскими правами любого пользователя через админку.
Обычного пользователя можно создать через админку: раздел «Пользователи» → «Добавить пользователя», сняв флажок «Статус персонала».

## Аутентификация в API
Система использует токены (TokenAuthentication).

Получение токена:
Через админку: раздел «Токены» → «Добавить токен», выбрать пользователя.
Или через shell:
```
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
token, _ = Token.objects.get_or_create(user=user)
print(token.key)
```
Использование в запросах:
Добавить в заголовок:
Authorization: Token ваш_токен_здесь

## Импорт работников из Excel

Эндпоинт:
POST /api/workers/import/

Требования к файлу:
Формат: .xlsx
Обязательные столбцы: first_name, last_name, email, position
Опционально: middle_name
Пример: sample_import.xlsx

Как протестировать:
Использовать файл sample_import.xlsx из корня проекта.
Отправить POST-запрос, например, через curl:
```
curl -X POST http://127.0.0.1:8000/api/workers/import/
-H "Authorization: Token ваш_токен_админа"
-F "file=@sample_import.xlsx"
```
Успешный ответ:
```
{
"success_count": 3,
"errors": []
}
```
Импорт доступен только администраторам.

## Тесты

Запуск тестов:
pytest

Покрыта ключевая функциональность:

Модель Worker (уникальность email, обязательные поля)
Права доступа (обычный пользователь vs админ)
Импорт из Excel (валидный файл, дубликаты, ошибки)

## Структура проекта
hr-system/
├── hr_system/ # Настройки Django
├── workers/ # Приложение учёта работников
├── sample_import.xlsx # Шаблон для импорта
├── pyproject.toml # Зависимости (Poetry)
├── poetry.lock
└── README.md
