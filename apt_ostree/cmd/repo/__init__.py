"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.cmd.repo.init import init


@click.group(help="Commands to create/manage Debian package repository")
@click.pass_context
def repo(ctxt):
    pass


repo.add_command(init)
