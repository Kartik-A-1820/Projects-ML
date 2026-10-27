from concurrent.futures import ThreadPoolExecutor
import json
import pytest
from contracttrace.core import Command, Gateway
from contracttrace.eval import ROLES, cmd, scenario_suite, concurrency_benchmark
from contracttrace.planner import deterministic_plan, bind_proposal


@pytest.fixture
def gate(tmp_path):
    g = Gateway(tmp_path/'db.sqlite')
    g.seed(quantity=10)
    return g


def test_command_validation():
    with pytest.raises(ValueError):
        Command.parse({**cmd('r','reserve'), 'quantity': True})
    with pytest.raises(ValueError):
        Command.parse({**cmd('r','delete'), 'action': 'delete'})


def test_replay_and_conflict(gate):
    request = cmd('r1','reserve',3)
    assert gate.execute(request, ROLES)['changed']
    assert gate.execute(request, ROLES)['replayed']
    with pytest.raises(ValueError):
        gate.execute({**request, 'quantity': 4}, ROLES)
    assert gate.snapshot('demo')['inventory'][0]['available'] == 7


def test_ship_and_release(gate):
    gate.execute(cmd('r1','reserve',2), ROLES)
    assert gate.execute(cmd('r2','ship',2,actor='bob'), ROLES)['status']=='committed'
    assert gate.execute(cmd('r3','release',2), ROLES)['status']=='rejected'
    assert gate.verify()['ok']


def test_policy_denies_and_no_mutation(gate):
    before = gate.snapshot('demo')
    result = gate.execute(cmd('r1','reserve',1,actor='guest'), ROLES)
    assert result['status']=='rejected'
    assert before == gate.snapshot('demo')


def test_approval(gate):
    gate.execute(cmd('r1','reserve',6), ROLES)
    assert gate.execute(cmd('r2','ship',6,actor='bob'), ROLES)['status']=='rejected'
    approved = {**cmd('r3','ship',6,actor='bob'), 'approval': True}
    assert gate.execute(approved, ROLES)['status']=='committed'


def test_fault_before_commit(gate):
    request = cmd('r1','reserve',2)
    with pytest.raises(ConnectionError):
        gate.execute(request, ROLES, fault='before_commit')
    assert gate.snapshot('demo')['inventory'][0]['available'] == 10
    assert gate.execute(request, ROLES)['status']=='committed'


def test_lost_ack_idempotent(gate):
    request = cmd('r1','reserve',2)
    with pytest.raises(ConnectionError):
        gate.execute(request, ROLES, fault='after_commit')
    assert gate.execute(request, ROLES)['replayed']
    assert gate.snapshot('demo')['inventory'][0]['available'] == 8


def test_audit_tampering(gate):
    gate.execute(cmd('r1','reserve',1), ROLES)
    assert gate.verify()['ok']
    with gate.connect() as c:
        c.execute("UPDATE audit SET event_hash='tampered' WHERE seq=1")
    assert not gate.verify()['ok']


def test_tenant_isolation(gate):
    gate.seed(tenant='other',quantity=5)
    gate.execute(cmd('r1','reserve',2), ROLES)
    assert gate.snapshot('other')['inventory'][0]['available']==5


def test_planner_and_schema():
    command = deterministic_plan('reserve 2 units of PART-A for O1',tenant='demo',actor='alice',request_id='r1')
    assert command['quantity']==2
    with pytest.raises(ValueError):
        deterministic_plan('please delete all orders',tenant='demo',actor='alice',request_id='r2')
    with pytest.raises(ValueError):
        bind_proposal({'action':'reserve','sku':'PART-A','order_id':'O1','quantity':1,'tenant':'evil'},
                      tenant='demo',actor='alice',request_id='r3')


def test_suite():
    assert scenario_suite()['verification']['ok']


def test_concurrency():
    assert concurrency_benchmark(workers=8,requests=30)['accepted']==10


def test_live_state_tampering(gate):
    gate.execute(cmd('r1','reserve',1), ROLES)
    with gate.connect() as c:
        c.execute("UPDATE inventory SET available=available+1 WHERE tenant='demo'")
    assert gate.verify()['ok'] is False
