#!/bin/bash

PROJECT_NAME="oscarwagtaildemo"

PROJECT_DIR=/home/vagrant/oscar-wagtail-demo
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


# Create database
su - vagrant -c "createdb $PROJECT_NAME"


# Virtualenv setup for project
su - vagrant -c "pyvenv $VIRTUALENV_DIR"
# Replace previous line with this if you are using Python 2
# su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR"

su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"


# Install PIP requirements
su - vagrant -c "$PIP install -r $PROJECT_DIR/requirements.txt -f /home/vagrant/wheelhouse"


# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py


# Run database migrations
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput"

# Load initial Wagtail data
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py load_initial_data"

# Import Oscar fixtures
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py loaddata demo/fixtures/catalogue/child_products.json && \
                 $PYTHON $PROJECT_DIR/manage.py oscar_import_catalogue demo/fixtures/catalogue/*.csv && \
                 $PYTHON $PROJECT_DIR/manage.py oscar_import_catalogue_images demo/fixtures/catalogue/images.tar.gz && \
                 $PYTHON $PROJECT_DIR/manage.py oscar_populate_countries && \
                 $PYTHON $PROJECT_DIR/manage.py loaddata demo/fixtures/pages.json demo/fixtures/auth.json demo/fixtures/ranges.json demo/fixtures/offers.json \
                 $PYTHON $PROJECT_DIR/manage.py loaddata demo/fixtures/orders.json"

su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py clear_index --noinput && \
                 $PYTHON $PROJECT_DIR/manage.py update_index"


# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PYTHONPATH=$PROJECT_DIR
export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev

alias dj="django-admin"
alias djrun="dj runserver 0.0.0.0:8000"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF
