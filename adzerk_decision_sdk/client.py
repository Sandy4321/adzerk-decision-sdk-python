import copy
from adzerk_decision_sdk.api_client import ApiClient
from adzerk_decision_sdk.configuration import Configuration
from adzerk_decision_sdk.api.decision_api import DecisionApi
from adzerk_decision_sdk.api.userdb_api import UserdbApi


class Client(object):
    class _DecisionClient(object):
        def __init__(self, api_client: ApiClient):
            self.api_client = api_client
            self.api = DecisionApi(api_client)

        def get(self, **kwargs):
            return self.api.get_decisions(**kwargs)

        def get_with_explanation(self, **kwargs):
            api_client = copy.deepclone(self.api_client)
            api_client.set_default_header('X-Adzerk-Explain',
                                          api_client.configuration.api_key)

            api = DecisionApi(api_client)
            return api.get_decisions(**kwargs)

    class _UserDbClient(object):
        def __init__(self, api_client: ApiClient):
            self.api = UserdbApi(api_client)

        def add_custom_properties(self, network_id, user_key, properties):
            return self.api.add_custom_properties(network_id,
                                                  user_key,
                                                  body=properties)

        def add_interests(self, network_id, user_key, interests: list):
            return self.api.add_interests(network_id,
                                          user_key,
                                          ",".join(interests))

        def add_retargeting_segment(self,
                                    network_id,
                                    user_key,
                                    advertiser_id,
                                    retargeting_segment_id):
            return self.api.add_retargeting_segment(network_id,
                                                    advertiser_id,
                                                    retargeting_segment_id,
                                                    user_key)

        def forget(self, network_id, user_key):
            return self.api.forget(network_id, user_key)

        def gdpr_consent(self, network_id, gdpr_consent):
            return self.api.gdpr_consent(network_id, body=gdpr_consent)

        def ip_override(self, network_id, user_key, ip):
            return self.api.ip_override(network_id, user_key, ip)

        def match_user(self, network_id, user_key, partner_id, user_id):
            return self.api.match_user(network_id,
                                       user_key,
                                       partner_id,
                                       user_id)

        def opt_out(self, network_id, user_key):
            return self.api.opt_out(network_id, user_key)

        def read(self, network_id, user_key):
            return self.api.read(network_id, user_key)

    def __init__(self, network_id, protocol='https',
                 host=None, path=None, api_key=None,
                 user_agent=None, logger_format=None,
                 logger_file=None, is_debug=False,):
        protocol = protocol or 'https'
        host = f'e-{network_id}.adzerk.net' if host is None else host

        configuration = Configuration(host,
                                      api_key={'X-Adzerk-ApiKey': api_key})

        if logger_format is not None:
            configuration.logger_format = logger_format

        if logger_file is not None:
            configuration.logger_file = logger_file

        api_client = ApiClient(configuration)

        self.decision_client = self._DecisionClient(api_client)
        self.user_db_client = self._UserDbClient(api_client)

    @property
    def decisions(self):
        return self.decision_client

    @property
    def user_db(self):
        return self.user_db_client
