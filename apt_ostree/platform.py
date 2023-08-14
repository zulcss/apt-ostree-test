"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""


import os

import apt

from apt_ostree.constants import excluded_packages
from apt_ostree.log import complete_step


def create_tmpfile_dir(rootdir):
    """Ensure directoeies in /var are created."""
    with complete_step("Creating systemd-tmpfiles configuration"):
        cache = apt.cache.Cache(rootdir=rootdir)
        dirs = []
        for pkg in cache:
            if "/var" in pkg.installed_files and \
                pkg.name not in excluded_packages:
                dirs += [file for file in pkg.installed_files
                         if file.startswith("/var")]
        if len(dirs) == 0:
            return
        conf = rootdir.joinpath(
            "usr/lib/tmpfiles.d/ostree-integration-autovar.conf")
        if conf.exists():
            os.unlink(conf)
        with open(conf, "w") as f:
            f.write("# Auto-genernated by apt-ostree\n")
            for d in (dirs):
                if d not in [
                        "/var",
                        "/var/lock",
                        "/var/cache",
                        "/var/spool",
                        "/var/log",
                        "/var/lib"]:
                    f.write(f"L {d} - - - - ../../usr/rootdirs{d}\n")
