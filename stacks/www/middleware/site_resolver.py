from django.http import Http404
from django.contrib.sites.models import RequestSite
from stacks.www.models.site import Site

class SiteResolverMiddleware(object):
    "Figure out which site the request is for based on domain."

    def process_view(self, request, view_func, view_args, view_kwargs):
        request_site = RequestSite(request)
        domain = request_site.domain

        try:
            site = Site.get_from_cache(domain=domain)
        except:
            raise Http404

        request.site = site