from pydantic import BaseModel

#use to insert data to database
class NoteModel(BaseModel):
    title:str
    noteInformation:str
    noteImp:bool = None