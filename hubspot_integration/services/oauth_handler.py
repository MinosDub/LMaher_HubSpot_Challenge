from requests_oauthlib import OAuth2Session


class OAuthHandler:
    def __init__(self, request, config):
        self.request = request
        self.config = config

    def generate_auth_url(self):
        oauth = OAuth2Session(
                client_id=self.config['client_id'],
                scope=self.config['scopes'],
                redirect_uri=self.config['redirect_uri']
            )

        auth_url, _ = oauth.authorization_url(self.config['auth_uri'])
        return auth_url
