from turtle import pd
from matplotlib import pyplot as plt
from utils.helpers import borrar_pantalla, esperar_tecla, validar_entero, validar_float
from datetime import datetime, timedelta
from modulos.clientes import actualizar_datos_compra
from modulos.inventario import actualizar_stock
from modulos.reportes import actualizar_datos_ventas

# Estructuras de datos
ventas = []
catalogo = [
    {"codigo": "AR001", "nombre": "Arroz 1kg", "precio": 2.50, "stock": 150},
    {"codigo": "LE001", "nombre": "Leche 1L", "precio": 3.20, "stock": 80}
]

def menu():
    while True:
        borrar_pantalla()
        print("\n" + "="*50)
        print(" MÓDULO DE VENTAS ".center(50))
        print("="*50)
        print("\n1. Nueva venta")
        print("2. Devoluciones")
        print("3. Historial de ventas")
        print("4. Buscar transacción")
        print("5. Análisis comercial")
        print("6. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-6): ")
        
        match opcion:
            case "1": nueva_venta()
            case "2": procesar_devolucion()
            case "3": historial_ventas()
            case "4": buscar_transaccion()
            case "5": analisis_comercial()
            case "6": break
            case _: print("\n¡Opción no válida!")
        
        esperar_tecla()


def nueva_venta():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" PUNTO DE VENTA (POS) ".center(50))
    print("="*50)
    
    # Configuración inicial
    vendedor = input("\nNombre del vendedor: ").title()
    sucursal = input("Sucursal: ").title()
    id_cliente = input("ID Cliente (opcional): ")
    
    # Proceso de venta
    items = []
    total = 0.0
    
    while True:
        borrar_pantalla()
        print("\n" + "-"*50)
        print(f"{'Código':<10}{'Producto':<20}{'Precio':<10}{'Stock':<10}")
        print("-"*50)
        for prod in catalogo:
            print(f"{prod['codigo']:<10}{prod['nombre']:<20}${prod['precio']:<9.2f}{prod['stock']:<10}")
        
        print("\n" + "-"*50)
        print(f"{'TOTAL PARCIAL':<30}${total:.2f}")
        print("-"*50)
        
        codigo = input("\nCódigo del producto (ENTER para finalizar): ").upper()
        if not codigo: break
        
        producto = next((p for p in catalogo if p["codigo"] == codigo), None)
        if not producto:
            print("\n❌ Producto no encontrado")
            esperar_tecla()
            continue
        
        if producto["stock"] <= 0:
            print("\n⚠ Producto sin stock disponible")
            esperar_tecla()
            continue
        
        try:
            cantidad = int(input(f"Cantidad de {producto['nombre']} (max {producto['stock']}): "))
            if cantidad <= 0 or cantidad > producto["stock"]:
                raise ValueError
        except ValueError:
            print("\n❌ Cantidad no válida")
            esperar_tecla()
            continue
        
        # Agregar a la venta
        subtotal = producto["precio"] * cantidad
        items.append({
            "codigo": producto["codigo"],
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": cantidad,
            "subtotal": subtotal
        })
        total += subtotal
        
        # Reservar stock (no descontar aún)
        producto["stock"] -= cantidad
    
    if not items:
        print("\n⚠ Venta cancelada (sin productos)")
        return
    
    # Proceso de pago
    borrar_pantalla()
    print("\n" + "="*50)
    print(" RESUMEN DE VENTA ".center(50))
    print("="*50)
    
    print(f"\n{'Cant.':<5}{'Producto':<20}{'P.Unit.':<10}{'Subtotal':<10}")
    print("-"*45)
    for item in items:
        print(f"{item['cantidad']:<5}{item['nombre']:<20}${item['precio']:<9.2f}${item['subtotal']:.2f}")
    
    print("\n" + "-"*45)
    print(f"{'TOTAL A PAGAR:':<30}${total:.2f}")
    
    # Métodos de pago
    metodos_pago = []
    while total > 0:
        print("\nMétodos disponibles:")
        print("1. Efectivo")
        print("2. Tarjeta Débito")
        print("3. Tarjeta Crédito")
        print("4. Transferencia")
        
        opcion = input("\nSeleccione método (1-4): ")
        monto = validar_float("Monto a aplicar: $")
        
        if monto > total:
            print(f"\n⚠ Cambio: ${monto - total:.2f}")
            monto = total
        
        metodos_pago.append({
            "tipo": ["Efectivo", "Débito", "Crédito", "Transferencia"][int(opcion)-1],
            "monto": monto
        })
        total -= monto
        
        if total <= 0:
            break
        
        print(f"\nRestante: ${total:.2f}")
    
    # Confirmar venta
    confirmacion = input("\n¿Confirmar venta? (S/N): ").upper()
    if confirmacion != "S":
        # Revertir reservas de stock
        for item in items:
            prod = next(p for p in catalogo if p["codigo"] == item["codigo"])
            prod["stock"] += item["cantidad"]
        print("\n❌ Venta cancelada")
        return
    
    # Registrar venta
    nueva_venta = {
        "id": len(ventas) + 1,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vendedor": vendedor,
        "sucursal": sucursal,
        "id_cliente": int(id_cliente) if id_cliente else None,
        "items": items,
        "metodos_pago": metodos_pago,
        "total": sum(item["subtotal"] for item in items),
        "estado": "Completada"
    }
    
    ventas.append(nueva_venta)
    
    # Actualizar sistemas
    if id_cliente:
        actualizar_datos_compra(int(id_cliente), nueva_venta["total"])
    
    for item in items:
        actualizar_stock(item["codigo"], -item["cantidad"])
    
    actualizar_datos_ventas({
        "total": nueva_venta["total"],
        "sucursal": sucursal,
        "vendedor": vendedor
    })
    
    # Generar ticket
    print("\n" + "="*50)
    print(" TICKET DE VENTA ".center(50))
    print("="*50)
    print(f"\nFecha: {nueva_venta['fecha']}")
    print(f"Vendedor: {vendedor}")
    print(f"N° Operación: {nueva_venta['id']}")
    print("\n" + "-"*50)
    for item in items:
        print(f"{item['cantidad']} x {item['nombre']} ${item['precio']:.2f} = ${item['subtotal']:.2f}")
    print("\n" + "-"*50)
    print(f"TOTAL: ${nueva_venta['total']:.2f}")
    print("\n" + "-"*50)
    print("Métodos de pago:")
    for pago in metodos_pago:
        print(f"- {pago['tipo']}: ${pago['monto']:.2f}")
    
    print("\n✅ Venta registrada exitosamente")

