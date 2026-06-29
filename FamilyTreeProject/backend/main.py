from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

app = FastAPI()

print("URL =", os.getenv("SUPABASE_URL"))
print("SUPABASE Connected")
#print("SUPABASE_URL =", SUPABASE_URL)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

class Family(BaseModel):
    family_name: str

class Member(BaseModel):
    family_id: str
    first_name: str
    last_name: str
    gender: str
    date_of_birth: Optional[str] = None
    photo_url: Optional[str] = None

class Relationship(BaseModel):
    family_id: str
    person1: str
    person2: str
    relation_type: str

class Family(BaseModel):
    family_name: str


@app.get("/")
def home():
    return {
        "message": "Family Tree API"
    }


@app.post("/create-family")
def create_family(family: Family):

    response = supabase.table(
        "families"
    ).insert({
        "family_name": family.family_name
    }).execute()

    return {
        "message": "Family created",
        "data": response.data
    }

@app.post("/add-member")
def add_member(member: Member):
    response = supabase.table(
        "family_members"
    ).insert(
        member.dict()
    ).execute()

    return response.data

@app.post("/add-relationship")
def add_relationship(relation: Relationship):

    response = supabase.table(
        "relationships"
    ).insert(
        relation.dict()
    ).execute()

    return response.data

@app.get("/family-tree/{family_id}")
def get_tree(family_id: str):

    members = supabase.table(
        "family_members"
    ).select("*").eq(
        "family_id",
        family_id
    ).execute()

    relations = supabase.table(
        "relationships"
    ).select("*").eq(
        "family_id",
        family_id
    ).execute()

    return {
        "members": members.data,
        "relationships": relations.data
    }