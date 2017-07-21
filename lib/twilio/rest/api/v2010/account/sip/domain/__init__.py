# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.api.v2010.account.sip.domain.credential_list_mapping import CredentialListMappingList
from twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping import IpAccessControlListMappingList


class DomainList(ListResource):

    def __init__(self, version, account_sid):
        """
        Initialize the DomainList

        :param Version version: Version that contains the resource
        :param account_sid: A 34 character string that uniquely identifies this resource.

        :returns: twilio.rest.api.v2010.account.sip.domain.DomainList
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainList
        """
        super(DomainList, self).__init__(version)

        # Path Solution
        self._solution = {
            'account_sid': account_sid,
        }
        self._uri = '/Accounts/{account_sid}/SIP/Domains.json'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams DomainInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.sip.domain.DomainInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists DomainInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.sip.domain.DomainInstance]
        """
        return list(self.stream(
            limit=limit,
            page_size=page_size,
        ))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of DomainInstance records from the API.
        Request is executed immediately

        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainPage
        """
        params = values.of({
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return DomainPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of DomainInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return DomainPage(self._version, response, self._solution)

    def create(self, domain_name, friendly_name=values.unset,
               auth_type=values.unset, voice_url=values.unset,
               voice_method=values.unset, voice_fallback_url=values.unset,
               voice_fallback_method=values.unset,
               voice_status_callback_url=values.unset,
               voice_status_callback_method=values.unset):
        """
        Create a new DomainInstance

        :param unicode domain_name: The unique address on Twilio to route SIP traffic
        :param unicode friendly_name: A user-specified, human-readable name for the trigger.
        :param unicode auth_type: The types of authentication mapped to the domain
        :param unicode voice_url: URL Twilio will request when receiving a call
        :param unicode voice_method: HTTP method to use with voice_url
        :param unicode voice_fallback_url: URL Twilio will request if an error occurs in executing TwiML
        :param unicode voice_fallback_method: HTTP method used with voice_fallback_url
        :param unicode voice_status_callback_url: URL that Twilio will request with status updates
        :param unicode voice_status_callback_method: The voice_status_callback_method

        :returns: Newly created DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        """
        data = values.of({
            'DomainName': domain_name,
            'FriendlyName': friendly_name,
            'AuthType': auth_type,
            'VoiceUrl': voice_url,
            'VoiceMethod': voice_method,
            'VoiceFallbackUrl': voice_fallback_url,
            'VoiceFallbackMethod': voice_fallback_method,
            'VoiceStatusCallbackUrl': voice_status_callback_url,
            'VoiceStatusCallbackMethod': voice_status_callback_method,
        })

        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )

        return DomainInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
        )

    def get(self, sid):
        """
        Constructs a DomainContext

        :param sid: Fetch by unique Domain Sid

        :returns: twilio.rest.api.v2010.account.sip.domain.DomainContext
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainContext
        """
        return DomainContext(
            self._version,
            account_sid=self._solution['account_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a DomainContext

        :param sid: Fetch by unique Domain Sid

        :returns: twilio.rest.api.v2010.account.sip.domain.DomainContext
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainContext
        """
        return DomainContext(
            self._version,
            account_sid=self._solution['account_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.DomainList>'


class DomainPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the DomainPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: A 34 character string that uniquely identifies this resource.

        :returns: twilio.rest.api.v2010.account.sip.domain.DomainPage
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainPage
        """
        super(DomainPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of DomainInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        """
        return DomainInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.DomainPage>'


class DomainContext(InstanceContext):

    def __init__(self, version, account_sid, sid):
        """
        Initialize the DomainContext

        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param sid: Fetch by unique Domain Sid

        :returns: twilio.rest.api.v2010.account.sip.domain.DomainContext
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainContext
        """
        super(DomainContext, self).__init__(version)

        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'sid': sid,
        }
        self._uri = '/Accounts/{account_sid}/SIP/Domains/{sid}.json'.format(**self._solution)

        # Dependents
        self._ip_access_control_list_mappings = None
        self._credential_list_mappings = None

    def fetch(self):
        """
        Fetch a DomainInstance

        :returns: Fetched DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return DomainInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def update(self, auth_type=values.unset, friendly_name=values.unset,
               voice_fallback_method=values.unset, voice_fallback_url=values.unset,
               voice_method=values.unset, voice_status_callback_method=values.unset,
               voice_status_callback_url=values.unset, voice_url=values.unset):
        """
        Update the DomainInstance

        :param unicode auth_type: The auth_type
        :param unicode friendly_name: A user-specified, human-readable name for the trigger.
        :param unicode voice_fallback_method: The voice_fallback_method
        :param unicode voice_fallback_url: The voice_fallback_url
        :param unicode voice_method: HTTP method to use with voice_url
        :param unicode voice_status_callback_method: The voice_status_callback_method
        :param unicode voice_status_callback_url: The voice_status_callback_url
        :param unicode voice_url: The voice_url

        :returns: Updated DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        """
        data = values.of({
            'AuthType': auth_type,
            'FriendlyName': friendly_name,
            'VoiceFallbackMethod': voice_fallback_method,
            'VoiceFallbackUrl': voice_fallback_url,
            'VoiceMethod': voice_method,
            'VoiceStatusCallbackMethod': voice_status_callback_method,
            'VoiceStatusCallbackUrl': voice_status_callback_url,
            'VoiceUrl': voice_url,
        })

        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )

        return DomainInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the DomainInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    @property
    def ip_access_control_list_mappings(self):
        """
        Access the ip_access_control_list_mappings

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingList
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingList
        """
        if self._ip_access_control_list_mappings is None:
            self._ip_access_control_list_mappings = IpAccessControlListMappingList(
                self._version,
                account_sid=self._solution['account_sid'],
                domain_sid=self._solution['sid'],
            )
        return self._ip_access_control_list_mappings

    @property
    def credential_list_mappings(self):
        """
        Access the credential_list_mappings

        :returns: twilio.rest.api.v2010.account.sip.domain.credential_list_mapping.CredentialListMappingList
        :rtype: twilio.rest.api.v2010.account.sip.domain.credential_list_mapping.CredentialListMappingList
        """
        if self._credential_list_mappings is None:
            self._credential_list_mappings = CredentialListMappingList(
                self._version,
                account_sid=self._solution['account_sid'],
                domain_sid=self._solution['sid'],
            )
        return self._credential_list_mappings

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.DomainContext {}>'.format(context)


class DomainInstance(InstanceResource):

    def __init__(self, version, payload, account_sid, sid=None):
        """
        Initialize the DomainInstance

        :returns: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        """
        super(DomainInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'api_version': payload['api_version'],
            'auth_type': payload['auth_type'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'domain_name': payload['domain_name'],
            'friendly_name': payload['friendly_name'],
            'sid': payload['sid'],
            'uri': payload['uri'],
            'voice_fallback_method': payload['voice_fallback_method'],
            'voice_fallback_url': payload['voice_fallback_url'],
            'voice_method': payload['voice_method'],
            'voice_status_callback_method': payload['voice_status_callback_method'],
            'voice_status_callback_url': payload['voice_status_callback_url'],
            'voice_url': payload['voice_url'],
            'subresource_uris': payload['subresource_uris'],
        }

        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: DomainContext for this DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainContext
        """
        if self._context is None:
            self._context = DomainContext(
                self._version,
                account_sid=self._solution['account_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The unique id of the account that sent the message
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def api_version(self):
        """
        :returns: The Twilio API version used to process the message
        :rtype: unicode
        """
        return self._properties['api_version']

    @property
    def auth_type(self):
        """
        :returns: The types of authentication mapped to the domain
        :rtype: unicode
        """
        return self._properties['auth_type']

    @property
    def date_created(self):
        """
        :returns: The date this resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date this resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def domain_name(self):
        """
        :returns: The unique address on Twilio to route SIP traffic
        :rtype: unicode
        """
        return self._properties['domain_name']

    @property
    def friendly_name(self):
        """
        :returns: A user-specified, human-readable name for the trigger.
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def sid(self):
        """
        :returns: A string that uniquely identifies the SIP Domain
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def uri(self):
        """
        :returns: The URI for this resource
        :rtype: unicode
        """
        return self._properties['uri']

    @property
    def voice_fallback_method(self):
        """
        :returns: HTTP method used with voice_fallback_url
        :rtype: unicode
        """
        return self._properties['voice_fallback_method']

    @property
    def voice_fallback_url(self):
        """
        :returns: URL Twilio will request if an error occurs in executing TwiML
        :rtype: unicode
        """
        return self._properties['voice_fallback_url']

    @property
    def voice_method(self):
        """
        :returns: HTTP method to use with voice_url
        :rtype: unicode
        """
        return self._properties['voice_method']

    @property
    def voice_status_callback_method(self):
        """
        :returns: The voice_status_callback_method
        :rtype: unicode
        """
        return self._properties['voice_status_callback_method']

    @property
    def voice_status_callback_url(self):
        """
        :returns: URL that Twilio will request with status updates
        :rtype: unicode
        """
        return self._properties['voice_status_callback_url']

    @property
    def voice_url(self):
        """
        :returns: URL Twilio will request when receiving a call
        :rtype: unicode
        """
        return self._properties['voice_url']

    @property
    def subresource_uris(self):
        """
        :returns: The subresource_uris
        :rtype: unicode
        """
        return self._properties['subresource_uris']

    def fetch(self):
        """
        Fetch a DomainInstance

        :returns: Fetched DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        """
        return self._proxy.fetch()

    def update(self, auth_type=values.unset, friendly_name=values.unset,
               voice_fallback_method=values.unset, voice_fallback_url=values.unset,
               voice_method=values.unset, voice_status_callback_method=values.unset,
               voice_status_callback_url=values.unset, voice_url=values.unset):
        """
        Update the DomainInstance

        :param unicode auth_type: The auth_type
        :param unicode friendly_name: A user-specified, human-readable name for the trigger.
        :param unicode voice_fallback_method: The voice_fallback_method
        :param unicode voice_fallback_url: The voice_fallback_url
        :param unicode voice_method: HTTP method to use with voice_url
        :param unicode voice_status_callback_method: The voice_status_callback_method
        :param unicode voice_status_callback_url: The voice_status_callback_url
        :param unicode voice_url: The voice_url

        :returns: Updated DomainInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.DomainInstance
        """
        return self._proxy.update(
            auth_type=auth_type,
            friendly_name=friendly_name,
            voice_fallback_method=voice_fallback_method,
            voice_fallback_url=voice_fallback_url,
            voice_method=voice_method,
            voice_status_callback_method=voice_status_callback_method,
            voice_status_callback_url=voice_status_callback_url,
            voice_url=voice_url,
        )

    def delete(self):
        """
        Deletes the DomainInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    @property
    def ip_access_control_list_mappings(self):
        """
        Access the ip_access_control_list_mappings

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingList
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingList
        """
        return self._proxy.ip_access_control_list_mappings

    @property
    def credential_list_mappings(self):
        """
        Access the credential_list_mappings

        :returns: twilio.rest.api.v2010.account.sip.domain.credential_list_mapping.CredentialListMappingList
        :rtype: twilio.rest.api.v2010.account.sip.domain.credential_list_mapping.CredentialListMappingList
        """
        return self._proxy.credential_list_mappings

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.DomainInstance {}>'.format(context)
