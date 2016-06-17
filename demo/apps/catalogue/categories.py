from wagtail.wagtailcore.models import Page
from demo.apps.catalogue.models import Category


def create_from_sequence(bits):
    """
    Create categories from an iterable
    """
    if len(bits) == 1:
        # Get or create root node
        name = bits[0]
        try:
            # Category names should be unique at the depth=2
            root = Category.get_root_nodes().get(title=name)
        except Category.DoesNotExist:
            root = Category.add_root(title=name)
        except Category.MultipleObjectsReturned:
            raise ValueError((
                "There are more than one categories with name "
                "%s at depth=1") % name)
        return [root]
    else:
        parents = create_from_sequence(bits[:-1])
        parent, name = parents[-1], bits[-1]

        try:
            child = parent.get_children().get(title=name)
        except (Page.DoesNotExist, Category.DoesNotExist):
            child = parent.add_child(title=name)
        except Category.MultipleObjectsReturned:
            raise ValueError((
                "There are more than one categories with name "
                "%s which are children of %s") % (name, parent))

        parents.append(child)
        return parents


def create_from_breadcrumbs(breadcrumb_str, separator='>'):
    """
    Create categories from a breadcrumb string
    """
    category_names = [x.strip() for x in breadcrumb_str.split(separator)]
    categories = create_from_sequence(category_names)
    return categories[-1]
