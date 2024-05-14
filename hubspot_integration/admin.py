from django.contrib import admin
from .models import OAuthCredential, HubspotResponseModel
# Register your models here.
admin.site.register(OAuthCredential)
admin.site.register(HubspotResponseModel)