Oscar Wagtail demo project
==========================

**A Django recipe for integrating [Oscar E-commerce](http://oscarcommerce.com) into a [Wagtail CMS](http://wagtail.io) application.**

*We do __not__ recommend using this project to start your own site*. This recipe is only to provide some examples of implementing common features, it is not an exemplar of Django, Oscar or Wagtail best practice.

If you're reasonably new to Python/Django, we suggest you run this project on a Virtual Machine using Vagrant, which helps resolve common software dependency issues. However instructions to start this project without Vagrant follow below.

Setup with Vagrant
------------------

### Dependencies
* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant 1.5+](https://www.vagrantup.com)

### Installation
Run the following commands:

    git clone https://github.com/pgovers/oscar-wagtail-demo.git
    cd oscar-wagtail-demo
    vagrant up
    vagrant ssh
      (then, within the SSH session:)
    ./manage.py runserver 0.0.0.0:8000

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/), the Wagtail admin interface at [http://localhost:8000/admin/](http://localhost:8000/admin/) and the Oscar dashboard interface at [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/). Log into them with the credentials ``admin / changeme``.

Setup without Vagrant
-----
Don't want to set up a whole VM to try out Wagtail? No problem.

### Dependencies
* [PostgreSQL](https://www.postgresql.org) or [SQLite](https://www.sqlite.org/)
* [PIP](https://github.com/pypa/pip)

### Installation

With PostgreSQL running (and configured to allow you to connect as the 'postgres' user - if not, you'll need to adjust the `createdb` line and the database settings in wagtaildemo/settings/base.py accordingly), run the following commands:

    git clone https://github.com/pgovers/oscar-wagtail-demo.git
    cd oscar-wagtail-demo
    virtualenv .
    source bin/activate
    createdb -Upostgres oscarwagtaildemo
    make develop
    ./manage.py runserver

The `make develop` command combines:
* `make clean` cleaning any compiled Python files
* `make install` installing dependencies via `pip` package manager
* `make migrations` performing `./manage migrations` to perform database migrations
* `make fixtures` load both Wagtail and Oscar fixtures and perform `update_index`
* `make superuser` create superuser (you'll be prompted for username, e-mail address and password)

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/), the Wagtail admin interface at [http://localhost:8000/admin/](http://localhost:8000/admin/) and the Oscar dashboard interface at [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/). Log into them with the credentials inserted in earlier step.

### SQLite support

SQLite is supported as an alternative to PostgreSQL - update the `DATABASES` setting in wagtaildemo/settings/base.py to use `'django.db.backends.sqlite3'` and set `NAME` to be the full path of your database file, as you would with a regular Django project.
