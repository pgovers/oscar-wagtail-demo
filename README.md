# Oscar Wagtail Demo

**A Django recipe for integration Wagtail into an Oscar application.**

This demo shows you how to run an Oscar e-commerce application in parallel with Wagtail. Both admin interfaces are
used. We keep the Oscar admin as is to manage your products. We bring in products and categories into Wagtail
to be able to create some editorial content.

This demo shows you:

    - How to add Oscar to an existing Wagtail site
    - CRUD Oscar Categories in Wagtail
    - Disable editing Categories in Oscar
    - Product block stream field
    - Category block stream field



# Prerequisites

A Wagtail site.


# Initial skeleton

To keep it simple we show you here the minimal steps required to get up and running.

Add Oscar to your `requirements.txt`. We use the latest Oscar 1.2.x

    oscar>=1.2,<1.3


Add Oscar to your settings, in base.py import Oscar:

    from oscar.defaults import *  # noqa
    from oscar import get_core_apps


Oscar needs to have the Django sites framework enabled. Add `django.contrib.sites`to `INSTALLED_APPS` and add a
`SITE_ID`. Oscar core aps are with `get_core_apps()`:

    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        ...
    ] + get_core_apps()


Configure the `OSCAR_IMAGE_FOLDER`.

    OSCAR_IMAGE_FOLDER = os.path.join(MEDIA_FOLDER, 'oscar_images')


Add `HAYSTACK_CONNECTIONS` needed by the search feature in the Oscar admin:


    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }


Note: We ignore all other Oscar settings/features to keep this demo simple. Consult the Oscar documentation
for additional settings:

    http://django-oscar.readthedocs.io/en/latest/internals/getting_started.html


# Admin routes

Add routes in `urls.py`:

    from oscar.app import application

    urlpatterns = [
        url(r'^i18n/', include('django.conf.urls.i18n')),
        url(r'', include(application.urls)),
        ...
    ]


# Categories in Wagtail


# Disable editing categories in Oscar admin


# Product block stream field


# Category block stream field


# Category landing page

