import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

from django.contrib.sites.models import RequestSite

app_url = re.compile(r'^/account/\w+/app/[\w.]+/\w+/(?P<component_path>(\w|\.)+)/.*')

class SiteResolverMiddleware(object):
    "Figure out which site the request is for based on domain."

    def process_view(self, request, view_func, view_args, view_kwargs):
        request_site = RequestSite(request)

        d = request_site.domain
        n = request_site.name


        # # first ensure this is an app-framework request
        # m = app_url.match(request.get_full_path())
        # if m:
        #     # store & elide account_code
        #     request.account_code = request.session['account_code'] = view_kwargs['account_code']
        #     del view_kwargs['account_code']
        #     # elide app_name, not needed
        #     del view_kwargs['app_name']
        #     # use app_code to drop app object into request & elide arg
        #     try:
        #         request.app = App.objects.get(code=view_kwargs['app_code'])
        #     except App.DoesNotExist:
        #         return render_to_response('westley/errors/not_found.html', RequestContext(request, {'thing': 'App'}))
        #     del view_kwargs['app_code']
        #     # move component_path into request, it's extracted with the local pattern
        #     request.component_path = m.group('component_path')
        #     # check access to component  (feature-vectors DISABLED for now)
        #     #if not request.app.feature_available(request.component_path):
        #      #   raise Http404


