from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from models.model_note import NoteModel
from config.db import conn
from schemas.schema_note import note_entity,note_entity_list
from fastapi.templating import Jinja2Templates

note_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@note_router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.getnotes.allnotes.find({})
    newDocs=[]
    for doc in docs:
        print(doc)
        newDocs.append({
            "id":doc["_id"],
            "title": doc["title"],
            "noteInformation" : doc["noteInformation"],
            "noteImp" : doc["noteImp"]
        })
    return templates.TemplateResponse(request=request, name="index.html",context={"newDocs":newDocs})


@note_router.get("/items/{item_id}")
def read_item(item_id: int, q: str| None = None):
    return {"item_id": item_id, "q": q}

@note_router.post("/")
async def addNote(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["noteImp"] = True if formDict.get("noteImp") == "on" else False
    addedNote = conn.getnotes.allnotes.insert_one(formDict)
    #return {"Success":True, note_entity(formDict)}
    return templates.TemplateResponse(request=request, name="index.html",context={"addedNote":addedNote})