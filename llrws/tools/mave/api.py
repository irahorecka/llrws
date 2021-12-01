"""
A simple MaveDB API wrapper.

E.g. Get scoresets with Universal Resource Number "urn:mavedb:00000040-a-4" :
scoresets(urn="urn:mavedb:00000040-a-4").get().json()
"""

import functools
import urllib
from posixpath import join as urljoin

import requests


def get_scoresets_csv_stream_from_urn(urn):
    """Uses URN to query MaveDB scoresets. Retrieves scoresets CSV
    as a stream.

    Args:
        urn (str): URN value

    Returns:
        (None)
    """
    return scoresets(urn=urn, download=True).get().content.decode("utf-8")


# #############################################################


class BaseAPI:
    """Base API wrapper for the MaveDB REST API.

    Args:
        *args (any): URL parameters as args
    Kwargs:
        **kwargs (any): URL parameters as kwargs
    """

    base_url = "https://mavedb.org/api"

    def __init__(self, **kwargs):
        self.path = []
        self.params = kwargs

    @property
    def url(self):
        """Generates MaveDB REST API URL.

        Returns:
            (str): Generated URL
        """
        # By default, urllib.parse.quote() function is intended for quoting the path section of a URL.
        url_ = urljoin(self.base_url, urllib.parse.quote(urljoin(*self.path)))
        if not any(self.params.values()):
            return url_
        # Use urllib.parse.quote() to quote parameters passed to urllib.parse.urlencode().
        return url_ + "?" + urllib.parse.urlencode(self.params, quote_via=urllib.parse.quote)


def requests_handler(method):
    """Uses method signatures to dispatch requests.

    Args:
        *args (any): *args for requests.Session methods (e.g. requests.get)
    Kwargs:
        **kwargs (any): **kwargs for requests.Session methods

    Returns:
        (requests.models.Response): Requests response from MaveDB REST API query
    """
    requests_methods = {
        "delete": requests.delete,
        "get": requests.get,
        "patch": requests.patch,
        "post": requests.post,
        "put": requests.put,
    }

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        requests_method = requests_methods[method.__name__]
        response = requests_method(self.url, *args, **kwargs)
        response.raise_for_status()
        return response

    return wrapper


class doi(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class ensembl(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class experiments(BaseAPI):
    def __init__(self, urn=""):
        super().__init__(urn=urn)
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class experimentsets(BaseAPI):
    def __init__(self, urn=""):
        super().__init__(urn=urn)
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class genome(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class keyword(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class pubmed(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class reference(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class refseq(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class scoresets(BaseAPI):
    def __init__(self, urn="", download=False):
        # URN and download flag are included in the URL path.
        # Downloads URN's MAVE scoreset as a CSV stream
        super().__init__()
        self.path.append(self.__class__.__name__)
        self.path.append(urn)
        if download is True:
            self.path.append("scores")

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class sra(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class target(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class uniprot(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass


class users(BaseAPI):
    def __init__(self):
        super().__init__()
        self.path.append(self.__class__.__name__)

    @requests_handler
    def get(self, *args, **kwargs):
        pass

    @requests_handler
    def post(self, *args, **kwargs):
        pass
