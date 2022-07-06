#!/bin/bash

git submodule init
git submodule update
pip install -r reptilerecon/yolov5/requirements.txt
python reptilerecon/manage.py makemigrations YOLOv5
python reptilerecon/manage.py migrate
mkdir reptilerecon/media
pip install django==4.0.3
pip install opencv-python
pip install plotly
pip install torch==1.10.0+cu102 torchvision==0.11.0+cu102 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
pip install daphne
cd reptilerecon && daphne -b 0.0.0.0 -p 8000 reptilerecon.asgi:application
