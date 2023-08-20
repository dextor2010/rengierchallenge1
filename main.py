from fastapi import FastAPI,HTTPException
import os
import httpx
from pydantic import BaseModel
app = FastAPI()


@app.get("/")
async def get_return_value():
    return {"welcome_message":'Welcome to Rengier, Use the following end point to test the services'}


@app.get("/server")
async def server_info():
    url = "https://rimu-tf-base-playground.s3.eu-west-1.amazonaws.com/tech_assess.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()

    # Calculate average load of the server
    load_avg = os.getloadavg()

    # Get available disk space on the current file system
    disk_info = os.statvfs('/')
    block_size = disk_info.f_frsize
    total_space = block_size * disk_info.f_blocks
    available_space = block_size * disk_info.f_bavail

    response_data = {
        "server_load": load_avg,
        'total_space':total_space, #Totla Disk Space
        "available_disk_space": available_space, #avaliable space
        "data_from_url":data
    }

    return response_data


@app.get("/return_value")
async def get_return_value():
    url = "https://rimu-tf-base-playground.s3.eu-west-1.amazonaws.com/tech_assess.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    data = response.json()
    return_value = data["tech"]["return_value"]
    return {"return_value":return_value}


class UpdateValue(BaseModel):
    return_value: int

json_data = {"tech": {"return_value":1337}}

@app.get("/get-return-value")
async def get_return_value():
    return json_data

@app.post("/update-return-value")
async def update_return_value(update: UpdateValue):
    new_return_value = update.return_value
    json_data["tech"]["return_value"] = new_return_value
    return {"message": "Return value updated successfully"}
