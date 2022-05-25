# Web Scraping LinkedIn Project: most common technical skills requested for Jr. Data Engineer

En este proyecto se hace uso de la API **linked_api** para obtener un listado de trabajos con la búsqueda ***junior data engineer***. 
Se hizo un filtro manual que almacena palabras no técnicas, palabras que inician el enlistado de skills (por ejemplo "Requerimos") y palabras que finalizan el enlistado (por ejemplo "Beneficios"). Con dichos elementos armamos un filtro que con cada lectura de posteos mejora la obtencion de palabras técnicas.
