from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

import send_mail

app = FastAPI()

# Folder where you will put real GIFs later: backend/media/
MEDIA_DIR = Path(__file__).parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)
app.mount("/api/media", StaticFiles(directory=MEDIA_DIR), name="media")


def project(pid, title, description, tags, gif=None,link=None):
    # gif=None means "use the default animated preview"
    return {"id": pid, "title": title, "description": description, "tags": tags, "gif": gif,"githubUrl":link}

class members():
    def __init__(self):
        self.name: str = ""
        self.status : bool = True

    def update(self,name,status :bool):
        self.name = name
        self.status = status

    def get_status(self)-> bool:
        return self.status
    
kiran = members()
pavan = members()
shreekant = members()

all_members = {
    "kiran": kiran,
    "pavan": pavan,
    "shreekant": shreekant
}

# ---- SAMPLE DATA: replace with real details later ----
people = {
    
}

messages = []


class Message(BaseModel):
    name: str
    email: str
    message: str

class status(BaseModel):
    name : str
    key: str
    status :bool



def find_person(username: str):
    person = people.get(username.lower())
    status = all_members[username].get_status()
    if not person or not status:
        raise HTTPException(status_code=404, detail="Portfolio not active")
    return person


@app.get("/api/portfolio/{username}")
def get_portfolio(username: str):
    print(username)
    return find_person(username)


@app.post("/api/portfolio/{username}/contact")
def send_message(username: str, msg: Message):
    find_person(username)
    send_mail.send_mail(username,msg)
    messages.append({"to": username, **msg.model_dump()})
    print(f"New message for {username}: {msg}")
    return {"ok": True}

@app.post("/api/portfolio/{username}/status")
async def lockprofile(username: str, status: status):
    if not status.key == "QWERasdzxc123" : return "wrong key"

    member = all_members.get(username)

    if member is None : return "No user Found"

    member.update(username, status.status)
    print("status is executed")
    return {
        "username" :username,
        "status": member.get_status()
    }
    
if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
