#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
   that distributes an archive to your web servers,
   using the function do_deploy."""

from pathlib import Path
from fabric.api import *
from os.path import exists
env.hosts = ['3.84.168.105', '100.26.18.236']


def do_deploy(archive_path):
    """Distributes an archive to a web servers."""
    if not exists(archive_path):
        return False

    file_name = archive_path.split('/')[1]
    file_path = '/data/web_static/releases/' + "{}".format(file_name.split('.')[0])
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}/'.format(file_path))
        run('rm -r /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}/'.format(file_path, file_path))
        run('rm -rf {}/web_static'.format(file_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(file_path))
        return True
    except Exception:
        return False
