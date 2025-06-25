run:
	python manage.py runserver

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

celery:
	celery -A book_api worker -l info
