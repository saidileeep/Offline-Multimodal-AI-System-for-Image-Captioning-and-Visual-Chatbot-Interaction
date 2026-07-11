import torch
from ultralytics import YOLO
from transformers import BlipProcessor, BlipForConditionalGeneration
import open_clip

# ---------------- PATHS ----------------
YOLO_PATH = "models/yolov8x.pt"   
BLIP_PATH = "models/blip"

# ---------------- YOLO ----------------
yolo_model = YOLO(YOLO_PATH)

# ---------------- BLIP ----------------
processor = BlipProcessor.from_pretrained(
    BLIP_PATH,
    local_files_only=True
)

caption_model = BlipForConditionalGeneration.from_pretrained(
    BLIP_PATH,
    local_files_only=True
)

caption_model.eval()

# ---------------- CLIP ----------------
clip_model, _, clip_preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="openai"
)

clip_model.eval()

clip_tokenizer = open_clip.get_tokenizer("ViT-B-32")
