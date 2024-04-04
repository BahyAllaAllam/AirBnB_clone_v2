#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
   that distributes an archive to your web servers,
   using the function do_deploy."""

from pathlib import Path
from fabric.api import env, put, run


def do_deploy(archive_path):
    """Distributes an archive to a web servers."""
    if not Path(archive_path).is_file():
        return False

    file_name = archive_path.split('/')[1]
    file_path = '/data/web_static/releases/'
    releases_path = file_path + file_name[:-4]
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(releases_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, releases_path))
        run('rm -rf /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}/'.format(releases_path, releases_path))
        run('rm -rf {}/web_static'.format(releases_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')
        return True
    except Exception:
        return False
