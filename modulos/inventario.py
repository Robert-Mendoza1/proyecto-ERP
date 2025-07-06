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
        print("5. modificar precio")
        print("6. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-5): ")
        
        match opcion:
            case "1": registrar_producto()
            case "2": actualizar_stock()
            case "3": listar_productos()
            case "4": buscar_producto()
            case "5": actualizar_precio()
            case "6": break
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

    # Variables de control para los bucles
    producto_encontrado = False
    stock_valido = False
    
    while not producto_encontrado:
        try:
            # Solicitar ID del producto
            id_input = input("\nIngrese el ID del producto a actualizar: ")
            id_producto = int(id_input)
            
            # Buscar el producto
            producto = next((p for p in productos if p["id"] == id_producto), None)
            
            if producto:
                producto_encontrado = True
                # Mostrar stock actual
                print(f"\nProducto: {producto['nombre']}")
                print(f"Stock actual: {producto['stock']}")
                
                while not stock_valido:
                    try:
                        nuevo_stock = int(input("Ingrese el nuevo valor de stock: "))
                        if nuevo_stock < 0:
                            print("¡Error! El stock no puede ser negativo.")
                        else:
                            producto["stock"] = nuevo_stock
                            print(f"\n✓ Stock actualizado para '{producto['nombre']}' a {nuevo_stock}.")
                            stock_valido = True
                    except ValueError:
                        print("¡Error! Debe ingresar un número entero válido.")
            else:
                print("\n✗ Producto no encontrado. Intente nuevamente.")
                # Mostrar lista de productos
                print("\nProductos disponibles:")
                for p in productos:
                    print(f"ID: {p['id']} - {p['nombre']}")
        except ValueError:
            print("¡Error! El ID debe ser un número entero. Intente nuevamente.")
        
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
        
def actualizar_precio ():
    print("\n"+"-"*50)
    print(" MODIFICAR PRECIO".center(50))
    print("-"*50)
    
    producto_encontrado = False
    
    while not producto_encontrado:
        try:
            id_input = input("\n ingrese el ID del productto a modificar (o '0' para salir)")
            
            if id_input == '0':
                print ("\n Operacion cancelada")
                return
            
            id_producto = int(id_input)
            
            producto = next((p for p in productos if p ["id"] == id_producto ), None)
            if producto:
                producto_encontrado = True
                # Mostrar información actual
                print(f"\nProducto: {producto['nombre']}")
                print(f"Precio actual: ${producto['precio']:.2f}")
                
                # Bucle para validar nuevo precio
                precio_valido = False
                while not precio_valido:
                    try:
                        nuevo_precio = float(input("Ingrese el nuevo precio: $"))
                        if nuevo_precio <= 0:
                            print("¡Error! El precio debe ser mayor que cero.")
                        else:
                            # Confirmar cambio
                            confirmacion = input(f"¿Confirmar cambio de precio de ${producto['precio']:.2f} a ${nuevo_precio:.2f}? (S/N): ").upper()
                            if confirmacion == 'S':
                                producto["precio"] = nuevo_precio
                                print(f"\n✓ Precio actualizado para '{producto['nombre']}' a ${nuevo_precio:.2f}.")
                                precio_valido = True
                            else:
                                print("\nCambio cancelado.")
                                precio_valido = True
                    except ValueError:
                        print("¡Error! Debe ingresar un valor numérico válido.")
            else:
                print("\n✗ Producto no encontrado. Intente nuevamente.")
                # Mostrar lista de productos disponibles
                print("\nProductos disponibles:")
                for p in sorted(productos, key=lambda x: x['id']):
                    print(f"ID: {p['id']} - {p['nombre']} (Precio actual: ${p['precio']:.2f})")
        except ValueError:
            print("¡Error! El ID debe ser un número entero. Intente nuevamente.")