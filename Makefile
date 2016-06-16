# These targets are not files
.PHONY: install migrations fixtures createsuperuser clean develop

install:
	cd wagtaildemo
	pip install -e . -r requirements.txt

migrations:
	# Migrate database
	./manage.py migrate

fixtures:
	# Load initial Wagtail data
	./manage.py load_initial_data
	# Import Oscar fixtures
	./manage.py loaddata demo/fixtures/catalogue/child_products.json
	./manage.py oscar_import_catalogue demo/fixtures/catalogue/*.csv
	./manage.py oscar_import_catalogue_images demo/fixtures/catalogue/images.tar.gz
	./manage.py oscar_populate_countries
	./manage.py loaddata demo/fixtures/pages.json demo/fixtures/auth.json demo/fixtures/ranges.json demo/fixtures/offers.json
	./manage.py loaddata demo/fixtures/orders.json
	# Update Oscar index
	./manage.py clear_index --noinput
	./manage.py update_index catalogue

createsuperuser:
	./manage.py createsuperuser

clean:
	# Delete compiled Python files
	find . -type f -name "*.pyc" -delete

develop: clean install migrations fixtures createsuperuser
