from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from pydantic import BaseModel
import os

load_dotenv()

app=FastAPI()

client = MongoClient("mongodb://localhost:27017/")

# this is equvalent to create a database 
db=client["task_db"]    

# and this is equvalent to create a collection
tasks_collection=db["tasks"]


# pydantic model

class Task(BaseModel):
    title:str
    description:str
    completed:bool=False


# make a CREATE API (POST REQUEST)

@app.post("/tasks")
def create_task(task:Task):
    task_data=task.model_dump()
    result=tasks_collection.insert_one(task_data)

    return {
        "message":"Task is created Successfully",
        "Task-id":str(result.inserted_id)
    }

@app.get("/tasks")
def get_task():

    tasks=list(tasks_collection.find())

    for task in tasks:
        task["_id"]=str(task["_id"])

    return tasks