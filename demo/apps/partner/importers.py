from oscar.apps.partner.importers import CatalogueImporter as BaseImporter
from oscar.core.loading import get_classes

from demo.apps.catalogue.categories import create_from_breadcrumbs
from demo.apps.catalogue.models import Category

ProductClass, Product, ProductCategory = get_classes(
    'catalogue.models', ('ProductClass', 'Product', 'ProductCategory'))


class CatalogueImporter(BaseImporter):

    def _create_item(self, product_class, category_str, upc, title,
                     description, stats):
        # Ignore any entries that are NULL
        if description == 'NULL':
            description = ''

        # Create item class and item
        product_class, __ \
            = ProductClass.objects.get_or_create(name=product_class)
        try:
            item = Product.objects.get(upc=upc)
            stats['updated_items'] += 1
        except Product.DoesNotExist:
            item = Product()
            stats['new_items'] += 1
        item.upc = upc
        item.title = title
        item.description = description
        item.product_class = product_class
        item.save()

        # Category
        category = create_from_breadcrumbs(category_str)
        try:
            ProductCategory.objects.create(product=item, category=category)
        except ValueError:
            object = Category.objects.filter(pk=category.pk).first()
            if object:
                ProductCategory.objects.get_or_create(
                    product=item, category=object
                )

        return item
