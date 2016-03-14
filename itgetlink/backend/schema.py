from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
import arrow
import colander as cl
# from flask import current_app

# temporary not used, please don't remove this function
# def msisdn_validator(node, value):
#     config = current_app.config
#     prefixs = config.get("ISAT_MSISDN_PREFIX") + \
#         config.get("XL_MSISDN_PREFIX") + config.get("TSEL_MSISDN_PREFIX")
#     if value[:5] not in prefixs:
#         raise cl.Invalid(node, 'not recognized')

#: Replaces whitespace with plus character.
whitespace_to_plus = lambda v: v.replace(" ", "+") if hasattr(v, "replace") else v  # noqa


def date_validation(node, value):
    current_date = arrow.utcnow()
    date = arrow.get(value, 'YYYY-MM-DD HH:mm:00')
    if date < current_date:
        raise cl.Invalid(node, 'Must be newer from current date')


class MTPushSchema(cl.MappingSchema):
    @cl.instantiate(validator=cl.Length(max=100))
    class msisdn(cl.SequenceSchema):
        msisdn = cl.SchemaNode(
            cl.String(),
            validator=cl.All(
                cl.Length(max=80, min=1),
            )
        )

    sms = cl.SchemaNode(
        cl.String(), validator=cl.All(cl.Length(max=200)))

    vip = cl.SchemaNode(
        cl.String(), validator=cl.All(cl.Length(max=25)))

    adn = cl.SchemaNode(
        cl.Integer(),
        missing=2000,
        default=2000,
    )

    message_type = cl.SchemaNode(
        cl.String(),
        default="mtpush",
        missing="mtpush",
    )


class MTSchema(cl.MappingSchema):
    msisdn = cl.SchemaNode(
        cl.String(),
        validator=cl.All(cl.Length(max=80)),
        description="MSISDN",
        preparer=whitespace_to_plus,
    )

    msisdn_hash = cl.SchemaNode(
        cl.String(),
        validator=cl.All(cl.Length(max=80)),
        description="MSISDN hash",
        preparer=whitespace_to_plus,
    )

    # the ``message``; uses backward-compat name as ``sms``
    sms = cl.SchemaNode(
        cl.String(),
        validator=cl.All(cl.Length(max=200)),
        description="Message",
    )

    # the ``session_id``; uses backward-compat name as ``trx_id``
    trx_id = cl.SchemaNode(
        cl.String(),
        validator=cl.All(cl.Length(max=100)),
        missing="",
        description="Session or transaction ID",
        preparer=whitespace_to_plus,
    )

    # the ``shortcode``; uses backward-compat name as ``masking``
    masking = cl.SchemaNode(
        cl.Integer(),
        description="ADN",
        missing="",
    )

    # the ``client``; uses backward-compat name as ``vip``
    vip = cl.SchemaNode(
        cl.String(),
        validator=cl.All(cl.Length(max=20, min=1)),
        description="VIP name",
    )


def build_mt_hook(url, method, mt_schema):
    serialized = {
        "url": url,
        "method": method,
        "data": {},
        "params": {},
    }
    for child in mt_schema.children:
        serialized["data"][child.name] = {
            "description": child.description,
            "type": child.typ.__class__.__name__.lower(),
            "required": child.required,
        }
    return serialized


class BroadcastSchema(cl.MappingSchema):
    object_id = cl.SchemaNode(cl.String())
    object_type = cl.SchemaNode(cl.String())
    subject_id = cl.SchemaNode(cl.String())
    subject_type = cl.SchemaNode(cl.String())
    start_at = cl.SchemaNode(
        cl.String(),
        validator=date_validation,
    )
    short_id = cl.SchemaNode(
        cl.String(),
        missing=None
    )

    bc_type = cl.SchemaNode(
        cl.String(),
        default="bc",
        missing="bc",
    )

    class msisdn(cl.SequenceSchema):
        msisdn = cl.SchemaNode(
            cl.String(),
            validator=cl.All(
                cl.Length(max=80, min=1),
            )
        )


class EbookSchema(cl.MappingSchema):
    @cl.instantiate(validator=cl.Length(max=100))
    class msisdn(cl.SequenceSchema):
        msisdn = cl.SchemaNode(
            cl.String(),
            validator=cl.All(
                cl.Length(max=80, min=1),
            )
        )

    sms = cl.SchemaNode(
        cl.String(), validator=cl.All(cl.Length(max=200)))

    vip = cl.SchemaNode(
        cl.String(), validator=cl.All(cl.Length(max=25)))

    adn = cl.SchemaNode(
        cl.Integer(),
        missing=2000,
        default=2000,
    )

    message_type = cl.SchemaNode(
        cl.String(),
        default="ebook",
        missing="ebook",
    )

    start_at = cl.SchemaNode(
        cl.String(),
        validator=date_validation,
    )