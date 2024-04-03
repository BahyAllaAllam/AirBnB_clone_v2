#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static.

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create directories if they don't exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared /data/web_static/current

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config="location /hbnb_static/ {
    alias /data/web_static/current/;
    index index.html;
}"
sudo sed -i "/^\s*server_name\s*localhost;/a $config" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
