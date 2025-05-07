#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argcomplete, argparse
import time

# Heavy imports
import pandas as pd
import numpy as np

def simulate_workload(name, delay=2):
    print(f"\n[⏳] Executing '{name}'... please wait {delay} seconds.")
    time.sleep(delay)
    print("[✅] Done.\n")

def print_info(context, options):
    print("====== Execution Summary ======")
    print(f"Command   : {context}")
    for key, value in options.items():
        print(f"{key.capitalize():10}: {value}")
    print("================================")

def handle_build(args):
    simulate_workload("build", delay=args.delay)
    print_info("build", vars(args))

def handle_deploy_staging(args):
    simulate_workload("deploy staging", delay=args.delay)
    print_info("deploy staging", vars(args))

def handle_deploy_production(args):
    simulate_workload("deploy production", delay=args.delay)
    print_info("deploy production", vars(args))

parser = argparse.ArgumentParser(description="🚀 Sample CLI Tool")
subparsers = parser.add_subparsers(dest="command", required=True)

# build command
build_parser = subparsers.add_parser("build", help="Build the project")
build_parser.add_argument("--delay", type=int, default=2, help="Delay in seconds")
build_parser.add_argument("--config", type=str, default="default.cfg", help="Path to config file")
build_parser.set_defaults(func=handle_build)

# deploy command
deploy_parser = subparsers.add_parser("deploy", help="Deploy the project")
deploy_subparsers = deploy_parser.add_subparsers(dest="environment", required=True)

# deploy staging
staging_parser = deploy_subparsers.add_parser("staging", help="Deploy to staging")
staging_parser.add_argument("--delay", type=int, default=3, help="Delay in seconds")
staging_parser.add_argument("--version", type=str, default="latest", help="Version to deploy")
staging_parser.set_defaults(func=handle_deploy_staging)

# deploy production
prod_parser = deploy_subparsers.add_parser("production", help="Deploy to production")
prod_parser.add_argument("--delay", type=int, default=5, help="Delay in seconds")
prod_parser.add_argument("--version", type=str, default="latest", help="Version to deploy")
prod_parser.set_defaults(func=handle_deploy_production)

argcomplete.autocomplete(parser)
args = parser.parse_args()
args.func(args)