def procesar_devolucion():
    
    borrar_pantalla()
    print("\n" + "="*50)
    print(" PROCESO DE DEVOLUCIÓN ".center(50))
    print("="*50)
    if not ventas:
        print("\nNo hay ventas registradas para procesar devoluciones")
        return
    print("\nHistorial de ventas:")
    print(f"{'ID':<5}{'Fecha':<20}{'Cliente':<20}{'Total':<10}")
    print("-"*55)
    for venta in ventas:
        cliente = f"Cliente #{venta['id_cliente']}" if venta['id_cliente'] else "Consumidor final"
        print(f"{venta['id']:<5}{venta['fecha'][:16]:<20}{cliente[:18]:<20}${venta['total']:.2f}")
        

def historial_ventas():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" HISTORIAL DE VENTAS ".center(50))
    print("="*50)
    
    if not ventas:
        print("\nNo hay ventas registradas")
        return
    
    # Filtros
    dias = validar_entero("\nMostrar últimos N días (0 para todo): ")
    fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d") if dias > 0 else None
    
    ventas_filtradas = [v for v in ventas if not fecha_limite or v["fecha"] >= fecha_limite]
    
    print(f"\n{'ID':<5}{'Fecha':<20}{'Cliente':<20}{'Total':<10}")
    print("-"*55)
    for venta in sorted(ventas_filtradas, key=lambda x: x["fecha"], reverse=True):
        cliente = f"Cliente #{venta['id_cliente']}" if venta['id_cliente'] else "Consumidor final"
        print(f"{venta['id']:<5}{venta['fecha'][:16]:<20}{cliente[:18]:<20}${venta['total']:.2f}")

def buscar_transaccion():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" BUSCAR TRANSACCIÓN ".center(50))
    print("="*50)
    
    if not ventas:
        print("\nNo hay transacciones registradas")
        return
def analisis_comercial():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" ANÁLISIS COMERCIAL ".center(50))
    print("="*50)
    
    if not ventas:
        print("\nNo hay datos para analizar")
        return
    
    df = pd.DataFrame(ventas)
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    print("\n1. Ventas por día")
    print("2. Productos más vendidos")
    print("3. Desempeño por vendedor")
    opcion = input("\nSeleccione análisis (1-3): ")
    
    if opcion == "1":
        df.groupby(df['fecha'].dt.date)['total'].sum().plot(kind='bar')
        plt.title('Ventas Diarias')
        plt.ylabel('Monto ($)')
        plt.tight_layout()
        plt.savefig('ventas_diarias.png')
        print("\nGráfico guardado: 'ventas_diarias.png'")
    
    elif opcion == "2":
        # Expandir items para análisis
        items = []
        for venta in ventas:
            for item in venta['items']:
                items.append({
                    'producto': item['nombre'],
                    'cantidad': item['cantidad'],
                    'fecha': venta['fecha']
                })
        
        df_items = pd.DataFrame(items)
        top_productos = df_items.groupby('producto')['cantidad'].sum().nlargest(5)
        
        print("\n" + "-"*50)
        print(" TOP 5 PRODUCTOS ".center(50))
        print("-"*50)
        print(top_productos.to_string())
    
    elif opcion == "3":
        desempeno = df.groupby('vendedor').agg({'total': ['sum', 'count', 'mean']})
        desempeno.columns = ['Total Vendido', 'Transacciones', 'Ticket Promedio']
        print("\n" + "-"*50)
        print(" DESEMPEÑO POR VENDEDOR ".center(50))
        print("-"*50)
        print(desempeno.sort_values('Total Vendido', ascending=False).to_string())