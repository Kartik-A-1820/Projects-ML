"""Transactional agent action gateway. SQLite is a local reference implementation."""
from __future__ import annotations
import hashlib
import json
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ACTIONS = frozenset({'reserve', 'release', 'ship'})


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


@dataclass(frozen=True)
class Command:
    request_id: str
    tenant: str
    actor: str
    action: str
    order_id: str
    sku: str
    quantity: int
    approval: bool = False

    @classmethod
    def parse(cls, obj: dict) -> 'Command':
        required = {'request_id', 'tenant', 'actor', 'action', 'order_id', 'sku', 'quantity'}
        if not required <= obj.keys() or set(obj) - (required | {'approval'}):
            raise ValueError('invalid command fields')
        if any(not isinstance(obj[k], str) or not obj[k] or len(obj[k]) > 128 for k in required - {'quantity'}):
            raise ValueError('invalid identifier')
        if type(obj['quantity']) is not int or not 1 <= obj['quantity'] <= 10000:
            raise ValueError('quantity out of range')
        if type(obj.get('approval', False)) is not bool:
            raise ValueError('approval must be boolean')
        if obj['action'] not in ACTIONS:
            raise ValueError('unknown action')
        return cls(**obj)


class Gateway:
    """Single-node durable state machine with state-delta oracles and chained audit."""
    def __init__(self, db: str | Path):
        self.db = str(db)
        Path(self.db).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as c:
            c.executescript('''
            CREATE TABLE IF NOT EXISTS inventory (
                tenant TEXT NOT NULL, sku TEXT NOT NULL,
                available INTEGER NOT NULL CHECK(available >= 0),
                reserved INTEGER NOT NULL CHECK(reserved >= 0),
                PRIMARY KEY (tenant,sku));
            CREATE TABLE IF NOT EXISTS orders (
                tenant TEXT NOT NULL, order_id TEXT NOT NULL, sku TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                status TEXT NOT NULL CHECK(status IN ('reserved','released','shipped')),
                PRIMARY KEY (tenant,order_id));
            CREATE TABLE IF NOT EXISTS receipts (
                tenant TEXT NOT NULL, request_id TEXT NOT NULL,
                command_hash TEXT NOT NULL, response TEXT NOT NULL,
                PRIMARY KEY (tenant,request_id));
            CREATE TABLE IF NOT EXISTS audit (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant TEXT NOT NULL, event TEXT NOT NULL,
                prev_hash TEXT NOT NULL, event_hash TEXT NOT NULL);
            ''')

    def connect(self):
        c = sqlite3.connect(self.db, timeout=10, isolation_level=None)
        c.row_factory = sqlite3.Row
        c.execute('PRAGMA busy_timeout=10000')
        c.execute('PRAGMA foreign_keys=ON')
        return c

    def seed(self, tenant='demo', sku='PART-A', quantity=20):
        if quantity < 0:
            raise ValueError('negative stock')
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            if c.execute('SELECT 1 FROM inventory WHERE tenant=? AND sku=?', (tenant, sku)).fetchone():
                c.rollback()
                raise ValueError('already seeded')
            c.execute('INSERT INTO inventory VALUES (?,?,?,0)', (tenant, sku, quantity))
            c.commit()

    def snapshot(self, tenant: str) -> dict:
        with self.connect() as c:
            return self._snapshot(c, tenant)

    @staticmethod
    def _snapshot(c, tenant):
        inventory = [dict(r) for r in c.execute(
            'SELECT sku,available,reserved FROM inventory WHERE tenant=? ORDER BY sku', (tenant,))]
        orders = [dict(r) for r in c.execute(
            'SELECT order_id,sku,quantity,status FROM orders WHERE tenant=? ORDER BY order_id', (tenant,))]
        return {'inventory': inventory, 'orders': orders}

    @staticmethod
    def _policy(cmd: Command, roles: dict[str, list[str]]) -> str | None:
        role = roles.get(cmd.actor, [])
        if cmd.action in ('reserve', 'release') and 'operator' not in role and 'admin' not in role:
            return 'actor not permitted'
        if cmd.action == 'ship' and 'shipper' not in role and 'admin' not in role:
            return 'actor not permitted'
        if cmd.action == 'ship' and cmd.quantity > 5 and not cmd.approval:
            return 'high-impact shipment requires approval'
        return None

    def execute(self, obj: dict, roles: dict[str, list[str]], fault: str | None = None) -> dict:
        """fault is test-only: before_commit or after_commit (simulates lost ACK)."""
        cmd = Command.parse(obj)
        if fault not in (None, 'before_commit', 'after_commit'):
            raise ValueError('unknown fault')
        command_hash = digest(asdict(cmd))
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            old = c.execute('SELECT command_hash,response FROM receipts WHERE tenant=? AND request_id=?',
                            (cmd.tenant, cmd.request_id)).fetchone()
            if old:
                if old['command_hash'] != command_hash:
                    c.rollback()
                    raise ValueError('idempotency key reused with different payload')
                response = json.loads(old['response'])
                c.commit()
                return {**response, 'replayed': True}
            before = self._snapshot(c, cmd.tenant)
            policy_error = self._policy(cmd, roles)
            error = policy_error
            if not error:
                try:
                    self._mutate(c, cmd)
                except ValueError as exc:
                    error = str(exc)
            after = self._snapshot(c, cmd.tenant)
            if error and before != after:
                c.rollback()
                raise AssertionError('rejected command mutated state')
            self._invariants(c, cmd.tenant)
            if fault == 'before_commit':
                c.rollback()
                raise ConnectionError('injected failure before commit')
            response = {
                'request_id': cmd.request_id, 'tenant': cmd.tenant,
                'status': 'rejected' if error else 'committed',
                'reason': error, 'before_hash': digest(before),
                'after_hash': digest(after), 'changed': before != after,
                'replayed': False,
            }
            c.execute('INSERT INTO receipts VALUES (?,?,?,?)',
                      (cmd.tenant, cmd.request_id, command_hash, canonical(response)))
            prior = c.execute('SELECT event_hash FROM audit ORDER BY seq DESC LIMIT 1').fetchone()
            prev_hash = prior['event_hash'] if prior else 'GENESIS'
            event = {'command_hash': command_hash, 'receipt': response}
            event_hash = digest({'prev_hash': prev_hash, 'event': event})
            c.execute('INSERT INTO audit(tenant,event,prev_hash,event_hash) VALUES (?,?,?,?)',
                      (cmd.tenant, canonical(event), prev_hash, event_hash))
            c.commit()
        if fault == 'after_commit':
            raise ConnectionError('injected lost acknowledgement after commit')
        return response

    @staticmethod
    def _mutate(c, cmd: Command):
        stock = c.execute('SELECT available,reserved FROM inventory WHERE tenant=? AND sku=?',
                          (cmd.tenant, cmd.sku)).fetchone()
        if not stock:
            raise ValueError('unknown sku')
        order = c.execute('SELECT sku,quantity,status FROM orders WHERE tenant=? AND order_id=?',
                          (cmd.tenant, cmd.order_id)).fetchone()
        if cmd.action == 'reserve':
            if order:
                raise ValueError('order already exists')
            if stock['available'] < cmd.quantity:
                raise ValueError('insufficient stock')
            c.execute('UPDATE inventory SET available=available-?,reserved=reserved+? WHERE tenant=? AND sku=?',
                      (cmd.quantity, cmd.quantity, cmd.tenant, cmd.sku))
            c.execute("INSERT INTO orders VALUES (?,?,?,?, 'reserved')",
                      (cmd.tenant, cmd.order_id, cmd.sku, cmd.quantity))
        else:
            if not order or order['status'] != 'reserved':
                raise ValueError('order not in reserved state')
            if order['sku'] != cmd.sku or order['quantity'] != cmd.quantity:
                raise ValueError('order parameters mismatch')
            if cmd.action == 'release':
                c.execute('UPDATE inventory SET available=available+?,reserved=reserved-? WHERE tenant=? AND sku=?',
                          (cmd.quantity, cmd.quantity, cmd.tenant, cmd.sku))
                status = 'released'
            else:
                c.execute('UPDATE inventory SET reserved=reserved-? WHERE tenant=? AND sku=?',
                          (cmd.quantity, cmd.tenant, cmd.sku))
                status = 'shipped'
            c.execute('UPDATE orders SET status=? WHERE tenant=? AND order_id=?',
                      (status, cmd.tenant, cmd.order_id))

    @staticmethod
    def _invariants(c, tenant):
        rows = c.execute('SELECT sku,reserved FROM inventory WHERE tenant=?', (tenant,)).fetchall()
        for row in rows:
            total = c.execute("SELECT COALESCE(SUM(quantity),0) AS n FROM orders WHERE tenant=? AND sku=? AND status='reserved'",
                              (tenant, row['sku'])).fetchone()['n']
            if total != row['reserved']:
                raise AssertionError('reservation accounting invariant violated')

    def verify(self) -> dict:
        with self.connect() as c:
            previous = 'GENESIS'
            count = 0
            for row in c.execute('SELECT * FROM audit ORDER BY seq'):
                event = json.loads(row['event'])
                expected = digest({'prev_hash': previous, 'event': event})
                if row['prev_hash'] != previous or row['event_hash'] != expected:
                    return {'ok': False, 'events': count, 'reason': 'audit chain mismatch'}
                receipt = c.execute('SELECT response FROM receipts WHERE tenant=? AND request_id=?',
                                    (row['tenant'], event['receipt']['request_id'])).fetchone()
                if not receipt or json.loads(receipt['response']) != event['receipt']:
                    return {'ok': False, 'events': count, 'reason': 'receipt mismatch'}
                previous = expected
                count += 1
            for row in c.execute('SELECT DISTINCT tenant FROM inventory'):
                self._invariants(c, row['tenant'])
                last = c.execute('SELECT event FROM audit WHERE tenant=? ORDER BY seq DESC LIMIT 1',
                                 (row['tenant'],)).fetchone()
                if last and json.loads(last['event'])['receipt']['after_hash'] != digest(self._snapshot(c, row['tenant'])):
                    return {'ok': False, 'events': count, 'reason': 'live state diverges from committed receipt'}
            return {'ok': True, 'events': count, 'tip': previous}