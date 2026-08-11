# Django Stripe Checkout

## [Демо проекта](https://django-stripe-checkout-136t.onrender.com)

Приложение на Django с каталогом товаров, сессионными заказами и оплатой через Stripe Payment Intents.

## Возможности

* Каталог товаров
* Управление товарами через Django Admin:

  * создание;
  * редактирование;
  * удаление;
  * изменение цены и валюты
* Добавление товаров в заказ
* Увеличение количества товара
* Удаление товара из заказа
* Полное удаление заказа
* Подсчёт общей стоимости заказа
* Поддержка скидок и налогов
* Интеграция со Stripe Payment Intents
* Сохранение Stripe Payment Intent ID в заказе
* Отслеживание статуса заказа
* Docker
* Деплой на Render
* WhiteNoise для отдачи статических файлов

## Стек

* Python
* Django
* PostgreSQL
* Stripe
* JavaScript
* Docker
* Render
* WhiteNoise

## Docker

Приложение может запускаться через Docker.

Сборка:

```bash
docker compose build
```

Запуск:

```bash
docker compose up
```

При запуске контейнера выполняются необходимые команды инициализации:

```bash
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
```

Сервер будет доступен по адресу:

http://127.0.0.1:8000

Django Admin:

http://127.0.0.1:8000/admin/

## Запуск локально

### 1. Клонирование проекта

```bash
git clone https://github.com/mopuk/django-stripe-checkout
cd django-stripe-checkout
```

### 2. Создание виртуального окружения

Для Linux и macOS:

```bash
python -m venv venv
source venv/bin/activate
```

Для Windows:

```powershell
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Переменные окружения

Необходимо создать файл `.env` в корне проекта со следующими переменными:

```env
POSTGRES_USER=local_user
POSTGRES_PASSWORD=local_password
POSTGRES_DB=django_stripe_checkout
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

STRIPE_SECRET_KEY=<ваш ключ>
STRIPE_PUBLISHABLE_KEY=<ваш ключ>

DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_EMAIL=you@example.com
DJANGO_ADMIN_PASSWORD=<ваш пароль>
```

### 5. Миграции

```bash
python manage.py migrate
```

### 6. Создание администратора

За создание администратора отвечает Django management command:

```text
catalog/management/commands/create_admin.py
```

Команда создаёт администратора на основе переменных окружения:

```bash
python manage.py create_admin
```

Если пользователь с указанным username уже существует, новый пользователь не создаётся.

### 7. Запуск

```bash
python manage.py runserver
```

Сервер будет доступен по адресу:

http://127.0.0.1:8000

Django Admin:

http://127.0.0.1:8000/admin/
