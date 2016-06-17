# Oscar Wagtail Demo

**A Django recipe for integrating Wagtail into an Oscar application.**

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


Install the requirements

    $ pip install -r requirements.txt


Add Oscar to your settings, in base.py import Oscar:

    from oscar.defaults import *  # noqa
    from oscar import get_core_apps


Oscar needs to have the Django sites framework enabled. Add `django.contrib.sites`to `INSTALLED_APPS` and add a
`SITE_ID`. Oscar core apps are with `get_core_apps()`:

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


# Oscar Categories in Wagtail

The Oscar Category and Wagtail Page look alike. We fork of the Oscar catalogue app into our project with:

    $ python manage.py oscar_fork_app catalogue demo/apps/


Now we create the Category Page model. In `demo/apps/catalogue/models.py` add:

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

Most methods are copied from the original Oscar Category class. We hightlight the once we needed to customize a
little more.


When Oscar requests the products for the search feature it calls `get_contect`. Here we add `category`
and search context to the context object. This allowes the Oscar search handler to get all Products on
the CategoryPage:


    def get_context(self, request, *args, **kwargs):
        self.search_handler = self.get_search_handler(
            request.GET, request.get_full_path(), self.get_categories())
        context = super(Category, self).get_context(request, *args, **kwargs)
        context['category'] = self
        search_context = self.search_handler.get_search_context_data('products')
        context.update(search_context)
        return context


Oscar has a field called `name` where Wagtail has `title`. In the save method we make sure both values
exist and are equal. This ensures that both Oscar and Wagtail work without further patching name/title related code.


    def save(self, *args, **kwargs):
        ...

        # Set title and name
        if self.name and not self.title:
            self.title = self.name
        else:
            self.name = self.title

        ...


# Oscar routes

Add routes in `urls.py`:

    from oscar.app import application

    urlpatterns = [
        url(r'^i18n/', include('django.conf.urls.i18n')),
        url(r'', include(application.urls)),
        ...
    ]


# ProductBlock StreamField

Oscar uses dynamic class loading. Dynamic class loading makes Oscar extensively customisable. We want to reference
an Oscar Product class from Wagtail. But it is not available when the vanilla Django model loader initializes the
Wagtail models.

To get a reference to the Oscar Product class from Wagtail we need to use a StreamField and a custom ChooserBlock.

Here the ProductChooserBlock loads Products with `get_model('catalogue', 'product')` on runtime.


    # oscar-wagtail-demo/demo/apps/catalogue/blocks.py

    from django.utils.functional import cached_property
    from oscar.core.loading import get_model
    ...


    class ProductChooserBlock(blocks.ChooserBlock):
        @cached_property
        def target_model(self):
            return get_model('catalogue', 'product')

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


# Category block stream field


# Category landing page

