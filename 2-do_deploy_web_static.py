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

    filename = archive_path.split('/')[-1]
    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    tmp = "/tmp/" + filename
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}/'.format(no_tgz))
        run('tar -xzf {} -C {}/'.format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run('mv {}/web_static/* {}/'.format(no_tgz, no_tgz))
        run('rm -rf {}/web_static'.format(no_tgz))
        run('rm -rf /data/web_static/current')
        run('ln -sf {}/ /data/web_static/current'.format(no_tgz))
        print('New version deployed!')
        return True
    except Exception as e:
        return False
