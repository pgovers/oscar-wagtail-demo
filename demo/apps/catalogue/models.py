from wagtail.wagtailcore.models import Page


class Category(Page):
    """
    The Oscars Category as a Wagtail Page
    This works because they both use Treebeard
    """

    @property
    def name(self):
        return self.title

from oscar.apps.catalogue.models import *  # noqa
