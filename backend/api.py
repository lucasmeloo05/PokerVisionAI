from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import tempfile
import os

from poker_analyzer import analyze_hand

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)

model = YOLO(
    os.path.join(BASE_DIR, "best.pt")
)


@app.get("/")
def root():
    return {
        "message": "PokerVisionAI API Online"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # cria arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    )

    content = await file.read()

    temp_file.write(content)
    temp_file.close()

    # inferência YOLO
    results = model(temp_file.name)

    # remove arquivo temporário
    os.unlink(temp_file.name)

    detections = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if conf >= 0.50:
                detections.append({
                    "card": model.names[cls],
                    "confidence": round(conf, 2)
                })

    # ordena pela confiança
    detections = sorted(
        detections,
        key=lambda x: x["confidence"],
        reverse=True
    )

    # remove cartas repetidas
    unique_cards = []

    for item in detections:

        card_name = item["card"]

        if card_name not in unique_cards:
            unique_cards.append(card_name)

    # análise da mão
    analysis = analyze_hand(unique_cards)

    return {
        "cards": unique_cards,
        "hand": analysis["hand"],
        "strength": analysis["strength"],
        "recommendation": analysis["recommendation"]
    }
