def note_entity(item) -> dict:
    return {
        "_id":str(item["_id"]),
        "title": item["title"],
        "noteInformation" : item["noteInformation"],
        "noteImp" : item["noteImp"]
    }

def note_entity_list(items)->list:
    return [note_entity(item) for item in items]

def uploadMessage(msg):
    return msg