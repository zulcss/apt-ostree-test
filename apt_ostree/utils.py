"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import os
import subprocess

import click

from apt_ostree.log import log_step


def run_command(cmd,
                debug=False,
                stdin=None,
                stdout=None,
                stderr=None,
                check=True,
                env={},
                cwd=None):
    env = dict(
        PATH=os.environ["PATH"],
        TERM=os.getenv("TERM", "vt220"),
        LANG="C.UTF-8",
    ) | env
    try:
        if debug:
            log_step(f"Running {' '.join(cmd)}")
        return subprocess.run(
            cmd,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            env=env,
            cwd=cwd,
            check=check,
        )
    except FileNotFoundError:
        click.secho(f"{cmd[0]} not found in PATH.")
    except subprocess.CalledProcessError as e:
        click.secho("Failed to run command.")
        click.secho(
            f"Error Code: {e.returncode}, Error message: {e.output}")
