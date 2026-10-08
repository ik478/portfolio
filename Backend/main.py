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
    "kiran": {
        "active": kiran.get_status(),
        "name": "C K Kiran Kumar",
        "initials": "ik",
        "role": "Software Developer",
        "tagline": "I build fast, beautiful web apps with Angular and Python.",
        "about": """Though I can be a bit lazy at times, my curiosity never rests when it
                    comes to learning old/new technologies. I'm always eager to dive into the
                    latest innovations and turn them into practical projects.""",
        "email": "ckkiran94@gmail.com",
        "stats": [
            {"value": "1.5+", "label": "Years of experiance"},
            {"value": "10+", "label": "Projects built"},
            {"value": "100%", "label": "Curiosity"},
        ],
        "skills": [
            {"name": "Python", "level": 80},
            {"name": "ROS2", "level": 85},
            {"name": "Gazebo", "level": 80},
            {"name": "Omniverse", "level": 70},
            {"name": "Isacc-sim", "level": 80},
            {"name": "C#", "level": 85},
            {"name": "PLC", "level": 70},
            {"name": "Unity", "level": 85},
            {"name": "CNC", "level": 70},
        ],
        "projects": [
            project(1, "Autonomous Mobile Robot Simulation", "built using ROS2 and isacc-sim created the \n web based tool to create task and automate ", ["ROS2", "Isaac-sim", "frontend skills","Python"],"/api/media/AMR_gif.gif","https://www.google.com"),
            project(2, "AI Vision Based PPE Detection", "Built AI based Personal protective equipmet detection, \n for ensuring the required equpments are there on the person", ["Python", "Yolo"]),
            project(3, "Chat Application", "Real-time messaging with rooms and typing indicators.", ["WebSockets", "FastAPI", "Redis"]),
        ],
    },
    "pavan": {
        "active": pavan.get_status(),
        "name": "Pavan Ashok Bushetti",
        "initials": "PAB",
        "role": "Software Developer",
        "tagline": "I turn complicated ideas into simple, delightful interfaces.",
        "about": "I love design systems, smooth animations and accessible layouts. I care about how a product feels, not just how it looks.",
        "email": "pavanbushetti@gmail.com",
        "stats": [
            {"value": "1.5+", "label": "Years of experiance"},
            {"value": "25+", "label": "Screens shipped"},
            {"value": "12", "label": "Happy clients"},
        ],
        "skills": [
            {"name": "UI Design", "level": 95},
            {"name": "Angular", "level": 80},
            {"name": "CSS Animation", "level": 92},
            {"name": "Figma", "level": 90},
            {"name":"Opcenter", "level":85},
        ],
        "projects": [
            project(1, "Travel Booking App", "Clean booking flow with a map and animated trip cards.", ["Angular", "Figma", "CSS"],"C:\\Users\\KiranKumarCK\\Music\\Learn\\Angular-web\\Backend\\media\\image.webp"),
            project(2, "Design System Kit", "Reusable buttons, forms and layouts for a whole company.", ["Design System", "CSS"]),
            project(3, "Fitness Tracker UI", "Progress rings, streaks and a friendly onboarding.", ["UI/UX", "Angular"]),
        ],
    },
    "shreekant": {
        "active": shreekant.get_status(),
        "name": "Shreekant Hallakar",
        "initials": "SH",
        "role": "C# devloper",
        "tagline": "I build reliable APIs and pipelines that handle real data.",
        "about": "I work with Python, databases and cloud tools. I enjoy making systems that are fast, safe and easy to maintain.",
        "email": "arjun@example.com",
        "stats": [
            {"value": "5+", "label": "Years coding"},
            {"value": "40+", "label": "APIs built"},
            {"value": "99.9%", "label": "Uptime goal"},
        ],
        "skills": [
            {"name": "Python", "level": 95},
            {"name": "FastAPI / Django", "level": 90},
            {"name": "SQL & PostgreSQL", "level": 88},
            {"name": "Docker & Cloud", "level": 78},
        ],
        "projects": [
            project(1, "Payments API", "Secure payment service handling thousands of requests.", ["Python", "FastAPI", "Docker"]),
            project(2, "Data Pipeline", "Automated daily import, cleaning and reporting of data.", ["Python", "SQL", "Airflow"]),
            project(3, "Inventory System", "Stock tracking with alerts and a clean REST API.", ["Django", "PostgreSQL"]),
        ],
    },
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