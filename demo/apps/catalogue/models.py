from django.db import models
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

    def generate_slug(self):
        """
        Generates a slug for a category. This makes no attempt at generating
        a unique slug.
        """
        return slugify(self.name)

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
