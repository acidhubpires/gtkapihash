import geopandas as gpd
import zipfile
import os
import tempfile
from fastapi import HTTPException
from .geo_processing import process_geodata

def processar_arquivo_upload(file_location):
    try:
        # Verifica o tipo de arquivo
        if file_location.endswith(".kmz"):
            # Processar KMZ
            gdf = gpd.read_file(f"zip://{file_location}")
        elif file_location.endswith(".geojson"):
            # Processar GeoJSON
            gdf = gpd.read_file(file_location)
        elif file_location.endswith(".zip"):
            # Processar shapefile compactado em ZIP
            with tempfile.TemporaryDirectory() as tmpdirname:
                with zipfile.ZipFile(file_location, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)

                # Procurar o arquivo .shp dentro do zip extraído
                shp_file = None
                for root, dirs, files in os.walk(tmpdirname):
                    for filename in files:
                        if filename.endswith(".shp"):
                            shp_file = os.path.join(root, filename)
                            break
                
                if shp_file is None:
                    raise HTTPException(status_code=400, detail="Nenhum arquivo .shp encontrado no arquivo ZIP.")
                
                gdf = gpd.read_file(shp_file)
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use KMZ, GeoJSON ou ZIP contendo shapefiles.")
        
        # Certifique-se de que gdf é um GeoDataFrame
        if not isinstance(gdf, gpd.GeoDataFrame):
            raise HTTPException(status_code=500, detail="Erro ao processar o arquivo: O arquivo fornecido não é um GeoDataFrame.")

        # Garantir que o GeoDataFrame tenha a coluna 'geometry'
        if 'geometry' not in gdf:
            raise HTTPException(status_code=400, detail="Nenhuma geometria encontrada no arquivo.")

        # Extrair coordenadas da geometria
        coordenadas = []
        for geom in gdf.geometry:
            if geom.is_empty:
                continue  # Ignorar geometrias vazias

            if geom.geom_type == "Polygon" or geom.geom_type == "MultiPolygon":
                coords = list(geom.exterior.coords)
            elif geom.geom_type in ["LineString", "Point", "MultiPoint", "MultiLineString"]:
                coords = list(geom.coords)
            else:
                raise HTTPException(status_code=400, detail=f"Tipo de geometria {geom.geom_type} não suportado.")
            coordenadas.append(coords)
        
        # Processa as coordenadas e gera as nomenclaturas
        resultados = process_geodata(coordenadas)
        
        return resultados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
