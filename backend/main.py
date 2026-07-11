from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
from collections import Counter

from models import (
    yolo_model,
    processor,
    caption_model
)

from chatbot import answer_question
from color_utils import get_dominant_color

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GLOBAL STORAGE ----------------
LATEST_DETECTION = {
    "objects": [],
    "counts": {},
    "summary_text": "",
    "caption": ""
}

# ---------------- CLEAN CAPTION ----------------
def generate_caption(image):

    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        output = caption_model.generate(
            **inputs,
            max_length=60,
            num_beams=5,
            early_stopping=True
        )

    caption = processor.decode(output[0], skip_special_tokens=True)

    return caption.capitalize()


# ---------------- ANALYZE IMAGE ----------------
@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    results = yolo_model(image, conf=0.5)
    result = results[0]
    boxes = result.boxes.cpu()

    objects = []
    counts = Counter()

    for i in range(len(boxes)):

        cls_id = int(boxes.cls[i].item())
        label = result.names[cls_id]
        confidence = float(boxes.conf[i].item())
        coords = boxes.xyxy[i].tolist()

        x1, y1, x2, y2 = map(int, coords)

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.width, x2)
        y2 = min(image.height, y2)

        crop = image.crop((x1, y1, x2, y2))

        # -------- COLOR DETECTION --------
        color = get_dominant_color(crop)

        objects.append({
            "label": label,
            "confidence": confidence,
            "box": coords,
            "color": color
        })

        counts[label] += 1

    print("CMD DETECTION:", counts)

    caption = generate_caption(image)

    summary_text = ", ".join(
        [f"{v} {k}" + ("s" if v > 1 else "") for k, v in counts.items()]
    )

    LATEST_DETECTION["objects"] = objects
    LATEST_DETECTION["counts"] = dict(counts)
    LATEST_DETECTION["summary_text"] = summary_text
    LATEST_DETECTION["caption"] = caption

    return {
        "caption": caption,
        "objects": objects,
        "counts": dict(counts)
    }


# ---------------- CHAT ----------------
@app.post("/chat/")
async def chat(request: dict):

    question = request.get("question", "")

    print("CHAT COUNTS:", LATEST_DETECTION["counts"])

    response = answer_question(
        question,
        LATEST_DETECTION["objects"],
        LATEST_DETECTION["counts"],
        LATEST_DETECTION["summary_text"]
    )

    return response
