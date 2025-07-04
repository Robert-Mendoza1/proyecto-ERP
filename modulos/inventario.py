from utils.helpers import borrar_pantalla, esperar_tecla

# Datos de ejemplo (en producción usaría una base de datos)
productos = [
    {"id": 1, "nombre": "Arroz 1kg", "categoria": "Abarrotes", "stock": 150, "precio": 2.50},
    {"id": 2, "nombre": "Leche 1L", "categoria": "Lácteos", "stock": 80, "precio": 3.20}
]

def menu():
    while True:
        borrar_pantalla()
        print("\n" + "="*50)
        print(" MÓDULO DE INVENTARIO ".center(50))
        print("="*50)
        print("\n1. Registrar nuevo producto")
        print("2. Actualizar stock")
        print("3. Listar productos")
        print("4. Buscar producto")
        print("5. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-5): ")
        
        match opcion:
            case "1": registrar_producto()
            case "2": actualizar_stock()
            case "3": listar_productos()
            case "4": buscar_producto()
            case "5": break
            case _: print("\n¡Opción no válida!")
        
        esperar_tecla()

def registrar_producto():
    print("\n" + "-"*50)
    print(" REGISTRAR NUEVO PRODUCTO ".center(50))
    print("-"*50)
    
    nuevo_producto = {
        "id": len(productos) + 1,
        "nombre": input("\nNombre del producto: ").title(),
        "categoria": input("Categoría: ").title(),
        "stock": int(input("Stock inicial: ")),
        "precio": float(input("Precio unitario: $"))
    }
    
    productos.append(nuevo_producto)
    print(f"\n✅ Producto '{nuevo_producto['nombre']}' registrado con éxito!")

def actualizar_stock():
    print("\n" + "-"*50)
    print(" ACTUALIZAR STOCK ".center(50))
    print("-"*50)
    
    id_producto = int(input("\nIngrese el ID del producto a actualizar: "))
    producto = next((p for p in productos if p["id"] == id_producto), None)
    
    if producto:
        nuevo_stock = int(input(f"Stock actual ({producto['stock']}): "))
        producto["stock"] = nuevo_stock
        print(f"\n✅ Stock actualizado para '{producto['nombre']}' a {nuevo_stock}.")
    else:
        print("\n❌ Producto no encontrado.")
        
        
        
        
def listar_productos():
    print("\n" + "-"*50)
    print(" LISTA DE PRODUCTOS ".center(50))
    print("-"*50)
    
    if not productos:
        print("\n❌ No hay productos registrados.")
        return
    
    for producto in productos:
        print(f"ID: {producto['id']}, Nombre: {producto['nombre']}, "
              f"Categoría: {producto['categoria']}, Stock: {producto['stock']}, "
              f"Precio: ${producto['precio']:.2f}")
        
def buscar_producto():
    print("\n" + "-"*50)
    print(" BUSCAR PRODUCTO ".center(50))
    print("-"*50)
    
    nombre_busqueda = input("\nIngrese el nombre del producto a buscar: ").title()
    resultados = [p for p in productos if nombre_busqueda in p["nombre"]]
    
    if resultados:
        for producto in resultados:
            print(f"ID: {producto['id']}, Nombre: {producto['nombre']}, "
                  f"Categoría: {producto['categoria']}, Stock: {producto['stock']}, "
                  f"Precio: ${producto['precio']:.2f}")
    else:
        print("\n❌ No se encontraron productos con ese nombre.")

# ... (implementar otras funciones del módulo)