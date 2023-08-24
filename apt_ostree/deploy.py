"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import os
import shutil
import subprocess
import sys

from rich.console import Console

from apt_ostree.ostree import Ostree
from apt_ostree.platform import create_tmpfile_dir
from apt_ostree.utils import run_sandbox_command


class Deployment:
    def __init__(self, state):
        self.state = state
        self.console = Console()
        self.ostree = Ostree(state)

        self.workspace = self._create_deployment_workspace()
        self.branch = self.state.branch

    def run_command(self):
        """Run a a command in a rootfs and commit thee result."""
        commit = self.ostree.ostree_ref(self.branch)
        if commit:
            with self.console.status(f"Checking out {commit[:10]}..."):
                self._create_rootfs(commit)
                r = self.ostree.ostree_checkout(commit, self.rootfs)
                if r.returncode != 0:
                    self.console.print(
                        f"[red]Error[/red] Failed to checkout {self.branch}")
                    sys.exit(1)
                os.unlink(self.rootfs.joinpath("usr/etc/resolv.conf"))
                run_sandbox_command(
                ["systemd-tmpfiles", "--create", "--boot"],
                self.rootfs,
                )

            self.console.print("Running apt-get update.")
            run_sandbox_command(
                ["apt", "update"],
                self.rootfs,
            )

            run_sandbox_command(list(self.state.commands), self.rootfs)

            self.console.print("Upding /usr/rootdirs/var.")
            create_tmpfile_dir(self.rootfs)
            self.console.print("Cleaning up rootfs")
            shutil.rmtree(self.rootfs.joinpath("etc"))
            self.console.print(f"Committing to {self.state.branch}.")
            self.ostree.ostree_commit(
                self.rootfs, subject="created by exec",
                msg=f"{' '.join(list(self.state.commands))}")

    def _create_deployment_workspace(self):
        """Create a deployment workspace"""
        workdir = self.state.workspace.joinpath(
            f"deployment/{self.state.branch}")
        workdir.mkdir(parents=True, exist_ok=True)
        return workdir

    def _create_rootfs(self, commit):
        """Create a temporary rootfs."""
        self.rootfs = self.workspace.joinpath(commit)
        if self.rootfs.exists():
            self.console.print("Found previous directory...removing.")
            shutil.rmtree(self.rootfs)
