# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
import functools
import json
import re
import warnings
from collections import namedtuple
from xml.parsers.expat import ExpatError

import colander
import requests
import xmltodict
from requests_oauthlib import OAuth1Session
from mimerender import FlaskMimeRender

from .logger import sentry

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import string
import random

#: A general purpose data container for validation.
#: Use ``args`` to store deserialized arguments,
#: ``errors`` to store error message for each passed argument,
#: and ``raw_args`` to store original arguments that ignores
#: the state whether validation is succeed or failed.
_validation = namedtuple("Validation", "args errors raw_args")

#: A decorator to render response as defined in HTTP content negotiation
#: mechanism.
#:
#: Typical usage (in conjuction with :func:`_json_dumps`)
#: to render JSON response:
#:
#: .. sourcecode:: python
#:
#:     @mimerender(json=_json_dumps)
#:     def hello(name="johndoe")
#:         return {"message": "hello, {}".format(name)}
#:
#: An example to render JSON and XML response:
#:
#: .. sourcecode:: python
#:
#:     @mimerender(json=_json_dumps, xml=_xml_dumps)
#:
mimerender = FlaskMimeRender()

#: A decorator to render JSON response.
#:
#: .. sourcecode:: python
#:
#:     @render_json
#:     def hello(name="johndoe"):
#:         return {"message": "hello, {}".format(name)}
#:
render_json = mimerender(
    json=lambda **kwargs: json.dumps(kwargs, ensure_ascii=False)
)

#: A decorator to render XML response.
#:
#: .. sourcecode:: python
#:
#:     @render_xml
#:     def hello(name="johndoe"):
#:         xml = """<?xml version="1.0" encoding="utf-8"?>
#: <data><username>johndoe</username><data>
#:         """
#:         return {"message": xml}
#:
render_xml = mimerender(xml=lambda message: message)


