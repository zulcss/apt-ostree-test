# -*- coding: utf-8 -*-

from apt_ostree.tests import base
from apt_ostree.cmd.shell import cli
from click.testing import CliRunner


class Test_apt_cli(base.TestCase):

    def test_something(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
