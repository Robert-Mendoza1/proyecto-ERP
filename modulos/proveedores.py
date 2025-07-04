from utils.helpers import borrar_pantalla, esperar_tecla, validar_entero, validar_float
from datetime import datetime
import csv

# Estructura de datos
proveedores = [
    {
        "id": 1,
        "razon_social": "Distribuidora Alimentos S.A.",
        "contacto": "Juan Pérez",
        "telefono": "987654321",
        "email": "ventas@dalimentos.com",
        "categoria": "Alimentos",
        "productos_suministrados": ["Arroz", "Aceite", "Conservas"],
        "condiciones_pago": "30 días",
        "rating": 4.5,
        "ultima_compra": "2023-11-15",
        "compras_totales": 12,
        "monto_total": 18450.00
    }
]

def menu():
    while True:
        borrar_pantalla()
        print("\n" + "="*50)
        print(" MÓDULO DE PROVEEDORES ".center(50))
        print("="*50)
        print("\n1. Registrar nuevo proveedor")
        print("2. Buscar/Editar proveedor")
        print("3. Evaluar desempeño")
        print("4. Historial de compras")
        print("5. Listado completo")
        print("6. Exportar a CSV")
        print("7. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-7): ")
        
        match opcion:
            case "1": registrar_proveedor()
            case "2": buscar_editar_proveedor()
            case "3": evaluar_desempeno()
            case "4": historial_compras()
            case "5": listar_proveedores()
            case "6": exportar_csv()
            case "7": break
            case _: print("\n¡Opción no válida!")
        
        esperar_tecla()

# -------------------------------
# Funciones principales del módulo
# -------------------------------

def registrar_proveedor():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" REGISTRO DE PROVEEDOR ".center(50))
    print("="*50)
    
    nuevo_proveedor = {
        "id": max(p["id"] for p in proveedores) + 1 if proveedores else 1,
        "razon_social": input("\nRazón social: ").title(),
        "contacto": input("Persona de contacto: ").title(),
        "telefono": input("Teléfono: "),
        "email": input("Email: ").lower(),
        "categoria": input("Categoría (Alimentos/Limpieza/Electrónica): ").title(),
        "productos_suministrados": input("Productos suministrados (separados por coma): ").title().split(","),
        "condiciones_pago": input("Condiciones de pago (ej: 30 días, contado): "),
        "rating": 0,
        "ultima_compra": None,
        "compras_totales": 0,
        "monto_total": 0.0
    }
    
    proveedores.append(nuevo_proveedor)
    print(f"\n✅ Proveedor {nuevo_proveedor['razon_social']} registrado con ID: {nuevo_proveedor['id']}")

def buscar_editar_proveedor():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" BUSCAR/EDITAR PROVEEDOR ".center(50))
    print("="*50)
    
    termino = input("\nBuscar por (1-ID, 2-Razón Social, 3-Categoría): ")
    valor = input("Término de búsqueda: ").lower()
    
    resultados = []
    for prov in proveedores:
        match termino:
            case "1" if str(prov["id"]) == valor:
                resultados.append(prov)
            case "2" if valor in prov["razon_social"].lower():
                resultados.append(prov)
            case "3" if valor in prov["categoria"].lower():
                resultados.append(prov)
    
    if not resultados:
        print("\n❌ No se encontraron coincidencias")
        return
    
    print("\nResultados encontrados:")
    for i, prov in enumerate(resultados, 1):
        print(f"{i}. ID: {prov['id']} | {prov['razon_social']} ({prov['categoria']})")
    
    seleccion = validar_entero("\nSeleccione proveedor a editar (0 para cancelar): ")
    if seleccion == 0 or seleccion > len(resultados): return
    
    proveedor = resultados[seleccion-1]
    mostrar_detalle_proveedor(proveedor)
    
    # Edición de campos
    campo = input("\nCampo a editar (ej: 'telefono', 'email', 0 para cancelar): ")
    if campo == "0": return
    
    if campo in proveedor:
        nuevo_valor = input(f"Nuevo valor para '{campo}': ")
        proveedor[campo] = nuevo_valor if campo != "rating" else float(nuevo_valor)
        print("\n✅ Cambio guardado")
    else:
        print("\n❌ Campo no válido")

def mostrar_detalle_proveedor(proveedor):
    print("\n" + "-"*50)
    print(f"ID: {proveedor['id']} | Rating: {'★' * int(proveedor['rating'])} ({proveedor['rating']}/5)")
    print(f"Razón Social: {proveedor['razon_social']}")
    print(f"Contacto: {proveedor['contacto']} | Tel: {proveedor['telefono']}")
    print(f"Email: {proveedor['email']} | Categoría: {proveedor['categoria']}")
    print(f"Productos: {', '.join(proveedor['productos_suministrados'])}")
    print(f"Condiciones Pago: {proveedor['condiciones_pago']}")
    print(f"Historial: {proveedor['compras_totales']} compras | ${proveedor['monto_total']:.2f}")

def evaluar_desempeno():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" EVALUACIÓN DE DESEMPEÑO ".center(50))
    print("="*50)
    
    id_prov = validar_entero("\nID del proveedor a evaluar: ")
    proveedor = next((p for p in proveedores if p["id"] == id_prov), None)
    
    if not proveedor:
        print("\n❌ Proveedor no encontrado")
        return
    
    print("\nCriterios de evaluación (1-5):")
    puntajes = {
        "calidad": validar_entero("Calidad de productos: "),
        "tiempo_entrega": validar_entero("Cumplimiento en tiempos: "),
        "precio": validar_entero("Competitividad en precios: "),
        "atencion": validar_entero("Atención al cliente: ")
    }
    
    nuevo_rating = sum(puntajes.values()) / len(puntajes)
    proveedor["rating"] = round(nuevo_rating, 1)
    
    print(f"\n★ Nuevo rating: {proveedor['rating']}/5")
    print("Detalle:")
    for criterio, puntaje in puntajes.items():
        print(f"- {criterio.replace('_', ' ').title()}: {puntaje}/5")

def historial_compras():
    # Integración con módulo de compras
    pass

def listar_proveedores():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" LISTADO DE PROVEEDORES ".center(50))
    print("="*50)
    
    # Ordenar por rating descendente
    proveedores_ordenados = sorted(proveedores, key=lambda x: x["rating"], reverse=True)
    
    print(f"\n{'ID':<5}{'Razón Social':<25}{'Categoría':<15}{'Rating':<10}{'Compras':<10}")
    print("-"*65)
    for prov in proveedores_ordenados:
        print(f"{prov['id']:<5}{prov['razon_social'][:24]:<25}{prov['categoria'][:14]:<15}"
              f"{prov['rating']:<10}{prov['compras_totales']:<10}")

def exportar_csv():
    with open('proveedores.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=proveedores[0].keys())
        writer.writeheader()
        writer.writerows(proveedores)
    print("\n✅ Datos exportados a 'proveedores.csv'")

# Función para integración con módulo de compras
def actualizar_historial(id_proveedor, monto):
    proveedor = next((p for p in proveedores if p["id"] == id_proveedor), None)
    if proveedor:
        proveedor["compras_totales"] += 1
        proveedor["monto_total"] += monto
        proveedor["ultima_compra"] = datetime.now().strftime("%Y-%m-%d")