"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.utils import run_command


def ostree_commit(state,
                  rootfs,
                  subject=None,
                  msg=None):
    """Commit rootfs to ostree repository."""
    cmd = ["ostree", "commit", f"--repo={state.repo}"]
    if state.edit:
        cmd += ["-e"]
    else:
        if subject:
            cmd += [f"--subject={subject}"]
        if msg:
            cmd += [f"--body={msg}"]

    cmd += [f"--branch={state.branch}", str(rootfs)]
    with complete_step(f"Committing {state.branch} to {state.repo}"):
        r = run_command(cmd)
        if r.returncode != 0:
            click.secho(
                f"Failed to commit {state.branch}  to {state.repo}.",
                fg="red")
            raise

        log_step(f"Succesfully commited {state.branch} to {state.repo}.")
