"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import logging

import click

from apt_ostree.cmd.compose import compose
from apt_ostree.cmd.version import version
from apt_ostree.log import edebug
from apt_ostree.log import init_logging


@click.group(
    help="\nHyrbid image/package management system."
)
@click.option(
    "--debug",
    is_flag=True,
    help="Turn on debugging mode."
)
@click.pass_context
def cli(ctx: click.Context, debug):
    init_logging()

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        edebug("Debug turned on.")

    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug


def main():
    cli(prog_name="apt-ostree")


cli.add_command(compose)
cli.add_command(version)
