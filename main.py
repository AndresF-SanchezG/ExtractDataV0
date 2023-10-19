import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from io import BytesIO

app = FastAPI()

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
            <!-- <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="excel_file">
                <input id="button" type="submit" value="upload">
            </form> -->
            <form action="/upload" method="post" enctype="multipart/form-data">
              <input type="file" name="excel_file" accept=".xls', '.xlsx">
              <input type="submit" value="Subir PDF">
          </form>
        </div>

    </div>
</body>
</html>
    """

@app.post("/upload/")
async def upload_file(excel_file: UploadFile = File(...)):
    try:
        # Validar que es un archivo Excel
        if not excel_file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(status_code=400, detail="El archivo debe ser un archivo de Excel (xls o xlsx).")
        
        # Leer el archivo directamente en un DataFrame
        excel_buffer = BytesIO(excel_file.file.read())
        excel_data = pd.read_excel(excel_buffer, engine='openpyxl')
        print(excel_data)

        # Procesar el DataFrame
        json_data = {"hoteles": []}
        current_hotel = None
        current_room = None

        for index, row in excel_data.iterrows():
            hotel_name = row["Hotel"]
            room_name = row["Tipo de Habitación"]
            desde = row["Desde"]
            hasta = row["Hasta"]
            descuento = row["Descuento"]
            sencilla = row["Sencilla"]
            doble_adicional = row["Doble Adicional"]
            niño = row["Niño"]
        
            if hotel_name != current_hotel:
                current_hotel = hotel_name
                current_room = None
                json_data["hoteles"].append({
                    "nombre": current_hotel,
                    "habitaciones": []
                })

            if room_name != current_room:
                current_room = room_name
                json_data["hoteles"][-1]["habitaciones"].append({
                    "nombre": current_room,
                    "tarifas": []
                })

            json_data["hoteles"][-1]["habitaciones"][-1]["tarifas"].append({
                "desde": desde.strftime("%d-%b-%y"),
                "hasta": hasta.strftime("%d-%b-%y"),
                "descuento": f"{descuento:.2f}%",
                "precios": {
                    "sencilla": f"{sencilla:.2f}",
                    "doble_adicional": f"{doble_adicional:.2f}",
                    "niño": f"{niño:.2f}"
                }
            })

        return json_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)