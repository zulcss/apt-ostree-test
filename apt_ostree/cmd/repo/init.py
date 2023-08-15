"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import shutil
import sys

import click


from apt_ostree.cmd.options import feed_option
from apt_ostree.cmd.options import origin_option
from apt_ostree.cmd.options import release_option
from apt_ostree.cmd import pass_state_context
from apt_ostree.log import complete_step
from apt_ostree.repo import Repo


@click.command(help="Create a Debian package repsoitory.")
@pass_state_context
@feed_option
@release_option
@origin_option
def init(state, feed, release, origin):
    if shutil.which("reprepro") is None:
        click.secho("reprepro was not found in your $PATH")
        sys.exit(0)

    with complete_step(
            f"Creating Debian package repository in {state.feed}."):
        Repo(state).init()
