#!/bin/bash

if ! command -v conda &> /dev/null
then
	mkdir -p ~/miniconda3
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
	bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
	rm -rf ~/miniconda3/miniconda.sh
	~/miniconda3/bin/conda init bash
	~/miniconda3/bin/conda init zsh
fi

conda clean -a -y
pip cache purge

eval "$(conda shell.bash hook)"
conda create --name reptilerecon -y
conda activate reptilerecon

conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch -y
conda install -c conda-forge ffmpeg x264 -y

git submodule init
git submodule update
pip install -r reptilerecon/yolov5/requirements.txt

pip install Django==5.0.4
pip install opencv-python
pip install plotly
pip install daphne

python reptilerecon/manage.py makemigrations YOLOv5
python reptilerecon/manage.py migrate
mkdir reptilerecon/media

cd reptilerecon && daphne -b 127.0.0.1 -p 8000 reptilerecon.asgi:application
