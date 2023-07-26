"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import os
import sys

import click


@click.group(help="Commands to build ostree repo/image")
@click.pass_context
def compose(ctxt):
    if os.getuid() != 0:
        print("You are not root.")
        sys.exit(-1)
