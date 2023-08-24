"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import subprocess
import sys

import click

from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.utils import run_command


class Ostree:
    def __init__(self, state):
        self.state = state

    def ostree_init(self):
        """Initialize an ostree repository."""
        if not self.state.repo.exists():
            click.secho(f"Creating ostree repository: {self.state.repo}")
            run_command(["ostree", "init", f"--repo={self.state.repo}",
                        "--mode=archive-z2"])

    def ostree_commit(self,
                      rootfs,
                      parent=None,
                      subject=None,
                      msg=None):
        """Commit rootfs to ostree repository."""
        cmd = ["ostree", "commit", f"--repo={self.state.repo}"]
        if self.state.edit:
            cmd += ["-e"]
        else:
            if subject:
                cmd += [f"--subject={subject}"]
            if msg:
                cmd += [f"--body={msg}"]

        if parent:
            cmd += [f"--parent={parent}"]

        cmd += [f"--branch={self.state.branch}",
                f"--tree=dir={str(rootfs)}"]
        with complete_step(
                f"Committing {self.state.branch} to {self.state.repo}"):
            r = run_command(cmd)
            if r.returncode != 0:
                click.secho(
                    f"Failed to commit {self.state.branch} "
                    f"to {self.state.repo}.",
                    fg="red")
                raise

            log_step(
                f"Succesfully commited {self.state.branch} "
                f"to {self.state.repo}.")

    def ostree_ref(self, branch):
        r = run_command(
            ["ostree", f"--repo={str(self.state.repo)}", "rev-parse", branch],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        msg = r.stdout.strip()
        if r.returncode != 0:
            click.secho(
                f"Unable to determine {branch} in {self.state.repo}", fg="red")
            sys.exit(1)

        return msg.decode("utf-8")

    def ostree_checkout(self, commit, rootfs):
        return run_command(
            ["ostree", "checkout",
                f"--repo={self.state.repo}", commit, str(rootfs)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def ostree_update(self):
        """Update the summary metadata"""
        return run_command(
            ["ostree", "summary",
             "f--repo={self.state.repo", "-u"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
