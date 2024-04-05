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
    if exists(archive_path) is False:
        return False

    file_name = archive_path.split('/')[-1]
    file_path = '/data/web_static/releases/'
    no_tgz = "{}{}".format(file_path, file_name.split('.')[0])
    tmp = "/tmp/{}".format(file_name)
    try:
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}/'.format(file_path))
        run('sudo tar -xzf {} -C {}/'.format(tmp, no_tgz))
        run("sudo rm -r {}".format(tmp))
        run('sudo rm -r /data/web_static/current')
        run('sudo ln -sf {}/ /data/web_static/current'.format(no_tgz))
        print('New version deployed!')
        return True
    except Exception as e:
        return False
