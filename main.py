from fastapi import FastAPI, Body
from model import GenreGenAssistant, ChordGenAssistant

app = FastAPI()
genre_gen_assistant = GenreGenAssistant()
chord_gen_assistant = ChordGenAssistant()

@app.get("/health")
async def health_check():
    return {"status": "200"}
@app.post("/api/v1/genre/{username}")
async def genre_model_call(username: str, item: dict = Body(...)):
    input = (f"i want you make me just one most proper melody based on my previous music note."
             f" make me next {item.get('value')} music note that include empty note and {item.get('text')} like."
             f" my previously music note is x = {item.get('previous')}")
    note_list = genre_gen_assistant.request_to_model(input)
    return note_list

@app.post("/api/v1/chord/{username}")
async def chord_model_call(username: str, item: dict = Body(...)):
    input = (f"i want you make me just one most proper lower-pitch D2 ~ B2 (35 ~ 24) chord based on my current music note that include empty note."
             f" suggest me among first and each 4th column major, minor triad. my current music note is suggestion = {item.get('previous')}")
    note_list = chord_gen_assistant.request_to_model(input)
    return note_list