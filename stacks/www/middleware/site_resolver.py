from django.http import Http404
from stacks.www.models import Site
from stacks import constants

class SiteResolverMiddleware(object):
    """Figure out which site the request is for based on domain."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'site' in view_kwargs:
            try:
                site = Site.get_from_cache(short_name=view_kwargs['site'])
            except:
                raise Http404

            # remove this kwarg for convenience
            del view_kwargs['site']

        else:
            site = Site.get_from_cache(id=constants.HOME_SITE_ID)

        request.site = site