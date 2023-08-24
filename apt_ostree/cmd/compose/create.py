"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import shutil
import sys

import click

from apt_ostree.bootstrap import create_ostree
from apt_ostree.cmd.options import compose_options
from apt_ostree.cmd import pass_state_context
from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.ostree import Ostree
from apt_ostree.utils import run_command


@click.command(short_help="Create treefile")
@pass_state_context
@compose_options
def create(state, repo, base, branch, edit):
    if state.repo is None:
        click.secho("You did not supply an ostree repository", fg="red")
        sys.exit(1)

    Ostree(state).ostree_init()

    if state.branch is None:
        click.secho("You did not supply an ostree branch.", fg="red")
        sys.exit(1)
    click.secho(f"Found ostree branch: {state.branch}")

    if state.base is None:
        click.secho("You did not supply a configuration directory.", fg="red")
        sys.exit(1)
    if not state.base.exists():
        click.secho("Configuration directory does not exist.", fg="red")
        sys.exit(1)
    else:
        click.secho(f"Found configuration directory: {state.base}")

    config = state.base.joinpath("bootstrap.yaml")
    if not config.exists():
        click.sceho("bootstrap.yaml does not exist.", fg="red")
        sys.exit(1)
    else:
        click.secho("Found configuration file bootstrap.yaml.")

    with complete_step(f"Setting up workspace for {branch}."):
        workspace = state.workspace
        workdir = workspace.joinpath(f"build/{branch}")
        rootfs = workdir.joinpath("rootfs")

        log_step(f"Building workspace for {branch} in {workspace}")
        if workdir.exists():
            log_step("Found working directory from previous run...removing.")
            shutil.rmtree(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        rootfs.mkdir(parents=True, exist_ok=True)

        log_step("Running bdebstrap, please wait.")
        verbosity = "-q"
        if state.debug:
            verbosity = "-v"
        run_command(
            ["bdebstrap", "-c", "bootstrap.yaml", verbosity,
             "--force", "--name", str(state.branch), "--target", str(rootfs),
             "--output", str(workdir)], cwd=state.base)

    create_ostree(rootfs)
    Ostree(state).ostree_commit(
        rootfs,
        subject="Commit by apt-ostree",
        msg="Initialized by apt-ostree")
    shutil.rmtree(rootfs)
