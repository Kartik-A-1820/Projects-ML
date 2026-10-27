"""Executable-contract evaluation: check final state, not agent/tool claims."""
import json
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .core import Gateway

ROLES = {'alice': ['operator'], 'bob': ['shipper'], 'admin': ['admin'], 'guest': []}


def cmd(request_id, action, qty=2, order='O1', actor='alice', tenant='demo'):
    return {'request_id': request_id, 'tenant': tenant, 'actor': actor, 'action': action,
            'order_id': order, 'sku': 'PART-A', 'quantity': qty}


def scenario_suite():
    with tempfile.TemporaryDirectory() as directory:
        gate = Gateway(Path(directory) / 'eval.sqlite')
        gate.seed(quantity=12)
        traces = []
        def run(command, fault=None):
            start = time.perf_counter()
            try:
                outcome = gate.execute(command, ROLES, fault=fault)
            except ConnectionError:
                outcome = {'status': 'transport_error'}
            traces.append({'action': command['action'], 'fault': fault,
                           'status': outcome['status'], 'latency_ms': (time.perf_counter()-start)*1000})
            return outcome
        assert run(cmd('r1','reserve',4))['status'] == 'committed'
        assert run(cmd('r1','reserve',4))['replayed']
        assert run(cmd('r2','ship',4,actor='bob'))['status'] == 'committed'
        assert run(cmd('r3','reserve',100))['status'] == 'rejected'
        assert run(cmd('r4','reserve',1,actor='guest'))['status'] == 'rejected'
        assert run(cmd('r5','reserve',2,order='O2'), 'before_commit')['status'] == 'transport_error'
        assert run(cmd('r5','reserve',2,order='O2'))['status'] == 'committed'
        assert run(cmd('r6','reserve',2,order='O3'), 'after_commit')['status'] == 'transport_error'
        assert run(cmd('r6','reserve',2,order='O3'))['replayed']
        snap = gate.snapshot('demo')
        assert snap['inventory'][0]['available'] == 4
        assert snap['inventory'][0]['reserved'] == 4
        verified = gate.verify()
        assert verified['ok']
        return {'traces': traces, 'final_snapshot': snap, 'verification': verified,
                'scenario_pass_rate': 1.0,
                'note': 'Deterministic fixture checks; not an LLM task-success estimate.'}


def concurrency_benchmark(workers=8, requests=30):
    with tempfile.TemporaryDirectory() as directory:
        gate = Gateway(Path(directory) / 'parallel.sqlite')
        gate.seed(quantity=10)
        start = time.perf_counter()
        def one(i):
            return gate.execute(cmd(f'c{i}','reserve',1,order=f'ORDER{i}'), ROLES)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(one, range(requests)))
        elapsed = time.perf_counter()-start
        accepted = sum(r['status']=='committed' for r in results)
        snapshot = gate.snapshot('demo')
        assert accepted == 10 and snapshot['inventory'][0]['available'] == 0
        return {'requests': requests, 'workers': workers, 'accepted': accepted,
                'rejected': requests-accepted, 'seconds': round(elapsed,4),
                'throughput_rps': round(requests/elapsed,2), 'verified': gate.verify()['ok']}


def write_report(path):
    result = {'scenario': scenario_suite(), 'concurrency': concurrency_benchmark()}
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2))
    return result