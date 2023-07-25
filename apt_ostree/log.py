"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import logging

from rich.console import Console
from rich.logging import RichHandler

logger = logging.getLogger("apt-ostree")


def init_logging():
    """Initialize logging for apt-ostree"""
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]",
        handlers=[RichHandler(
            show_path=False,
            show_time=False,
            show_level=False,
            markup=True,
            rich_tracebacks=True,
            console=Console(),
        )]
    )


def edebug(msg):
    logger.debug(msg)
