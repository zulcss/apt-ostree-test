"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.utils import run_command


class Ostree:
    """Ostree operations"""

    def __init__(self, state):
        self.state = state
        self.repo = self.state.repo
        self.branch = self.state.branch
        self.edit = self.state.edit

    def ostree_init(self):
        """Iniatialize an empty ostree repository."""
        if not self.repo.exists():
            click.secho(f"Creating f{self.repo}")
            run_command(["ostree", "init", f"--repo={self.repo}",
                         "--mode=archive-z2"])

    def ostree_commit(self,
                      rootfs,
                      subject=None,
                      msg=None):
        """Commit rootfs to ostree repository."""
        cmd = ["ostree", "commit", f"--repo={self.repo}"]
        if self.edit:
            cmd += ["-e"]
        else:
            if subject:
                cmd += [f"--subject={subject}"]
            if msg:
                cmd += [f"--body={msg}"]

        cmd += [f"--branch={self.branch}", str(rootfs)]
        with complete_step(f"Committing {self.branch} to {self.repo}"):
            r = run_command(cmd)
            if r.returncode != 0:
                click.secho(
                    f"Failed to commit {self.branch}  to {self.repo}.",
                    fg="red")
                raise

            log_step(f"Succesfully commited {self.branch} to {self.repo}.")
