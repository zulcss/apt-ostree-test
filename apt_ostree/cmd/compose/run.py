"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.cmd.options import branch_option
from apt_ostree.cmd.options import commands_argument
from apt_ostree.cmd.options import edit_option
from apt_ostree.cmd.options import repo_option
from apt_ostree.cmd import pass_state_context
from apt_ostree.deploy import Deployment


@click.command(name="exec", help="One shot command in an ostree branch")
@pass_state_context
@repo_option
@branch_option
@edit_option
@commands_argument
def run(state, repo, branch, edit, commands):
    Deployment(state).run_command()
