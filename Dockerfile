# Dockerfile

# Используем официальный образ Python в качестве базового
FROM python:3.11

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN apt-get update \
    && apt-get install -y mariadb-client netcat-openbsd

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install -r requirements.txt

# Копируем entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Запускаем линтеры
RUN flake8 myapp || true
RUN black --check myapp || true

# Указываем команду для запуска приложения
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]