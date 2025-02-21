import os
import uuid

from fastapi import APIRouter, Request, UploadFile, status, HTTPException, File
from fastapi.responses import HTMLResponse
from models.model_note import NoteModel
from config.db import conn
from schemas.schema_note import note_entity, note_entity_list, uploadMessage
from fastapi.templating import Jinja2Templates
import magic
import aiofiles
from uuid import uuid4
note_router = APIRouter()
templates = Jinja2Templates(directory="templates")
from fastapi.responses import RedirectResponse

KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES ={
    'image/png':'png',
    'image/jpeg':'jpg',
    'application/pdf':'pdf'
}
@note_router.post("/upload")
async def post_endpoint(request: Request):
    try:
        random_name = uuid.uuid4()
        form = await request.form()
        filename = form['file'].filename
        fileSizeState = await validate_file_size(form['file'])
        #fileTypeState = await validate_file_Type(form['file'])
        print(fileSizeState)
        #print(fileTypeState)
        #if fileSizeState and fileTypeState:
        if fileSizeState:
            async with aiofiles.open(f"static/{random_name}.jpg", "wb") as out_file:
                while content := await form['file'].read(1024):  # async read chunk
                    await out_file.write(content)
            status = True
        else:
            status = False
    except Exception:
        raise HTTPException(status_code=500, detail=Exception)

    #return {"message": f"Successfully uploaded {filename} file size {file_size}"}
    #return templates.TemplateResponse("index.html", {"request": request,"message": f"Successfully uploaded {filename} file size {file_size}"})
    print(status)
    if status:
        out_file.close()
        return templates.TemplateResponse(request=request, name="index.html",context={"message":uploadMessage(f"Successfully uploaded {filename}")})
    else:
        return templates.TemplateResponse(request=request, name="index.html",
                                          context={"message": uploadMessage(f"Failed To uploaded. File Size State - {fileSizeState}")})
@note_router.get("/")
async def main(request: Request):
    files = os.listdir("./static")
    files_paths = sorted([f"{f}" for f in files])
    # return templates.TemplateResponse(request=request, name="index.html")
    return templates.TemplateResponse(
        "index.html", {"request": request, "files": files_paths}
    )



@note_router.get("/images", response_class=HTMLResponse)
async def list_files(request: Request):

    files = os.listdir("./static")
    files_paths = sorted([f"{f}" for f in files])
    return templates.TemplateResponse(
        "images.html", {"request": request, "files": files_paths}
    )

@note_router.get("/login", response_class=HTMLResponse)
async def list_files(request: Request):
    form = await request.form()
    return templates.TemplateResponse(
        "Login.html", {"request": request}
    )

async def validate_file_size(file: UploadFile):
    file_size =file.size
    print(file_size)
    if not 0 < file_size <= 1 * MB:

        return False
    else:

        return True

async def validate_file_Type(file: UploadFile):
    contents = await file.read()
    file_type =  file.content_type
    #file_type = magic.from_buffer(buffer=contents, mime=True)
    print(file_type)
    if file_type not in SUPPORTED_FILE_TYPES:

        return False
    else:

        return True



