#!/bin/bash

# script to install this on a bare Debian-based GCP/AWS/whatever instance/container, running as root

apt update
apt install -y python3 python3-pip python3-venv vim tmux git
# add ssh keys here
chmod 600 ~/.ssh/id_ed25519
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
git clone git@github.com:orange-life/ursula-api.git
cd ursula-api/
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
./scripts/start.sh
