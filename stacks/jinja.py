from crimpyutils.django_jinja import Loader
from django.core import urlresolvers
from stacks.www import models
from stacks import constants

def reverse_site_url(viewname, site, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    """Convenience function for URLs with a site prefix."""
    if kwargs:
        kwargs['site'] = site.short_name
    else:
        kwargs = {'site': site.short_name}
    return urlresolvers.reverse(viewname, urlconf, args, kwargs, prefix, current_app)

class StacksLoader(Loader):
    def more_globals(self):
        return {
            'models': models,
            'constants': constants,
            'site_url': reverse_site_url,
        }