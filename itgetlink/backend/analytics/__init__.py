from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from collections import defaultdict
from itertools import groupby

from flask import Blueprint, request
from werkzeug.datastructures import MultiDict

from ..database import Message, db
from ..utils import render_json, make_response_body, validate_schema
from .schema import PaginationSchema

analytic_api = Blueprint("analytic_api", __name__)


ACTIVE_PROVIDERS = ("kisel", "andalabs",)


def as_dict(msg):
    d = msg.asdict(exclude=["created_at", "data"])
    d.update({"created_at": msg.created_at.isoformat()})
    return d


def paginate_messages(model, page=1, per_page=20, type_="mo"):
    q = (model.query.filter(model.provider.in_(ACTIVE_PROVIDERS),
                            model.type == type_,
                            )
                    .order_by(model.created_at.desc()))
    return q.paginate(page=page, per_page=per_page)


@analytic_api.route("/inbox")
@render_json
def handle_inbox():
    body = make_response_body()
    validation = validate_schema(request.values, PaginationSchema())

    if validation.errors:
        body["error"] = {"params": validation.errors}
        return body, 400

    messages = paginate_messages(
        Message,
        validation.args["page"],
        validation.args["per_page"],
        type_="mo",
        )

    body["meta"] = {"has_next": messages.has_next,
                    "has_prev": messages.has_prev,
                    "total": messages.total,
                    }
    body["objects"] = [as_dict(msg) for msg in messages.items]
    return body


@analytic_api.route("/outbox")
@render_json
def handle_outbox():
    body = make_response_body()
    validation = validate_schema(request.values, PaginationSchema())

    if validation.errors:
        body["error"] = {"params": validation.errors}
        return body, 400

    messages = paginate_messages(
        Message,
        validation.args["page"],
        validation.args["per_page"],
        type_="mt",
        )

    body["meta"] = {"has_next": messages.has_next,
                    "has_prev": messages.has_prev,
                    "total": messages.total,
                    }
    body["objects"] = [as_dict(msg) for msg in messages.items]
    return body


def _normalize_networks(provider, networks):
    _provider = {"provider": provider, "networks": []}
    for netw, stats in groupby(networks, lambda r: r["network_code"]):
        _network = MultiDict()

        for s in stats:
            _network.add(netw, {"type": s["type"], "count": s["count"]})

        _provider["networks"].append({
            "network": netw, "stats": _network.getlist(netw)
            })
    return _provider


def normalize_stats(data):
    normalized_stats = []
    for community, providers in data.items():
        _community = {"community": community, "providers": []}

        for provider, networks in groupby(providers, lambda r: r["provider"]):
            _community["providers"].append(
                _normalize_networks(provider, networks))

        normalized_stats.append(_community)
    return normalized_stats


@analytic_api.route("/stats")
@render_json
def handle_stats():
    body = make_response_body()

    query = Message.query.with_entities(
        Message.provider,
        Message.community,
        Message.network_code,
        Message.type,
        db.func.count(Message.community).label("count"),
        )
    query = query.filter(Message.provider.in_(ACTIVE_PROVIDERS))
    query = query.group_by(
        Message.community,
        Message.provider,
        Message.network_code,
        Message.type,
        )

    data = defaultdict(list)

    for msg in query:
        data[msg.community].append({
            k: v for k, v in msg.__dict__.items()
            if k not in ("_labels", "community",)
        })

    body["objects"] = normalize_stats(data)
    return body
