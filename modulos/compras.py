from utils.helpers import borrar_pantalla, esperar_tecla, validar_entero, validar_float
from datetime import datetime

# Datos de ejemplo (en producción usar DB)
ordenes_compra = []
proveedores = [
    {"id": 1, "nombre": "Distribuidora Alimentos S.A.", "contacto": "Juan Pérez", "telefono": "987654321"},
    {"id": 2, "nombre": "Bebidas del Norte", "contacto": "María Gómez", "telefono": "912345678"}
]

def menu():
    while True:
        borrar_pantalla()
        print("\n" + "="*50)
        print(" MÓDULO DE COMPRAS ".center(50))
        print("="*50)
        print("\n1. Crear orden de compra")
        print("2. Recepción de mercancía")
        print("3. Historial de órdenes")
        print("4. Gestión de proveedores")
        print("5. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-5): ")
        
        match opcion:
            case "1": crear_orden_compra()
            case "2": recibir_mercancia()
            case "3": historial_compras()
            case "4": gestion_proveedores()
            case "5": break
            case _: print("\n¡Opción no válida!")
        
        esperar_tecla()

def crear_orden_compra():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" NUEVA ORDEN DE COMPRA ".center(50))
    print("="*50)
    
    # Selección de proveedor
    print("\nProveedores disponibles:")
    for prov in proveedores:
        print(f"{prov['id']}. {prov['nombre']} (Contacto: {prov['contacto']})")
    
    id_proveedor = validar_entero("\nID del proveedor: ")
    proveedor = next((p for p in proveedores if p["id"] == id_proveedor), None)
    
    if not proveedor:
        print("¡Proveedor no encontrado!")
        return

    # Detalles de la orden
    productos = []
    while True:
        print("\n" + "-"*50)
        print("Agregar producto (deje el nombre vacío para terminar)")
        nombre = input("Nombre del producto: ").strip()
        if not nombre: break
        
        cantidad = validar_entero("Cantidad: ")
        precio_unitario = validar_float("Precio unitario: $")
        
        productos.append({
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "recibido": False
        })
    
    if not productos:
        print("\n¡La orden debe contener al menos un producto!")
        return
    
    # Generar orden
    nueva_orden = {
        "id": len(ordenes_compra) + 1,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "proveedor": proveedor["nombre"],
        "id_proveedor": proveedor["id"],
        "productos": productos,
        "estado": "Pendiente",
        "total": sum(p["cantidad"] * p["precio_unitario"] for p in productos)
    }
    
    ordenes_compra.append(nueva_orden)
    print(f"\n✅ Orden #{nueva_orden['id']} creada con éxito (Total: ${nueva_orden['total']:.2f})")

def recibir_mercancia():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" RECEPCIÓN DE MERCANCÍA ".center(50))
    print("="*50)
    
    if not ordenes_compra:
        print("\nNo hay órdenes pendientes.")
        return
    
    # Mostrar órdenes pendientes
    print("\nÓrdenes pendientes de recepción:")
    for orden in filter(lambda o: o["estado"] == "Pendiente", ordenes_compra):
        print(f"\nID: {orden['id']} | Proveedor: {orden['proveedor']}")
        print(f"Fecha: {orden['fecha']} | Total: ${orden['total']:.2f}")
        for prod in orden["productos"]:
            status = "✓" if prod["recibido"] else "✗"
            print(f"  - {status} {prod['nombre']} ({prod['cantidad']} unidades)")

    # Seleccionar orden
    id_orden = validar_entero("\nID de orden a recibir (0 para cancelar): ")
    if id_orden == 0: return
    
    orden = next((o for o in ordenes_compra if o["id"] == id_orden), None)
    if not orden:
        print("¡Orden no encontrada!")
        return
    
    # Marcar productos como recibidos
    print("\nProductos a recibir:")
    for i, prod in enumerate(orden["productos"], 1):
        if not prod["recibido"]:
            recibido = input(f"{i}. {prod['nombre']} ({prod['cantidad']} unidades) ¿Recibido? (s/n): ").lower()
            if recibido == "s":
                prod["recibido"] = True
    
    # Actualizar estado
    if all(p["recibido"] for p in orden["productos"]):
        orden["estado"] = "Completada"
        print("\n✅ Todos los productos recibidos. Orden completada.")
    else:
        orden["estado"] = "Parcial"
        print("\n⚠ Recepción parcial registrada.")

def historial_compras():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" HISTORIAL DE COMPRAS ".center(50))
    print("="*50)
    
    if not ordenes_compra:
        print("\nNo hay órdenes registradas.")
        return
    
    # Filtros
    print("\nFiltros disponibles:")
    print("1. Todas las órdenes")
    print("2. Solo pendientes")
    print("3. Solo completadas")
    filtro = input("\nSeleccione filtro (1-3): ")
    
    ordenes_filtradas = []
    match filtro:
        case "1": ordenes_filtradas = ordenes_compra
        case "2": ordenes_filtradas = [o for o in ordenes_compra if o["estado"] != "Completada"]
        case "3": ordenes_filtradas = [o for o in ordenes_compra if o["estado"] == "Completada"]
        case _:
            print("Opción no válida. Mostrando todas.")
            ordenes_filtradas = ordenes_compra
    
    # Mostrar resultados
    for orden in sorted(ordenes_filtradas, key=lambda x: x["fecha"], reverse=True):
        print("\n" + "-"*50)
        print(f"Orden #{orden['id']} | {orden['fecha']}")
        print(f"Proveedor: {orden['proveedor']} | Estado: {orden['estado']}")
        print(f"Total: ${orden['total']:.2f}")
        
        print("\nProductos:")
        for prod in orden["productos"]:
            status = "✓" if prod["recibido"] else "✗"
            print(f"  - {status} {prod['nombre']}: {prod['cantidad']} x ${prod['precio_unitario']:.2f}")

def gestion_proveedores():
    pass