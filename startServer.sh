#!/bin/bash

git submodule init
git submodule update
pip install -r reptilerecon/yolov5/requirements.txt
python reptilerecon/manage.py makemigrations YOLOv5
python reptilerecon/manage.py migrate
mkdir reptilerecon/media
pip install django
pip install opencv-python
pip install plotly
conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
pip install daphne
cd reptilerecon && daphne -b 0.0.0.0 -p 8000 reptilerecon.asgi:application
