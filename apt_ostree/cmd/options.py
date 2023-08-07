"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import pathlib

import click

from apt_ostree.cmd import State


def debug_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.debug = value
        return value
    return click.option(
        "--debug",
        is_flag=True,
        help="Increase verbosity",
        callback=callback
    )(f)


def workspace_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.workspace = pathlib.Path(value)
        return value
    return click.option(
        "--workspace",
        help="Path to the apt-ostree workspace",
        nargs=1,
        default="/var/tmp/apt-ostree",
        required=True,
        callback=callback
    )(f)


def repo_option(f):
    """ostree repo path option"""
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.repo = pathlib.Path(value)
        return value
    return click.option(
        "--repo",
        help="Path to the Ostree Repository",
        nargs=1,
        required=True,
        callback=callback
    )(f)


def base_option(f):
    """apt-ostree configuration directory option"""
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.base = pathlib.Path(value)
        return value
    return click.option(
        "--base",
        help="Path to the apt-ostree configuration directory",
        nargs=1,
        required=True,
        callback=callback
    )(f)


def branch_option(f):
    """ostree branch option"""
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.branch = value
        return value
    return click.argument(
        "branch",
        nargs=1,
        callback=callback
    )(f)


def compose_options(f):
    f = repo_option(f)
    f = base_option(f)
    f = branch_option(f)
    return f
