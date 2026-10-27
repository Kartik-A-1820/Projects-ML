"""Run deterministic local scenario, benchmark, or command from CLI."""
import argparse
import json
from .core import Gateway
from .eval import ROLES, write_report
from .planner import deterministic_plan


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', default='artifacts/state.sqlite')
    sub = p.add_subparsers(dest='action', required=True)
    seed = sub.add_parser('seed')
    seed.add_argument('--quantity', type=int, default=20)
    act = sub.add_parser('act')
    act.add_argument('--text', required=True)
    act.add_argument('--request-id', required=True)
    act.add_argument('--actor', default='alice')
    sub.add_parser('verify')
    sub.add_parser('snapshot')
    bench = sub.add_parser('benchmark')
    bench.add_argument('--output', default='reports/benchmark.json')
    args = p.parse_args()
    if args.action == 'benchmark':
        result = write_report(args.output)
    else:
        g = Gateway(args.db)
        if args.action == 'seed':
            g.seed(quantity=args.quantity)
            result = {'seeded': args.quantity}
        elif args.action == 'act':
            command = deterministic_plan(args.text, tenant='demo', actor=args.actor, request_id=args.request_id)
            result = g.execute(command, ROLES)
        elif args.action == 'verify':
            result = g.verify()
        else:
            result = g.snapshot('demo')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()