def deprecated(func):
    """A decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn(
            "Call to deprecated callable '{}'.".format(func.__name__),
        )
        return func(*args, **kwargs)
    return new_func


def validate_schema(datamapping, schema):
    """Validates a dict-like object to match againsts a colander schema.

    :param datamapping: A dict maps key and value as string
    :param schema: Instance of colander schema
    """
    try:
        raw_args = {k: v for k, v in datamapping.items()}
        args, errors = schema.deserialize(raw_args), {}
    except colander.Invalid as exc:
        args, errors = {}, exc.asdict()
    return _validation(args=args, errors=errors, raw_args=raw_args)


def make_response_body(**kwargs):
    """Creates a dict which set all necessary keys.

    Typical usage:

    .. sourcecode:: python

        >> body = make_response_body()
        >> body
        {"error": None, "meta": None, "objects": None}

    This function accepts 3 keys, ``error``, ``meta``, ``objects``.
    Hence we could build richer key-value pairs by passing
    the appropriate keys:

    .. sourcecode:: python

        >> err = {"username": "required"}
        >> body = make_response_body({"error": err})
        >> body
        {"error": {"username": "required"}, "meta": None, "objects": None}

    Since it always returns ``dict``, we could apply any dict operation, e.g.:

    .. sourcecode:: python

        >> body
        {"error": {"username": "required"}, "meta": None, "objects": None}
        >> body["meta"] = {"status": 200}
        >> body
        {
            "error": {"username": "required"},
            "meta": {"status": 200},
            "objects": None
        }

    :param kwargs: Arbitrary keyword arguments; Currently, only 3 keys
        are accepted — ``error``, ``meta``, and ``objects``
    :returns: dict

    """
    keys = ("error", "meta", "objects",)
    bases = dict.fromkeys(keys)
    bases.update({k: v for k, v in kwargs.items() if k in keys})
    return bases


# TODO: a proper name?
def parse_xml(xml, encoding="utf-8", full_document=True):
    """Parse an XML string and transforms into an instance of ``_validation``.

    :param xml: XML string
    """
    try:
        args, errors = xmltodict.parse(xml, encoding=encoding), {}
    except (TypeError, ExpatError, AttributeError) as exc:
        args, errors = {}, {"message": exc}
    return _validation(args=args, errors=errors, raw_args={})


# TODO: handle error verbosely
# TODO: a proper name?
def unparse_xml(full_document=True, encoding="utf-8", **kwargs):
    """Transforms ``dict``-like object into an XML string.

    :param full_document: Whether XML doc string must be appended
        (e.g. ``<?xml version="1.0">)
    :param kwargs: Any keyword argument as XML tags
    """
    xmlstr = xmltodict.unparse(kwargs, encoding=encoding,
                               full_document=full_document)
    return xmlstr


def msisdn_mapper(msisdn, config, community, _type=None, shortcode =None):
    data = {}
    prefix = msisdn[:5]

    if community.lower() == 'payau':
        data = {
            "name": "andalabs",
            "username": config.get("ANDALABS_USERNAME"),
            "password": config.get("ANDALABS_PASSWORD"),
            "mtpush_url": config.get("ANDALABS_MT_PUSH_URL"),
        }

        if prefix in config.get("ISAT_MSISDN_PREFIX"):
            data["network_code"] = "isat"
        elif prefix in config.get("TSEL_MSISDN_PREFIX"):
            data["network_code"] = "tsel2"
        elif prefix in config.get("XL_MSISDN_PREFIX"):
            data["network_code"] = "xl"

    elif community.lower() == 'rpp' or community.lower() == 'lisa' or community.lower() == 'konco' or community.lower() == 'energi' or community.lower() == 'perempuan':
        if prefix in config.get("ISAT_MSISDN_PREFIX"):
            data = {
                "name": "andalabs",
                "network_code": "isat",
                "username": config.get("ANDALABS_USERNAME"),
                "password": config.get("ANDALABS_PASSWORD"),
                "mtpush_url": config.get("ANDALABS_MT_PUSH_URL"),
            }
        elif prefix in config.get("TSEL_MSISDN_PREFIX"):
            data = {
                "name": "andalabs",
                "network_code": "tsel2",
                "username": config.get("ANDALABS_USERNAME"),
                "password": config.get("ANDALABS_PASSWORD"),
                "mtpush_url": config.get("ANDALABS_MT_PUSH_URL"),
            }
        elif prefix in config.get("XL_MSISDN_PREFIX"):
            data = {
                "name": "xl",
                "network_code": "xl",
                "username": config.get("XL_MT_APP_ID"),
                "password": config.get("XL_MT_APP_PWD"),
                "mtpush_url": config.get("XL_MT_PUSH_URL"),
                "shortname": config.get("XL_MT_SHORTNAME"),
            }
            if _type == "push":
                data["username"] = config.get("XL_MT_PUSH_APP_ID")
                data["password"] = config.get("XL_MT_PUSH_APP_PWD")
                data["shortname"] = config.get("XL_MT_PUSH_SHORTNAME")

    else:
        if prefix in config.get("ISAT_MSISDN_PREFIX"):
            data = {
                "name": "kisel",
                "network_code": "isat",
                "username": config.get("KISEL_USERNAME"),
                "password": config.get("KISEL_PASSWORD"),
                "mtpush_url": config.get("KISEL_MT_PUSH_URL"),
            }
            if shortcode == 2000 and _type == "push":
                data["username"] = config.get("KISEL_PUSH_USERNAME")
                data["password"] = config.get("KISEL_PUSH_PASSWORD")
        elif prefix in config.get("TSEL_MSISDN_PREFIX"):
            data = {
                "name": "andalabs",
                "network_code": "tsel2",
                "username": config.get("ANDALABS_USERNAME"),
                "password": config.get("ANDALABS_PASSWORD"),
                "mtpush_url": config.get("ANDALABS_MT_PUSH_URL"),
            }
        else:
            # assuming XL
            if shortcode == 2000:
                data = {
                    "name": "kisel",
                    "network_code": "xl",
                    "username": config.get("KISEL_USERNAME"),
                    "password": config.get("KISEL_PASSWORD"),
                    "mtpush_url": config.get("KISEL_MT_PUSH_URL"),
                }
                if _type == "push":
                    data["username"] = config.get("KISEL_PUSH_USERNAME")
                    data["password"] = config.get("KISEL_PUSH_PASSWORD")
            elif shortcode == 2580:  # direct XL
                data = {
                    "name": "xl",
                    "network_code": "xl",
                    "username": config.get("XL_MT_APP_ID"),
                    "password": config.get("XL_MT_APP_PWD"),
                    "mtpush_url": config.get("XL_MT_PUSH_URL"),
                    "shortname": config.get("XL_MT_SHORTNAME"),
                }
                if _type == "push":
                    data["username"] = config.get("XL_MT_PUSH_APP_ID")
                    data["password"] = config.get("XL_MT_PUSH_APP_PWD")
                    data["shortname"] = config.get("XL_MT_PUSH_SHORTNAME")
    
   # sentry.captureMessage(
   #     "Capture msisdn_maper",
   #     extra={"name": data["name"],
   #            "network_code": data["network_code"],
   #            "username": data["username"],
   #            "password": data["password"],
   #            "mtpush_url": data["mtpush_url"],
   #            "shortname": data["shortname"]},
   # )
        
    return data


def msisdn_prefix_replace(message, replacer):
    return re.sub(r"(0)(\d+)", r"{}\2".format(replacer), message)


def encode_header_keys(headers, encoding="utf-8"):
    # see https://github.com/mitsuhiko/flask/issues/758
    headers = headers or {}
    return {k.encode(encoding): v for k, v in headers.items()}


def guess_msisdn_operator(msisdn, config):
    prefix = msisdn[:5]

    if prefix in config.get("ISAT_MSISDN_PREFIX"):
        return "indosat"
    elif prefix in config.get("TSEL_MSISDN_PREFIX"):
        return "telkomsel"
    elif prefix in config.get("XL_MSISDN_PREFIX"):
        return "xl"
    else:
        return "xl"


def id_generator(size=6, chars=string.digits + string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def parse_url(url):
    # get query from URL and transform transforms into an instance of ``_validation``.
    try:
        url = urlparse(url)
        data = url.query
        arData = data.split('&',4)
        dictData = {'mo_data' : {}}

        for listdata in arData:
            tempArray = listdata.split('=',1)
            dictData['mo_data'][tempArray[0]] = tempArray[1]

        
        if dictData['mo_data']['msisdn'] == "":
            args, errors = {}, {'message' : 'required msisdn'}
        elif dictData['mo_data']['sms'] == "":
            args, errors = {}, {'message' : 'required sms'}
        elif dictData['mo_data']['src'] == "":
            args, errors = {}, {'message' : 'required shortcode'}
        elif dictData['mo_data']['dcs'] == "":
            args, errors = {}, {'message' : 'required dcs'}
        else:
            args, errors = dictData, {}
    except(TypeError, ExpatError, AttributeError) as exc:
        args, errors = {}, {"message": exc}
        
    return _validation(args=args, errors=errors, raw_args={})

