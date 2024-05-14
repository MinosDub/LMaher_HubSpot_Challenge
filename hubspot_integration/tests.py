import django
from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        'hubspot_integration.apps.HubspotAppConfig'
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
django.setup()


import unittest
from unittest.mock import MagicMock, patch
from django.http import HttpResponse
from hubspot_integration.services.callback_handler import CallbackHandler


class TestCallbackHandler(unittest.TestCase):
    def setUp(self):
        self.request_mock = MagicMock()
        self.config = {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
            "redirect_uri": "your_redirect_uri"
        }
        self.handler = CallbackHandler(self.request_mock, self.config)

    def test_handle_get_callback_without_authorization_code(self):
        self.request_mock.GET.get.return_value = None
        response = self.handler.handle_get_callback('callback.html')
        self.assertIsInstance(response, HttpResponse)

    @patch('hubspot_integration.services.callback_handler.requests.post')
    @patch('hubspot_integration.models.OAuthCredential.save')
    def test_get_access_token_success(self, save_mock, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.json.return_value = {'access_token': 'access_token', 'refresh_token': 'refresh_token'}
        access_token, refresh_token = self.handler._get_access_token('authorization_code')
        self.assertEqual(access_token, 'access_token')
        self.assertEqual(refresh_token, 'refresh_token')
        save_mock.assert_called_once()

    @patch('hubspot_integration.services.callback_handler.requests.post')
    def test_get_access_token_failure(self, post_mock):
        post_mock.return_value.status_code = 400
        access_token, refresh_token = self.handler._get_access_token('authorization_code')
        self.assertIsNone(access_token)
        self.assertIsNone(refresh_token)

    @patch('hubspot_integration.services.callback_handler.requests.post')
    def test_get_refresh_token_success(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.json.return_value = {'access_token': 'new_access_token'}
        access_token = self.handler._get_refresh_token('refresh_token')
        self.assertEqual(access_token, 'new_access_token')

    @patch('hubspot_integration.services.callback_handler.requests.post')
    def test_get_refresh_token_failure(self, post_mock):
        post_mock.return_value.status_code = 400
        access_token = self.handler._get_refresh_token('refresh_token')
        self.assertIsNone(access_token)


    @patch('hubspot_integration.services.callback_handler.requests.get')
    def test_make_api_request_failure(self, get_mock):
        get_mock.return_value.status_code = 400
        response = self.handler._make_api_request('invalid_access_token')
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
