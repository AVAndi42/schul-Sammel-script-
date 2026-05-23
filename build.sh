#!/usr/bin/env bash
set -e

# Install libmagic system dependency
apt-get update -qq && apt-get install -y -qq libmagic1 || true

# Install Python dependencies
pip install -r requirements.txt
