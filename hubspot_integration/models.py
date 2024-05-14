from django.db import models


class OAuthCredential(models.Model):
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)


class HubspotResponseModel(models.Model):
    response_text = models.TextField()
    response_code = models.IntegerField()
