# My Django Project

## Описание

Этот проект представляет собой Django-приложение с поддержкой базы данных MySQL, развертываемое с использованием Docker и Docker Compose. Также в проект включены линтеры `flake8` и `black` для проверки качества кода.

## Требования

Перед началом убедитесь, что у вас установлены следующие компоненты:

- Docker: [Установка Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Установка Docker Compose](https://docs.docker.com/compose/install/)

## Установка

1. Клонируйте репозиторий:
- git clone https://github.com/kuznik27/simple_dj_server
- cd simple_dj_server

2. Постройте и запустите контейнеры:
- docker-compose up --build

## Использование линтеров

Для запуска линтеров используйте следующую команду:
- docker-compose run --rm lint

## Тестирование

Для тестирования используется pytest. Вы можете запустить тесты с помощью следующей команды:
- docker-compose run --rm web pytest

## Дополнительные команды

1.	Применение миграций:
- docker-compose run --rm web python manage.py migrate

2.	Создание суперпользователя:	
- docker-compose run --rm web python manage.py createsuperuser

3.	Сборка статических файлов:
- docker-compose run --rm web python manage.py collectstatic --noinput
