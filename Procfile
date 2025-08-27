web: gunicorn graphic_design_hub.wsgi:application
release: python manage.py migrate && python manage.py collectstatic --noinput