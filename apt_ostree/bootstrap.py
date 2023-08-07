"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import hashlib
import os
import shutil

from apt_ostree.log import complete_step
from apt_ostree.log import log_step


def create_ostree(rootdir):
    """Create an ostree branch from a rootfs."""
    with complete_step(f"Creating ostree from {rootdir}."):
        log_step("Setting up /usr/lib/ostree-boot")
        setup_boot(rootdir,
                   rootdir.joinpath("boot"),
                   rootdir.joinpath("usr/lib/ostree-boot"))
        convert_to_ostree(rootdir)


def convert_to_ostree(rootdir):
    """Convert rootfs to ostree."""
    CRUFT = ["boot/initrd.img", "boot/vmlinuz",
             "initrd.img", "initrd.img.old",
             "vmlinuz", "vmlinuz.old"]
    assert rootdir is not None and rootdir != ""

    with complete_step(f"Converting {rootdir} to ostree."):
        dir_perm = 0o755

        # Emptying /dev
        log_step("Emptying /dev.")
        shutil.rmtree(rootdir.joinpath("dev"))
        os.mkdir(rootdir.joinpath("dev"), dir_perm)

        # Moving /var
        sanitize_usr_symlinks(rootdir)
        log_step("Moving /var to /usr/rootdirs.")
        os.mkdir(rootdir.joinpath("usr/rootdirs"), dir_perm)
        shutil.move(
            rootdir.joinpath("var"),
            rootdir.joinpath("usr/rootdirs/var"))
        os.mkdir(rootdir.joinpath("var"), dir_perm)

        # Remove unecessary files
        log_step("Removing unecesasry files.")
        for c in CRUFT:
            try:
                os.remove(rootdir.joinpath(c))
            except OSError:
                pass

        # Setup and split out etc
        log_step("Moving /etc to /usr/etc.")
        shutil.move(rootdir.joinpath("etc"),
                    rootdir.joinpath("usr"))

        log_step("Setting up /ostree and /sysroot.")
        try:
            rootdir.joinpath("ostree").mkdir(
                parents=True, exist_ok=True)
            rootdir.joinpath("sysroot").mkdir(
                parents=True, exist_ok=True)
        except OSError:
            pass

        log_step("Setting up symlinks.")
        TOPLEVEL_LINKS = {
            "media": "run/media",
            "mnt": "var/mnt",
            "opt": "var/opt",
            "ostree": "sysroot/ostree",
            "root": "var/roothome",
            "srv": "var/srv",
            "usr/local": "../var/usrlocal",
        }
        fd = os.open(rootdir, os.O_DIRECTORY)
        for l, t in TOPLEVEL_LINKS.items():
            shutil.rmtree(rootdir.joinpath(l))
            os.symlink(t, l, dir_fd=fd)


def sanitize_usr_symlinks(rootdir):
    """Replace symlinks from /usr pointing to /var"""
    usrdir = os.path.join(rootdir, "usr")
    for base, dirs, files in os.walk(usrdir):
        for name in files:
            p = os.path.join(base, name)

            if not os.path.islink(p):
                continue

            # Resolve symlink relative to root
            link = os.readlink(p)
            if os.path.isabs(link):
                target = os.path.join(rootdir, link[1:])
            else:
                target = os.path.join(base, link)

            rel = os.path.relpath(target, rootdir)
            # Keep symlinks if they're pointing to a location under /usr
            if os.path.commonpath([target, usrdir]) == usrdir:
                continue

            toplevel = get_toplevel(rel)
            # Sanitize links going into /var, potentially other location can
            # be added later
            if toplevel != 'var':
                continue

            os.remove(p)
            os.link(target, p)


def get_toplevel(path):
    head, tail = os.path.split(path)
    while head != '/' and head != '':
        head, tail = os.path.split(head)

    return tail


def setup_boot(rootdir, bootdir, targetdir):
    """Setup up the ostree bootdir"""
    vmlinuz = None
    initrd = None
    dtbs = None
    version = None

    try:
        os.mkdir(targetdir)
    except OSError:
        pass

    for item in os.listdir(bootdir):
        if item.startswith("vmlinuz"):
            assert vmlinuz is None
            vmlinuz = item
            _, version = item.split("-", 1)
        elif item.startswith("initrd.img") or item.startswith("initramfs"):
            assert initrd is None
            initrd = item
        elif item.startswith("dtbs"):
            assert dtbs is None
            dtbs = os.path.join(bootdir, item)
        else:
            # Move all other artifacts as is
            shutil.move(os.path.join(bootdir, item), targetdir)
    assert vmlinuz is not None

    m = hashlib.sha256()
    m.update(open(os.path.join(bootdir, vmlinuz), mode="rb").read())
    if initrd is not None:
        m.update(open(os.path.join(bootdir, initrd), "rb").read())

    csum = m.hexdigest()

    os.rename(os.path.join(bootdir, vmlinuz),
              os.path.join(targetdir, vmlinuz + "-" + csum))

    if initrd is not None:
        os.rename(os.path.join(bootdir, initrd),
                  os.path.join(targetdir,
                               initrd.replace(
                                   "initrd.img", "initramfs") + "-" + csum))
