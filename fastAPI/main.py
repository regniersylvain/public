from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
import requests
import random
import json
from enum import Enum


app = FastAPI()


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



@app.get("/stations_velo")
async def read_velo(id:str,
		    		addr:Union[str, None]=None,
					cap:Union[str, None]=None
					) :
	url = "https://www.juleshaag.fr/devIA/devAPI/station_information.json"
	stations = requests.get(url)
	stations = eval(stations.text)["data"]["stations"]

	if id =="toutes" and cap == "":
		cap_total = 0
		for station in stations :
			cap_total += station["capacity"]
		return cap_total

	else :
		if addr == "" :
			return stations[int(id)]["address"]
		elif cap == "" :
			return stations[int(id)]["capacity"]
		else :
			return json.dumps(stations[int(id)], ensure_ascii=False).encode('utf8')
	



@app.get("/stations_velo/{id}/{info}")
async def read2_velo(id : str, info : Union[str, None] = None) :
	url = "https://www.juleshaag.fr/devIA/devAPI/station_information.json"
	stations = requests.get(url)
	stations = eval(stations.text)["data"]["stations"]

	if id == "toutes" and info == "cap":
		cap_total = 0
		for station in stations :
			cap_total += station["capacity"]
		return cap_total
	
	else :
		if info == "addr" :
			return stations[int(id)]["address"]
		elif info == "cap" :
			return stations[int(id)]["capacity"]
		else :
			return json.dumps(stations[int(id)]).encode('utf8')
	