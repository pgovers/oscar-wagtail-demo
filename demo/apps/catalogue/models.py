from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from oscar.core.utils import slugify
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class Category(Page):
    """
    The Oscars Category as a Wagtail Page
    This works because they both use Treebeard
    """
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full'),
        ImageChooserPanel('image')
    ]

    @classmethod
    def add_root(cls, **kwargs):
        """
        Adds a Catalogue page node to Wagtail's tree root node. Note that this
        isn't at depth=1 as that's Wagtail's root.
        """
        node = Category.objects.filter(depth=1).first()
        return node.add_child(**kwargs)

    @classmethod
    def get_root_nodes(cls):
        """
        :returns: A queryset containing the root nodes in the tree. This
        differs from the default implementation to find category page root
        nodes by `content_type`.
        """
        content_type = ContentType.objects.get_for_model(cls)
        depth = (cls.objects.filter(content_type=content_type).aggregate(
            depth=models.Min('depth')))['depth']

        if depth is not None:
            return cls.objects.filter(content_type=content_type, depth=depth)

        return cls.objects.filter(content_type=content_type)

    def generate_slug(self):
        """
        Generates a slug for a category. This makes no attempt at generating
        a unique slug.
        """
        return slugify(self.name)

    def get_categories(self):
        """
        Return a list of the current category and its ancestors
        """
        return list(self.get_descendants()) + [self]

    @classmethod
    def get_tree(self, parent = None):
        return self.objects.all()

    def get_absolute_url(self):
        return self.url

    def get_search_handler(self, *args, **kwargs):
        from oscar.apps.catalogue.search_handlers import get_product_search_handler_class
        return get_product_search_handler_class()(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        self.search_handler = self.get_search_handler(
            request.GET, request.get_full_path(), self.get_categories())
        context = super(Category, self).get_context(request, *args, **kwargs)
        context['category'] = self
        search_context = self.search_handler.get_search_context_data('products')
        context.update(search_context)
        return context

    def ensure_slug_uniqueness(self):
        """
        Ensures that the category's slug is unique amongst it's siblings.
        This is inefficient and probably not thread-safe.
        """
        unique_slug = self.slug
        siblings = self.get_siblings().exclude(pk=self.pk)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        """
        Oscar traditionally auto-generated slugs from names. As that is
        often convenient, we still do so if `slug` is not supplied through
        other means. Also, Wagtail's Page requires `title` where Oscar requires
        `name`. Therefore we set `title` as `name` if `name` but no `title`
         supplied, else set `name` as `title`.
        """

        # Set title and name
        if self.name and not self.title:
            self.title = self.name
        else:
            self.name = self.title

        # Set slug if not supplied
        if self.slug:
            super(Category, self).save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            super(Category, self).save(*args, **kwargs)
            # We auto-generated a slug, so we need to make sure that it's
            # unique. As we need to be able to inspect the category's siblings
            # for that, we need to wait until the instance is saved. We
            # update the slug and save again if necessary.
            self.ensure_slug_uniqueness()


from oscar.apps.catalogue.models import *  # noqa
