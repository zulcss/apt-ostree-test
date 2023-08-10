"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import shutil

import click

from apt_ostree.cmd.options import compose_options
from apt_ostree.cmd import pass_state_context
from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.utils import run_command


@click.command(help="Create an raw image from ostree branch")
@pass_state_context
@compose_options
def image(state, repo, base, branch):
    click.secho(f"Found ostree repository: {state.repo}")
    click.secho(f"Found ostree branch: {state.branch}")
    with complete_step(f"Setting up workspace for {state.branch}"):
        workdir = state.workspace.joinpath(f"build/{state.branch}")
        img_dir = workdir.joinpath("image")
        ostree_repo = img_dir.joinpath("ostree_repo")
        if img_dir.exists():
            shutil.rmtree(img_dir)
        shutil.copytree(
            state.base.joinpath("image"),
            img_dir, dirs_exist_ok=True)

    with complete_step("Creating local ostree repository"):
        log_step("Creating image build repository")
        run_command(
            ["ostree", "init", f"--repo={str(ostree_repo)}"],
            cwd=img_dir)
        log_step(f"Pulling {state.branch} in image build repository")
        run_command(
            ["ostree", "pull-local", f"--repo={str(ostree_repo)}",
             str(state.repo), str(state.branch)],
            cwd=img_dir)
        log_step("Running debos...")

        cmd = ["debos",
               "-t", f"branch:{state.branch}",
               ]
        if state.debug:
            cmd += ["-v"]
        cmd += ["image.yaml"]

        run_command(cmd, cwd=img_dir)

    click.secho(f"Image can be found in {img_dir}")
