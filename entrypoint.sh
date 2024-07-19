#!/bin/sh

# Ждем, пока база данных станет доступной
echo "Waiting for MySQL..."

while ! nc -z db 3306; do
  sleep 1
done

echo "MySQL started"

# Применяем миграции и собираем статические файлы
python manage.py makemigrations
python manage.py migrate
#python manage.py collectstatic --noinput

# Создаем суперпользователя, если он не существует
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists()"; then
        echo "Creating superuser $DJANGO_SUPERUSER_USERNAME"
        python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"
    else
        echo "Superuser $DJANGO_SUPERUSER_USERNAME already exists"
    fi
fi

# Запускаем сервер
exec "$@"