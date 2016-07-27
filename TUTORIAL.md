# Oscar Wagtail Tutorial

**Integrating [Oscar E-commerce](http://oscarcommerce.com) into a [Wagtail CMS](http://wagtail.io) application.**

This tutorial shows you how to run an Oscar E-commerce application in parallel with Wagtail CMS. Both admin interfaces are used. We keep the Oscar admin unchanged. We bring `Categories` into Wagtail to be able to create editorial content.

This demo shows you:

  - How to add Oscar to an existing Wagtail site
  - CRUD Oscar Categories in Wagtail
  - Select Products in Wagtail's streamfields.


# Prerequisites

A Wagtail site.


# Initial skeleton

To keep it simple we show you here the minimal steps required to get up and running.

Add Oscar to your `requirements.txt`. We use the latest Oscar 1.2.x. As Oscar currently lacks support for Django 1.9 or above we pin down Django to 1.8.x.

    Django>=1.8,<1.9
    django-oscar>=1.2,<1.3


Install the requirements

    virtualenv .
    source bin/activate
    $ pip install -r requirements.txt


Add Oscar to your settings, in `wagtaildemo/settings/base.py` import Oscar:

    from oscar.defaults import *  # noqa
    from oscar import get_core_apps


Oscar needs to have the Django sites framework enabled, therefore add `django.contrib.sites` to `INSTALLED_APPS` and include Oscar's core apps with `get_core_apps()`:

    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        ...
    ] + get_core_apps()


Oscar utilizes [Haystack](http://haystacksearch.org/) for search indexing. Add `HAYSTACK_CONNECTIONS`:


    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }


Note: We ignore all other Oscar settings/features to keep this demo simple. Consult the Oscar documentation for additional settings:

    http://django-oscar.readthedocs.io/en/latest/internals/getting_started.html


# Oscar routes

Add routes in `urls.py`:

    from oscar.app import application

    urlpatterns = [
        url(r'^i18n/', include('django.conf.urls.i18n')),
        url(r'', include(application.urls)),
        ...
    ]


# Oscar Categories in Wagtail

The Oscar `Category` and Wagtail `Page` share the same tree structure implementation due to both utilizing [Django Treebeard](https://tabo.pe/projects/django-treebeard). We fork the Oscar catalogue app into our project with:

    $ python manage.py oscar_fork_app catalogue demo/apps/


Now we create the Category model extending from Wagtail's Page. In `demo/apps/catalogue/models.py` add:

    ...
    from django.db import models

    from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
    from wagtail.wagtailcore.fields import StreamField
    from wagtail.wagtailcore.models import Page
    from wagtail.wagtailcore import blocks
    from wagtail.wagtailimages.blocks import ImageChooserBlock
    ...

    class Category(Page):
        """
        The Oscars Category as a Wagtail Page
        This works because they both use Treebeard
        """
        template = "catalogue/categorypage.html"
        name = models.CharField(_('Name'), max_length=255, db_index=True)
        description = models.TextField(_('Description'), blank=True)
        image = models.ForeignKey(
            'wagtailimages.Image',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
        )
        body = StreamField([
            ('heading', blocks.CharBlock(classname="full title")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('product_block', ProductBlock()),
        ])

        content_panels = Page.content_panels + [
            FieldPanel('description', classname='full'),
            ImageChooserPanel('image'),
            StreamFieldPanel('body'),
        ]

    ...


Run `makemigrations` and `migrate` to let your database reflect the changes:

    $ python manage.py makemigrations
    $ python manage.py migrate


# Supply additional Oscar Category methods


The Oscar machinery needs some extra methods on the new Category class for the navigation to work.

Most methods are copied from the original Oscar Category class. Here we show you the methods we need to customize a little more.


When Oscar requests the products for the search feature it calls `get_context`. Here we add `category` and search context to the context object. This allows the Oscar search handler to get all Products on the CategoryPage:


    def get_context(self, request, *args, **kwargs):
        self.search_handler = self.get_search_handler(
            request.GET, request.get_full_path(), self.get_categories())
        context = super(Category, self).get_context(request, *args, **kwargs)
        context['category'] = self
        search_context = self.search_handler.get_search_context_data('products')
        context.update(search_context)
        return context


Oscar has a field called `name` where Wagtail has `title`. In the save method we make sure both values exist and are equal. This ensures that both Oscar and Wagtail work without further patching name/title related code.


    def save(self, *args, **kwargs):
        ...

        # Set title and name
        if self.name and not self.title:
            self.title = self.name
        else:
            self.name = self.title

        ...


# ProductBlock StreamField

Oscar uses dynamic class loading. Dynamic class loading makes Oscar extensively customisable. We want to reference an Oscar Product class from Wagtail. But it is not available when the vanilla Django model loader initializes the Wagtail models.

To get a reference to the Oscar Product class from Wagtail we need to use a StreamField and a custom ChooserBlock.

Here the ProductChooserBlock loads Products with `get_model('catalogue', 'Product')` on runtime:


    # oscar-wagtail-demo/demo/apps/catalogue/blocks.py

    from django.utils.functional import cached_property
    from oscar.core.loading import get_model
    ...


    class ProductChooserBlock(blocks.ChooserBlock):
        @cached_property
        def target_model(self):
            return get_model('catalogue', 'Product')

        widget = forms.Select

        class Meta:
            app_label = 'catalogue'

        def value_for_form(self, value):
            # return the key value for the select field
            if isinstance(value, self.target_model):
                return value.pk
            else:
                return value


    class ProductBlock(blocks.StructBlock):
        ...
        products = blocks.ListBlock(ProductChooserBlock)
