# cd /venv/
# /venv/bin/python manage.py makemigrations
# /venv/bin/python manage.py migrate

# if [ -z "${API_URL}" ]
# then
#   echo "API_URL is empty"
# else
#   echo "API_URL: ${API_URL}"
# fi

# /venv/bin/python manage.py runserver 0.0.0.0:8000

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 config.wsgi:application
