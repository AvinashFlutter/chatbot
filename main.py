# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import numpy as np

app = FastAPI()

# Load trained model and label encoder
model = joblib.load("model/intent_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

# Load intents.json
with open("intents.json", "r", encoding='utf-8') as f:
    intents = json.load(f)

class Query(BaseModel):
    message: str

@app.post("/chat")
def chatbot_reply(query: Query):
    user_input = query.message.lower()

    # Predict with probabilities
    probabilities = model.predict_proba([user_input])[0]
    confidence = np.max(probabilities)
    predicted_index = np.argmax(probabilities)
    intent = label_encoder.inverse_transform([predicted_index])[0]

    # Threshold check
    if confidence < 0.3:
        return {
            "response": "Sorry, I'm not sure what you mean. Can you please rephrase?",
            "suggested_replies": []
        }

    # Return response and suggestions
    for item in intents:
        if item["intent"] == intent:
            combined_response = "\n".join(item["responses"])
            # full_response = "\n".join(item["responses"])
            return {
                # "response": item["responses"][0],
                "response":combined_response,
                "suggested_replies": item.get("suggested_replies", [])
            }

    return {
        "response": "Sorry, I didn't understand your question.",
        "suggested_replies": []
    }
