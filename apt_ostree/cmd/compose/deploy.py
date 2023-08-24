"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""
import click

from apt_ostree.cmd.options import branch_argument
from apt_ostree.cmd.options import edit_option
from apt_ostree.cmd.options import parent_option
from apt_ostree.cmd.options import repo_option
from apt_ostree.cmd import pass_state_context
from apt_ostree.deploy import Deployment


@click.command(short_help="Ostree operations")
@pass_state_context
@repo_option
@parent_option
@edit_option
@branch_argument
def deploy(state, repo, parent, edit, branch):
    if parent:
        Deployment(state).create_parent()
