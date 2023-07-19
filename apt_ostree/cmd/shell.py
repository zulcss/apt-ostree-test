"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.cmd.version import version


@click.group(
    help="\nHyrbid image/package management system."
)
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)


def main():
    cli(prog_name="apt-ostree")


cli.add_command(version)
