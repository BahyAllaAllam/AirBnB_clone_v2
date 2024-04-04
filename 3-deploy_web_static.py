#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py)
   that creates and distributes an archive to your web servers
   using the function deploy."""

import os
from fabric.api import *
from datetime import datetime


def do_pack():
    """
    Packs web static to versions
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        c.local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Deploys web static 1
    """
    try:
        if os.path.exists(archive_path):
            file_name = archive_path.split('/')[-1]
            file_path = '/data/web_static/releases/'
            releases_path = file_path + file_name[:-4]
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
        else:
            return False
    except Exception as e:
        return False


def deploy():
    """
    Deploys web static 2
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
