from flask import Flask, render_template, request, send_file
from PIL import Image
import io
from transformers import BertTokenizer
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from authtoken import auth_token

app = Flask(__name__)


modelid = "CompVis/stable-diffusion-v1-4"
device = "cuda"
stable_diffusion_model = StableDiffusionPipeline.from_pretrained(
    modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token=auth_token)
stable_diffusion_model.to(device)




@app.route('/')
def index():
    return render_template('index.html')




@app.route('/generate_image', methods=['POST'])
def generate_image():
    text = request.form['text']
    with autocast(device):
        image = stable_diffusion_model(text, guidance_scale=8.5)["sample"][0]

  
    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
