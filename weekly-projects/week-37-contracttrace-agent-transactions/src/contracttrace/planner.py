"""Constrained local planning; LLM output is a proposal, never an authority."""
import json
import re
import urllib.request
from .core import Command

PATTERN = re.compile(r'^(reserve|release|ship) (\d+) (?:units? of )?([A-Za-z0-9_-]+) for ([A-Za-z0-9_-]+)$', re.I)


def deterministic_plan(text, *, tenant, actor, request_id, approval=False):
    match = PATTERN.fullmatch(text.strip())
    if not match:
        raise ValueError('request outside supported grammar; no action taken')
    action, qty, sku, order = match.groups()
    return Command.parse({'request_id': request_id, 'tenant': tenant, 'actor': actor,
                          'action': action.lower(), 'quantity': int(qty), 'sku': sku,
                          'order_id': order, 'approval': approval}).__dict__


def local_llm_proposal(text, *, endpoint='http://127.0.0.1:8080/v1/chat/completions', model='local'):
    """Optional llama.cpp server; proposal excludes trusted tenant/actor/approval."""
    if not endpoint.startswith('http://127.0.0.1:') and not endpoint.startswith('http://localhost:'):
        raise ValueError('only loopback inference endpoints allowed in local reference')
    body = json.dumps({'model': model, 'temperature': 0, 'max_tokens': 128,
                       'messages': [{'role': 'system', 'content': 'Return only JSON with action (reserve/release/ship), sku, order_id, quantity. No other keys.'},
                                    {'role': 'user', 'content': text}]}).encode()
    req = urllib.request.Request(endpoint, body, {'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=15) as response:
        result = json.load(response)
    proposal = json.loads(result['choices'][0]['message']['content'])
    if set(proposal) != {'action', 'sku', 'order_id', 'quantity'}:
        raise ValueError('invalid proposal schema')
    return proposal


def bind_proposal(proposal, *, tenant, actor, request_id, approval=False):
    """Trusted metadata supplied only by caller; policy still enforced by gateway."""
    if set(proposal) != {'action', 'sku', 'order_id', 'quantity'}:
        raise ValueError('proposal contains unauthorized fields')
    return Command.parse({**proposal, 'tenant': tenant, 'actor': actor,
                          'request_id': request_id, 'approval': approval}).__dict__
