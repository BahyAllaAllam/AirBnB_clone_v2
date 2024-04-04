#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
   that distributes an archive to your web servers,
   using the function do_deploy."""

from pathlib import Path
from fabric.api import *
from os.path import exists
from datetime import datetime

env.hosts = ['3.84.168.105', '100.26.18.236']


def do_deploy(archive_path):
    """Distributes an archive to a web servers."""
    if not Path(archive_path).is_file():
        return False

    try:
        put(archive_path, "/tmp/")
        archive_filename = Path(archive_path).stem
        release_folder = "/data/web_static/releases/{}".format(
                         archive_filename)
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{}.tgz -C {}".format(
            archive_filename, release_folder))
        run('rm -r /tmp/{}.tgz'.format(archive_filename))
        current_link = "/data/web_static/current"
        run("rm -rf {}".format(current_link))
        run("ln -s {} {}".format(release_folder, current_link))
        print("New version deployed!")
        return True
    except Exception:
        return False
