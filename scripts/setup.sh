#!/bin/bash

# 初始化数据库
echo "Initializing database..."
poetry run python scripts/init_db.py

echo "Done!"
