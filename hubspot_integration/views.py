import os

from django.views import View
from django.shortcuts import redirect, render
from hubspot_integration.services.callback_handler import CallbackHandler
from hubspot_integration.services.oauth_handler import OAuthHandler
from decouple import config
app_config = {
            'client_id': config("CLIENT_ID"),
            'client_secret': config("CLIENT_SECRET"),
            'scopes': ['oauth', 'crm.objects.contacts.read'],
            'auth_uri': config("AUTH_URI"),
            'token_uri': config("TOKEN_URI"),
            'redirect_uri': config("REDIRECT_URI")
        }


class CallbackView(View):
    def get(self, request):
        handler = CallbackHandler(request, app_config)
        response = handler.handle_get_callback(template_name='callback.html')
        return response

    def post(self, request):
        handler = CallbackHandler(request, app_config)
        response = handler.handle_post_callback()
        return response


class HubspotView(View):
    template_name = 'integrate_hubspot.html'

    def get(self, request):
        handler = OAuthHandler(request, app_config)
        auth_url = handler.generate_auth_url()
        return render(self.request, self.template_name, {'auth_url': auth_url})


