"""
Using Jinja2 with Django 1.2
Taken from: https://gist.github.com/472309
Based on: http://djangosnippets.org/snippets/2063/

To use:
  * Add this template loader to settings: `TEMPLATE_LOADERS`
  * Add template dirs to settings: `JINJA2_TEMPLATE_DIRS`

If in template debug mode - we fire the template rendered signal, which allows
debugging the context with the debug toolbar.  Viewing source currently doesnt
work.

If you want {% url %} or {% csrf_token %} support I recommend grabbing them
from Coffin (http://github.com/dcramer/coffin/blob/master/coffin/template/defaulttags.py)
Note for namespaced urls you have to use quotes eg:
  {% url account:login %} => {% url "account:login" %}
"""

import jinja2
from django.template.loader import BaseLoader
from django.template import TemplateDoesNotExist, Origin
from django.core.context_processors import csrf as django_csrf
from django.core import urlresolvers
from django.conf import settings
from stacks.www import models
from stacks import constants

# Global functions
# -------------------------

def reverse_site_url(viewname, site, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    """Convenience function for URLs with a site prefix."""
    if kwargs:
        kwargs['site'] = site.short_name
    else:
        kwargs = {'site': site.short_name}
    return urlresolvers.reverse(viewname, urlconf, args, kwargs, prefix, current_app)

def csrf(request):
    """Generate a CSRF token."""
    return django_csrf(request)['csrf_token']

# Custom filters
# -------------------------

def pluralize(value, plural_suffix="s", singular_suffix=""):
    if len(value) == 1:
        return singular_suffix
    else:
        return plural_suffix


# Django/Jinja integration
# -------------------------

class Template(jinja2.Template):
    def render(self, context):
        # flatten the Django Context into a single dictionary.
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)
        
        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)
        
        return super(Template, self).render(context_dict)

class Loader(BaseLoader):
    """
    A file system loader for Jinja2.
    
    Requires the following setting `JINJA2_TEMPLATE_DIRS`
    """
    is_usable = True
    
    # Set up the jinja env and load any extensions you may have
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(settings.JINJA2_TEMPLATE_DIRS),
        extensions=()
    )
    env.template_class = Template
    
    # add global identifiers
    env.globals['url'] = urlresolvers.reverse
    env.globals['site_url'] = reverse_site_url
    env.globals['models'] = models
    env.globals['constants'] = constants
    env.globals['settings'] = settings
    env.globals['csrf'] = csrf

    # add custom filters
    env.filters['pluralize'] = pluralize

    def load_template(self, template_name, template_dirs=None):
        try:
            template = self.env.get_template(template_name)
            return template, template.filename
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)
