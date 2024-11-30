#!/bin/sh


if [ "$DATABASE" = "postgres" ]

then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done
    
    echo "POSTGRESQL started"
fi

chown -R app:app /home/app/web/staticfiles /home/app/web/mediafiles

python manage.py collectstatic --no-input
python manage.py migrate

exec "$@"