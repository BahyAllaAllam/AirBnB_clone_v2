#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents
   of the web_static folder of your AirBnB Clone repo,
   using the function do_pack."""

from datetime import datetime
from fabric.api import local
from pathlib import Path


def do_pack():
    """# Create versions directory if it doesn't exist"""
    Path("versions").mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None
