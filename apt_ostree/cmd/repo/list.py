"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import shutil
import sys

import click

from apt_ostree.cmd.options import feed_option
from apt_ostree.cmd.options import release_option
from apt_ostree.cmd import pass_state_context
from apt_ostree.repo import Repo


@click.command(name="list", help="List package(s) in repository")
@pass_state_context
@feed_option
@release_option
def show(state, feed, release):
    if shutil.which("reprepro") is None:
        click.secho("reprepro was not found in your $PATH")
        sys.exit(0)

    Repo(state).show()
