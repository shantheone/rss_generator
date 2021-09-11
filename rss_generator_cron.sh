#!/usr/bin/bash
source /var/services/homes/shan/scripts/rss_generator/.venv/bin/activate
cd /var/services/homes/shan/scripts/rss_generator/
python main.py
deactivate
mv *.xml /volume1/web/rss/
