import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from huggingface_hub import HfFolder
import shutil
from IPython.display import FileLink

# Set your Hugging Face token
HfFolder.save_token("huggingfacetokenhere")

# Load the model
pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

# Generate the video frames
prompt = "Spiderman is surfing"
video_frames = pipe(prompt, num_inference_steps=25).frames

# Reshape or select the appropriate portion of the video_frames array
video_frames_reshaped = [frame for frame in video_frames[0]]

# Export the video frames to a video
video_path = export_to_video(video_frames_reshaped)

# Define the location to save the video (you can specify your desired path)
output_video_path = "generated_video.mp4"

# Move or rename the generated video file to the desired location
shutil.move(video_path, output_video_path)

# Create a download link (this will work in Jupyter Notebooks or environments that support FileLink)
print(f"Video saved to: {output_video_path}")
FileLink(output_video_path)  # This will create a clickable link to download the video
