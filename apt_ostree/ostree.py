"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.utils import run_command


def ostree_commit(repo, branch, rootfs):
    """Commit directory to ostree repository"""
    with complete_step(f"Committing {branch} to {repo}"):
        r = run_command(
            ["ostree", "commit", f"--repo={repo}",
             f"--branch={branch}", str(rootfs)],
        )
        if r.returncode != 0:
            click.secho(f"Failed to commit to ostree.", fg="red")
            raise

        log_step(f"Succesfully commited {branch} to {repo}.")
