# These targets are not files
.PHONY: install migrations fixtures createsuperuser clean develop

install:
	pip install -r requirements.txt

migrations:
	# Migrate database
	./manage.py migrate

fixtures:
	# Load initial Wagtail data
	./manage.py load_initial_data
	# Load initial Oscar data
	./manage.py load_oscar_data
	# Update Haystack index
	./manage.py clear_index --noinput
	./manage.py update_index

superuser:
	./manage.py createsuperuser

clean:
	# Delete compiled Python files
	find . -type f -name "*.pyc" -delete

develop: clean install migrations fixtures superuser
