from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import Response
from pydantic import BaseModel
import requests
import random
import json

app = FastAPI()

class Item(BaseModel):
	name: str
	price : float
	is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/val")
async def read_val(nb: Union[int, None] = None):
	if nb :
		random_list = random.sample(range(-1000, 1000), nb)
		random_dict = { "nb" : nb, "valeurs" : random_list }
		random_json = json.dumps(random_dict)
		return(random_json)
	if not nb :
		return(random.randint(0, 100))

@app.get("/calc/add")
async def read_add(n1:int , n2:int):
	return(n1+n2)

@app.get("/calc/prod", response_class=HTMLResponse)
async def read_prod(n1:int , n2:int):
	resultat = n1*n2
	page = f"<html><head></head><body><h1> {n1} x {n2} = {resultat}</h1></body></html>"
	return(page)

@app.get("/img", response_class=Response)
async def read_img(num:int):
	url = f"https://www.juleshaag.fr/devIA/devAPI/{num}.png"
	img = requests.get(url, stream=True).content
	return Response(content=img, media_type="image")

@app.get("/stations_velo", response_class=Response)
async def read_velo(id : int) :
	url = "https://www.juleshaag.fr/devIA/devAPI/station_information.json"
	velo = requests.get(url)
	velo = eval(velo.text)
	velo = json.dumps(velo["data"]["stations"][id])
	return Response(velo)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
	return{"item_name": item.name, "item_id": item_id}

