from django import template
from django.conf import settings
import pandas as pd
import plotly.express as px


register = template.Library()


@register.simple_tag
def get_figure(video):
    coef_list = pd.read_csv(video.signal.path, index_col=0).squeeze("columns").map(abs)
    figure = px.line(coef_list)
    figure_output_path = f"{settings.BASE_DIR}/YOLOv5/templates/YOLOv5/figure.html"
    figure.write_html(figure_output_path)
    return ""
