"""
Сервер демонстрационных страниц
"""
import gradio as gr
from fastapi import FastAPI

from reccomender.interface import gr_rec_interface
from classifier.interface import gr_classifier_interface
from forecaster.interface import gr_forecaster_interface


app = FastAPI()
gr.mount_gradio_app(app, gr_rec_interface(), path="/gradio/rec")
gr.mount_gradio_app(app, gr_classifier_interface(), path="/gradio/classifier")
gr.mount_gradio_app(app, gr_forecaster_interface(), path="/gradio/forecaster")
