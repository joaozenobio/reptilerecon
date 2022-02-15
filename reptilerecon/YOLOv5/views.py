from django.core.exceptions import PermissionDenied
from .models import Video
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UploadVideoForm
from django.core.files import File
from django.conf import settings
import cv2
from PIL import Image
import io
import torch
import numpy as np
import pandas as pd
import os


class UploadVideoFormView(FormView):
    form_class = UploadVideoForm
    template_name = 'index.html'
    success_url = reverse_lazy('YOLOv5_nm:index')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('video')
        if form.is_valid():
            for f in files:
                # Get video
                video = Video(video=f)
                video_path = f.temporary_file_path()

                # Get processed video and signal
                model = torch.hub.load(f"{settings.BASE_DIR}/yolov5", 'custom', path=f"{settings.BASE_DIR}/best.pt", source='local')
                model.conf = 0.25
                video_capture = cv2.VideoCapture(video_path)
                width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                video_output_path = f"{settings.MEDIA_ROOT}result.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(video_output_path, fourcc, 30.0, (width, height))
                success, image = video_capture.read()
                coef_list = []
                while success:
                    results = model(image)
                    points = dict()
                    for result in results.pandas().xyxy[0].values:
                        x_min, y_min, x_max, y_max = map(round, result[:4])
                        class_id = result[6]
                        points[class_id] = (x_min, y_min, x_max, y_max)
                        if ("head" in points) and ("body" in points):
                            break
                    if ("head" in points) and ("body" in points):
                        image = cv2.rectangle(image, (points['head'][0], points['head'][1]), (points['head'][2], points['head'][3]), (255, 0, 0), 2)
                        image = cv2.putText(image, " head", (points['head'][0], points['head'][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                        image = cv2.rectangle(image, (points['body'][0], points['body'][1]), (points['body'][2], points['body'][3]), (255, 0, 0), 2)
                        image = cv2.putText(image, " body", (points['body'][0], points['body'][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                        x_mean_head = int((points['head'][0] + points['head'][2]) / 2)
                        y_mean_head = int((points['head'][1] + points['head'][3]) / 2)
                        x_mean_body = int((points['body'][0] + points['body'][2]) / 2)
                        y_mean_body = int((points['body'][1] + points['body'][3]) / 2)
                        cv2.line(image, (x_mean_head, y_mean_head), (x_mean_body, y_mean_body), (0, 255, 0), thickness=2)
                        cv2.circle(image, (x_mean_head, y_mean_head), radius=5, color=(0, 0, 255), thickness=-1)
                        cv2.circle(image, (x_mean_body, y_mean_body), radius=5, color=(0, 0, 255), thickness=-1)
                        video_writer.write(image)
                        v = (y_mean_head - y_mean_body) / (x_mean_head - x_mean_body)
                        coef_list.append(v)
                    else:
                        coef_list.append(np.NaN)
                        video_writer.write(image)
                    success, image = video_capture.read()
                coef_list = np.round(coef_list, decimals=3)
                df = pd.Series(coef_list)
                df_tmp1 = df.rolling(3).mean()
                df_tmp2 = df.iloc[::-1].rolling(3).mean()
                df = df_tmp1.fillna(df_tmp2).fillna(df).interpolate(method='nearest').ffill().bfill()
                csv_output_path = video_output_path[0:-4] + '.csv'
                df.to_csv(csv_output_path)
                video_capture.release()
                video_writer.release()
                video_output_path_temp = video_output_path[0:-4] + 't.mp4'
                os.system(f"ffmpeg -i {video_output_path} -vcodec libx264 {video_output_path_temp} -y")
                os.rename(video_output_path_temp, video_output_path)
                with open(video_output_path, 'rb') as f1, open(csv_output_path, 'rb') as f2:
                    video.processed_video.save('result.mp4', File(f1), save=False)
                    video.signal.save('result.csv', File(f2), save=False)

                # Get thumb
                video_capture = cv2.VideoCapture(video_path)
                success, image = video_capture.read()
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(image)
                image_io = io.BytesIO()
                image_pil.save(image_io, 'JPEG')
                video.thumbnail.save('thumb.jpg', File(image_io))

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        videos = Video.objects.all()
        context = {
            'form': form,
            'videos': videos
        }
        return render(request, "YOLOv5/index.html", context)


class DetailView(generic.DetailView):
    model = Video
    template_name = 'YOLOv5/detail.html'


class DeleteView(generic.DeleteView):
    model = Video
    success_url = reverse_lazy('YOLOv5_nm:index')
