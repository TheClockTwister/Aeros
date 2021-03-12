"""
This module contains features for client-side caching using the Cache-Control header.
"""

from enum import Enum
from quart import Response
import functools
from quart import make_response


class CacheTypes(Enum):
    """
    An enum to replace the cache option strings with variables for auto-complete in most IDEs.
    """
    NO_CACHE = 'no-cache'
    NO_STORE = 'no-store'
    PUBLIC = 'public'
    PRIVATE = 'private'


class CacheControl:
    """
    This class manipulates the Cache-Control header in all responses sent from an endpoint
    decorated with this class.

    .. hint::
        If you need conditional caching rules you may still use `response` from quart to
        manipulate the Cache-Control header to your needs.
    """

    def __init__(
            self, cache_type: CacheTypes, max_age: int = None,
            immutable: bool = False, no_transform: bool = False,
            stale_while_revalidate: int = None, stale_if_error: bool = False,
            cache_on_status: list = [200]
    ):
        """
        Arguments:
            cache_type (CacheTypes): public | private | no-cache | no-store
            max_age (int): mag-age in seconds
            no_transform (bool): disallow proxy changes?
            immutable (bool): If set, browsers will not re-validate
            stale_while_revalidate (int): Time in seconds how long we allow to serve the old content while re-validating
            stale_if_error (bool): Serve the last cached content if backend gives error code
            cache_on_status (list): A list of HTTP response codes when to apply the policy (default: [200])

        """
        self.cache_on_status = cache_on_status
        self.params = [cache_type.value]
        self.params.append(f'max_age={max_age}') if max_age else None,
        self.params.append('immutable') if immutable else None
        self.params.append('no-transform') if no_transform else None
        self.params.append(f'stale-while-revalidate={stale_while_revalidate}') if stale_while_revalidate else None
        self.params.append('stale-if-error') if stale_if_error else None

    def __call__(self, f: callable) -> callable:
        @functools.wraps(f)
        async def wrapped(*args, **kwargs):
            response = await f(*args, **kwargs)

            if not isinstance(response, Response):
                response = await make_response(response)

            if response.status_code in self.cache_on_status:
                response.headers['cache-control'] = ', '.join(self.params)

            return response

        return wrapped
