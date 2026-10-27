"""Optional local API; caller identity is bound to server configuration, not request JSON."""
import os
import secrets
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from .core import Gateway
from .planner import deterministic_plan

app = FastAPI(title='ContractTrace', version='0.1.0')


class Intent(BaseModel):
    request_id: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1, max_length=512)


def gateway():
    return Gateway(os.environ.get('CONTRACTTRACE_DB', 'artifacts/state.sqlite'))


@app.get('/health')
def health():
    return gateway().verify()


@app.post('/execute')
def execute(intent: Intent, x_api_key: str | None = Header(default=None)):
    expected = os.environ.get('CONTRACTTRACE_API_KEY')
    if not expected or not x_api_key or not secrets.compare_digest(expected, x_api_key):
        raise HTTPException(403, 'authorization required')
    command = deterministic_plan(intent.text, tenant='demo', actor='alice', request_id=intent.request_id)
    return gateway().execute(command, {'alice': ['operator']})