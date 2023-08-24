"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.cmd.compose.create import create
from apt_ostree.cmd.compose.image import image
from apt_ostree.cmd.compose.run import run


@click.group(help="Commands to build ostree repo/image")
@click.pass_context
def compose(ctxt):
    pass


compose.add_command(create)
compose.add_command(image)
compose.add_command(run)
