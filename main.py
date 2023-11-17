import json
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from io import BytesIO

app = FastAPI()

NOMBRE_CIUDAD_MAP = {
    "Barú": "cartagena",
    "Cartagena": "cartagena-decameron",
    "Galeón": "santa-marta",
    "Heliconias": "armenia",
    "Panaca": "armenia-panaca",
    "Ticuna": "amazonas-leticia"
}

hotelesDataJson = []

def format_value(value):
    try:
        return f"{float(value):.2f}"
    except ValueError:
        return value

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto+Mono:wght@400;500&family=Roboto+Slab:wght@500;600&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="" type="text/css">
        <title>Plenty APP</title>
    </head>
    <body>
        <div class="container">
            <h1>ATERRIZA APP - MODULO ADMINISTRATIVO</h1>
            <h3>Sección: Carga de Facturas</h3>
            <div class="view">
                <h4></h4>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="excel_file" accept=".xls', '.xlsx">
                    <input type="submit" value="Subir Excel">
                </form>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/upload/")
async def upload_file(excel_file: UploadFile = File(...)):
    try:
        if not excel_file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(status_code=400, detail="El archivo debe ser un archivo de Excel (xls o xlsx).")

        excel_buffer = BytesIO(excel_file.file.read())
        excel_data = pd.read_excel(excel_buffer, engine='openpyxl')

        result = []

        for index, row in excel_data.iterrows():
            hotel_name = row["Hotel"].strip().lower()

            room_name = row["Habitación"]
            desde = row["Desde"]
            hasta = row["Hasta*"]
            descuento = format_value(row["Descuento"])
            sencilla = format_value(row["Sencilla"])
            doble_adicional = format_value(row["Doble/Adicional"])
            niño = format_value(row["Niño"])

            ciudad = NOMBRE_CIUDAD_MAP.get(hotel_name, "san-andres")

            current_hotel = next((item for item in result if item["nombre"] == hotel_name), None)

            if current_hotel is None:
                current_hotel = {
                    "nombre": hotel_name,
                    "ciudad": ciudad,
                    "habitaciones": []
                }
                result.append(current_hotel)

            current_room = next((item for item in current_hotel["habitaciones"] if item["tipoHabitacion"] == room_name), None)

            if current_room is None:
                current_room = {
                    "tipoHabitacion": room_name,
                    "tarifas": []
                }
                current_hotel["habitaciones"].append(current_room)

            current_room["tarifas"].append({
                "desde": desde.strftime("%d-%b-%y"),
                "hasta": hasta.strftime("%d-%b-%y"),
                "descuento": f"{descuento}%",
                "precios": {
                    "sencilla": sencilla,
                    "doble_adicional": doble_adicional,
                    "niño": niño
                }
            })

        # Asigna el resultado a la variable global
        global hotelesDataJson
        hotelesDataJson = result

        # Guarda el resultado en un archivo JSON
        with open("hotelesData.json", "w") as json_file:
            json.dump(result, json_file)

        data = pd.read_json('/hotelesData.json')
        print(data) 

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    import uvicorn
  
    uvicorn.run(app, host="0.0.0.0", port=8000)

