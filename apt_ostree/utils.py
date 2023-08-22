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


def run_sandbox_command(
    args,
    rootfs,
    stdin=None,
    stdout=None,
    stderr=None,
    check=True,
    env={},
):
    """Run command wrapped in bubblewrap"""
    cmd = [
        "bwrap",
        "--dev", "/dev",
        "--proc", "/proc",
        "--dir", "/run",
        "--chdir", "/",
        "--die-with-parent",
        "--unshare-pid",
        "--unshare-uts",
        "--unshare-ipc",
        "--unshare-cgroup-try",
        "--ro-bind", "/sys/block", "/sys/block",
        "--ro-bind", "/sys/bus", "/sys/bus",
        "--ro-bind", "/sys/class", "/sys/class",
        "--ro-bind", "/sys/dev", "/sys/dev",
        "--ro-bind", "/sys/devices", "/sys/devices",
        "--share-net",
        "--symlink", "usr/lib", "/lib",
        "--symlink", "usr/lib64", "/lib64",
        "--symlink", "usr/bin", "/bin",
        "--symlink", "usr/sbin", "/sbin",
        "--bind", f"{rootfs}/usr", "/usr",
        "--bind", f"{rootfs}/usr/etc", "/etc",
        "--bind", f"{rootfs}/usr/rootdirs/var", "/var",
        "--bind", "/tmp", "/tmp",
    ]

    cmd += args

    run_command(
        cmd,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        check=check,
        env=env,
    )
