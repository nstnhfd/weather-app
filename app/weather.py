from fastapi import FastAPI,HTTPException
from pydantic import BaseModel  
import uvicorn  
import requests
import os

app = FastAPI()  
# Define a Pydantic model for the parameters  
class Params(BaseModel):  
    param1 : str  
    # param2 : str  

@app.post('/setparams')  
async def get_weather(params: Params):  
    print("start")
    base_url= " https://api.openweathermap.org/data/2.5/weather"
    # api_key = "6634d222d05ad6b8503f176d40083136"
    api_key = os.getenv('API_KEY')
    query_params = {  
        "q": f"{params.param1}",  
        "appid": api_key,  # Add the API key here  
        "units": "metric"  # Metric units for temperature  
    }  
    response = requests.get(base_url, params=query_params)
    print(response)
    if response.status_code == 200:                 
                weather_data = response.json()
    else:
                weather_data = "no weather"
    return {"message": "Parameters received", "params": weather_data}  

if __name__ == "__main__":  
    uvicorn.run(app, host="127.0.0.1", port=8000)