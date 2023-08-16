"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import shutil
import sys

import click

from apt_ostree.cmd.options import feed_option
from apt_ostree.cmd.options import packages_option
from apt_ostree.cmd.options import release_option
from apt_ostree.cmd import pass_state_context
from apt_ostree.log import complete_step
from apt_ostree.repo import Repo


@click.command(help="Remove debian package(s) from reposiotry")
@pass_state_context
@feed_option
@release_option
@packages_option
def remove(state, feed, release, packages):
    if shutil.which("reprepro") is None:
        click.secho("reprepro was not found in your $PATH")
        sys.exit(0)

    with complete_step(
            f"Removing packages from {state.feed}"):
        Repo(state).remove()
