from app.repositories.productos_repo import obtener_productos

def buscar_producto(nombre):
    """Devuelve el primer producto cuyo nombre contenga el texto buscado."""
    buscado = nombre.lower()
    for p in obtener_productos():
        if buscado in p["nombre"].lower():
            return p
    return None

def obtener_productos_disponibles():
    """Productos que se ofrecen en el desplegable."""
    return obtener_productos()