from django.conf.urls import include, url

from oscar.app import Shop


class OscarApplication(Shop):

    def get_urls(self):
        """
        Override the default get_urls() method to move default Oscar promotions
        from location r'' to r'^promotions/' to free up space for Wagtail's
        wagtailcore serving mechanism.
        """
        urls = super(OscarApplication, self).get_urls()[:-1]
        urls.append(url(r'^promotions/', include(self.promotions_app.urls)),)
        return urls


oscar_urls = OscarApplication().urls
