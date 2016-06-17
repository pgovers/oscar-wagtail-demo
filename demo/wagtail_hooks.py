from django.utils.html import format_html
from django.conf import settings
from django.core.urlresolvers import reverse

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="%(static_url)sdemo/css/'
        'admin-streamfield-styles.css">' % {'static_url': settings.STATIC_URL}
    )


@hooks.register('register_admin_menu_item')
def register_oscar_menu_item():
    return MenuItem(
        'Oscar dashboard', reverse('dashboard:index'),
        classnames='icon icon-redirect', order=10000
    )
