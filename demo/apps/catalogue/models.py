from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page


class Category(Page):
    """
    The Oscars Category as a Wagtail Page
    This works because they both use Treebeard
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        help_text=_("Category name")
    )

from oscar.apps.catalogue.models import *  # noqa
