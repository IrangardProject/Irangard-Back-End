web: gunicorn --chdir /app/Irangard Irangard.wsgi:application --log-file - --log-level debug
release: python --chdir /app/Irangard manage.py migrate

