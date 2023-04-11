# Бэкенд магазина
## Технологии
Python 3.10, Django Rest Framework, Djoser, Docker, PostgreSQL, drf-yasg

## Локальный запуск проекта  
Для запуска подойдёт Docker 20.10.21, Docker Compose 2.12.2.  
Клонируйте репозиторий:  
```
git clone git@github.com:ElenaChuvasheva/store.git
```
Перейдите в папку store/:
```
cd store/
```
Создайте в этой папке файл .env, примеры значений:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-%!qw$+ma=z6o(a84216y-y7f0=%fp0gqm5vfhbr1wd0^e%y3&w
```
Запустите команду:
```
docker-compose up
```
Выполните команду сборки статики:
```
docker-compose exec web python manage.py collectstatic
```
Выполните команду применения миграций:
```
docker-compose exec web python manage.py migrate
```
Загрузите фикстуры:
```
docker-compose exec web python manage.py loaddata fixtures.json
```

## Примеры запросов
/redoc - автоматически сгенерированная документация API
/for_staff_only - админка
В тестовой базе данных суперпользователь admin, email a@a.ru, пароль admin. Пароли остальных пользователей qwerty123@

/api/categories - получить список категорий
/api/products - получить список всех продуктов. Доступна фильтрация по id категории и подкатегории, поиск по названию продукта.
