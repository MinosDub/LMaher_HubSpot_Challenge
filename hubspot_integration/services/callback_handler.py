import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from ..models import HubspotResponseModel, OAuthCredential
from django.core.cache import cache
import requests


class CallbackHandler:
    def __init__(self, request, config):
        self.request = request
        self.config = config

    def handle_get_callback(self, template_name):
        authorization_code = self.request.GET.get('code')

        if authorization_code:
            return render(self.request, template_name, {'authorization_code': authorization_code})
        else:
            return HttpResponseBadRequest("Authorization code not found in request parameters.")

    def handle_post_callback(self):
        try:
            access_token = self._get_access_token_from_cache()
        except cache.NotFound:
            access_token = None

        if not access_token:
            # Token not found in cache, attempt to obtain from the request
            authorization_code = self.request.POST.get('authorization_code')
            if not authorization_code:
                return HttpResponseBadRequest('Authorization code not found in request parameters')

            access_token, _ = self._get_access_token(authorization_code)
            if not access_token:
                return HttpResponseServerError('Error occurred while obtaining access token')

            # Store the access token in the cache
            self._store_access_token_in_cache(access_token)

        # Make API request and handle response
        api_response = self._make_api_request(access_token)
        if not api_response:
            return HttpResponseServerError('Error occurred while making request to HubSpot API')

        return render(self.request, 'api_response.html', {'response_data': api_response})


    def _store_access_token_in_cache(self, access_token):
        cache.set('access_token', access_token, timeout=3600)

    def _get_access_token_from_cache(self):
        return cache.get('access_token')

    def _get_access_token(self, authorization_code):
        # Prepare payload for token request
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.config["client_id"],
            'client_secret': self.config["client_secret"],
            'redirect_uri': self.config['redirect_uri'],
            'code': authorization_code
        }

        # Make request to HubSpot token endpoint
        token_url = 'https://api.hubspot.com/oauth/v1/token'
        response = requests.post(token_url, data=payload)

        # return access token and save it to model
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            refresh_token = response.json().get('refresh_token')
            # save token to model
            oath_obj = OAuthCredential(access_token=access_token, refresh_token=refresh_token)
            oath_obj.save()
            return access_token, refresh_token
        else:
            return None, None

    def _get_refresh_token(self, refresh_token):
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self.config["client_id"],
            'client_secret': self.config["client_secret"],
            'refresh_token': refresh_token
        }
        token_url = 'https://api.hubspot.com/oauth/v1/token'
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            return access_token
        else:
            return None

    def _save_hubspot_data(self, response):
        hubspot_response = HubspotResponseModel()
        hubspot_response.response_code = response.status_code
        hubspot_response.response_text = response.json()
        hubspot_response.save()

    def _make_api_request(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        endpoint = 'https://api.hubapi.com/contacts/v1/lists/all/contacts/all'
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            self._save_hubspot_data(response)
            data = response.json()
            return json.dumps(data)

        if response.status_code == 401:  # Token expired, attempt refresh
            oauth_credential = OAuthCredential.objects.first()
            if not oauth_credential.refresh_token:
                return None

            access_token = self._get_refresh_token(oauth_credential.refresh_token)
            if not access_token:
                return None

            # save updated token and retry API request
            oauth_credential.access_token = access_token
            oauth_credential.save()

            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return json.dumps(data)

        return None


