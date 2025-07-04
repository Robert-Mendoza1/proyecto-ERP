from utils.helpers import borrar_pantalla, esperar_tecla, validar_entero
from datetime import datetime
import json

# Base de datos simulada
clientes = [
    {
        "id": 1,
        "nombre": "Laura Martínez",
        "tipo": "Premium",
        "contacto": "lauram@email.com",
        "telefono": "987654321",
        "compras_totales": 15,
        "gasto_total": 2450.50,
        "ultima_compra": "2023-11-20"
    },
    {
        "id": 2,
        "nombre": "Carlos Rodríguez",
        "tipo": "Regular",
        "contacto": "carlosr@email.com",
        "telefono": "912345678",
        "compras_totales": 5,
        "gasto_total": 780.00,
        "ultima_compra": "2023-12-05"
    }
]

def menu():
    while True:
        borrar_pantalla()
        print("\n" + "="*50)
        print(" MÓDULO DE CLIENTES ".center(50))
        print("="*50)
        print("\n1. Registrar nuevo cliente")
        print("2. Buscar cliente")
        print("3. Historial de compras")
        print("4. Programa de fidelización")
        print("5. Listado completo")
        print("6. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-6): ")
        
        match opcion:
            case "1": registrar_cliente()
            case "2": buscar_cliente()
            case "3": historial_compras()
            case "4": programa_fidelizacion()
            case "5": listar_clientes()
            case "6": break
            case _: print("\n¡Opción no válida!")
        
        esperar_tecla()

# -------------------------------
# Funciones principales del módulo
# -------------------------------

def registrar_cliente():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" REGISTRO DE CLIENTE ".center(50))
    print("="*50)
    
    nuevo_cliente = {
        "id": max(c["id"] for c in clientes) + 1 if clientes else 1,
        "nombre": input("\nNombre completo: ").title(),
        "tipo": seleccionar_tipo_cliente(),
        "contacto": input("Email: ").lower(),
        "telefono": input("Teléfono: "),
        "compras_totales": 0,
        "gasto_total": 0.0,
        "ultima_compra": None,
        "puntos": 0
    }
    
    clientes.append(nuevo_cliente)
    print(f"\n✅ Cliente {nuevo_cliente['nombre']} registrado con ID: {nuevo_cliente['id']}")

def seleccionar_tipo_cliente():
    tipos = {"1": "Regular", "2": "Premium", "3": "Empresarial"}
    print("\nTipos de cliente:")
    for key, value in tipos.items():
        print(f"{key}. {value}")
    return tipos.get(input("Seleccione tipo (1-3): "), "Regular")

def buscar_cliente():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" BUSCAR CLIENTE ".center(50))
    print("="*50)
    
    criterio = input("\nBuscar por (1-ID, 2-Nombre, 3-Teléfono, 4-Email): ")
    termino = input("Término de búsqueda: ").lower()
    
    resultados = []
    for cliente in clientes:
        match criterio:
            case "1" if str(cliente["id"]) == termino:
                resultados.append(cliente)
            case "2" if termino in cliente["nombre"].lower():
                resultados.append(cliente)
            case "3" if termino in cliente["telefono"]:
                resultados.append(cliente)
            case "4" if termino in cliente["contacto"].lower():
                resultados.append(cliente)
    
    if resultados:
        print("\nResultados encontrados:")
        for cliente in resultados:
            mostrar_detalle_cliente(cliente)
    else:
        print("\n❌ No se encontraron coincidencias")

def mostrar_detalle_cliente(cliente):
    print("\n" + "-"*50)
    print(f"ID: {cliente['id']} | Tipo: {cliente['tipo']}")
    print(f"Nombre: {cliente['nombre']}")
    print(f"Contacto: {cliente['contacto']} | Tel: {cliente['telefono']}")
    print(f"Compras totales: {cliente['compras_totales']}")
    print(f"Gasto acumulado: ${cliente['gasto_total']:.2f}")
    print(f"Última compra: {cliente['ultima_compra'] or 'N/A'}")
    if "puntos" in cliente:
        print(f"Puntos fidelización: {cliente['puntos']}")

def historial_compras():
    # Integración con módulo de ventas
    pass

def programa_fidelizacion():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" PROGRAMA DE FIDELIZACIÓN ".center(50))
    print("="*50)
    
    print("\n1. Acumular puntos")
    print("2. Canjear premios")
    print("3. Reporte de puntos")
    opcion = input("\nSeleccione opción (1-3): ")
    
    if opcion == "1":
        id_cliente = validar_entero("ID del cliente: ")
        cliente = next((c for c in clientes if c["id"] == id_cliente), None)
        
        if cliente:
            monto = float(input("Monto de la compra: $"))
            puntos = int(monto // 10)  # 1 punto por cada $10
            cliente["puntos"] = cliente.get("puntos", 0) + puntos
            print(f"\n➕ {puntos} puntos añadidos | Total: {cliente['puntos']}")
        else:
            print("\n❌ Cliente no encontrado")

def listar_clientes():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" LISTADO DE CLIENTES ".center(50))
    print("="*50)
    
    # Ordenar por mayor gasto
    clientes_ordenados = sorted(clientes, key=lambda x: x["gasto_total"], reverse=True)
    
    print(f"\n{'ID':<5}{'Nombre':<25}{'Tipo':<12}{'Gasto Total':<12}{'Últ. Compra':<12}")
    print("-"*60)
    for cliente in clientes_ordenados:
        print(f"{cliente['id']:<5}{cliente['nombre'][:24]:<25}{cliente['tipo']:<12}"
              f"${cliente['gasto_total']:<11.2f}{cliente['ultima_compra'] or 'N/A':<12}")

# Función para integración con módulo de ventas
def actualizar_datos_compra(id_cliente, monto):
    cliente = next((c for c in clientes if c["id"] == id_cliente), None)
    if cliente:
        cliente["compras_totales"] += 1
        cliente["gasto_total"] += monto
        cliente["ultima_compra"] = datetime.now().strftime("%Y-%m-%d")