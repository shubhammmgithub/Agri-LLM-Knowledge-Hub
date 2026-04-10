# backend/services.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def get_mandi_prices(commodity: str, state: str):
    # Official Open Government Data (OGD) API endpoint
    api_key = os.getenv("GOV_API_KEY", "YOUR_GOV_API_KEY")
    url = f"https://api.data.gov.in/resource/9ef273d4-d367-4638-8e68-3069c9b1979c?api-key={api_key}&format=json&filters[commodity]={commodity}&filters[state]={state}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        # Logic to extract the "Modal Price" (average price)
        return data['records'][0]['modal_price'] if data['records'] else "No data found"