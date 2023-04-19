from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class CustomAccount(ProviderAccount):
    pass


class CustomProvider(OAuth2Provider):

    id = 'customprovider'
    name = 'My Custom oAuth Provider'
    account_class = CustomAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        from pprint import pprint
        return dict(uuid=data['uuid'],
                    username=data['username'],
                    avatar=data['avatar'])

    def get_default_scope(self):
        scope = ['read']
        return scope

provider_classes=[CustomProvider]

providers.registry.register(CustomProvider)
