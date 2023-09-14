import torch
from diffusers import StableDiffusionPipeline

hugging_token = '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'

pipe = StableDiffusionPipeline.from_pretrained('CompVis/stable-diffusion-v1-4',
                                               revision='fp16',
                                               torch_dtype=torch.float32,
                                               use_auth_token=hugging_token
                                               ).to('cpu')

#stablediffusion 1-4 text to image

prompt = 'a photo of an astronaut riding a horse on mars'
image = pipe(prompt).images[0]
image.save(f'./image.png')