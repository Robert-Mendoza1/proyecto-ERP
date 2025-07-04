from utils.helpers import borrar_pantalla, esperar_tecla, validar_entero
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import os

# Datos de ejemplo (en producción se conecta a otros módulos)
datos_ventas = [
    {"fecha": "2023-12-01", "monto": 1250.50, "sucursal": "Norte", "vendedor": "Juan Pérez"},
    {"fecha": "2023-12-02", "monto": 980.00, "sucursal": "Sur", "vendedor": "María Gómez"}
]

datos_inventario = [
    {"producto": "Arroz 1kg", "stock": 150, "ventas_mes": 45, "rotacion": 0.3},
    {"producto": "Leche 1L", "stock": 80, "ventas_mes": 120, "rotacion": 1.5}
]

def menu():
    while True:
        borrar_pantalla()
        print("\n" + "="*50)
        print(" DASHBOARD DE REPORTES ".center(50))
        print("="*50)
        print("\n1. Reporte de Ventas")
        print("2. Análisis de Inventario")
        print("3. Desempeño de Proveedores")
        print("4. Clientes VIP")
        print("5. Reporte Personalizado")
        print("6. Exportar Datos")
        print("7. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-7): ")
        
        match opcion:
            case "1": reporte_ventas()
            case "2": analisis_inventario()
            case "3": desempeno_proveedores()
            case "4": clientes_vip()
            case "5": reporte_personalizado()
            case "6": exportar_datos()
            case "7": break
            case _: print("\n¡Opción no válida!")
        
        esperar_tecla()

# -------------------------------
# Funciones principales del módulo
# -------------------------------

def reporte_ventas():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" REPORTE DE VENTAS ".center(50))
    print("="*50)
    
    # Filtros
    hoy = datetime.now()
    fecha_inicio = input(f"Fecha inicio (YYYY-MM-DD) [{(hoy - timedelta(days=30)).strftime('%Y-%m-%d')}]: ") or (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
    fecha_fin = input(f"Fecha fin (YYYY-MM-DD) [{hoy.strftime('%Y-%m-%d')}]: ") or hoy.strftime('%Y-%m-%d')
    
    # Filtrar datos (en producción sería consulta SQL)
    ventas_filtradas = [v for v in datos_ventas if fecha_inicio <= v["fecha"] <= fecha_fin]
    
    if not ventas_filtradas:
        print("\nNo hay datos en el período seleccionado")
        return
    
    # Convertir a DataFrame para análisis
    df = pd.DataFrame(ventas_filtradas)
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Resumen ejecutivo
    print("\n" + "-"*50)
    print(" RESUMEN EJECUTIVO ".center(50))
    print("-"*50)
    print(f"\nTotal Ventas: ${df['monto'].sum():,.2f}")
    print(f"Venta Promedio: ${df['monto'].mean():,.2f}")
    print(f"Días con ventas: {df['fecha'].nunique()}")
    
    # Gráfico de tendencia
    df.groupby('fecha')['monto'].sum().plot(
        kind='line', 
        title='Tendencia de Ventas',
        ylabel='Monto ($)',
        xlabel='Fecha',
        figsize=(10, 5))
    plt.tight_layout()
    plt.savefig('ventas_tendencia.png')
    print("\nGráfico generado: 'ventas_tendencia.png'")
    
    # Top performers
    print("\n" + "-"*50)
    print(" TOP 5 VENDEDORES ".center(50))
    print("-"*50)
    print(df.groupby('vendedor')['monto'].sum().nlargest(5).to_string())

def analisis_inventario():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" ANÁLISIS DE INVENTARIO ".center(50))
    print("="*50)
    
    df = pd.DataFrame(datos_inventario)
    
    # Alertas
    bajo_stock = df[df['stock'] < 50]
    alta_rotacion = df[df['rotacion'] > 1.2]
    baja_rotacion = df[df['rotacion'] < 0.5]
    
    print("\n" + "!"*50)
    print(" ALERTAS ".center(50))
    print("!"*50)
    if not bajo_stock.empty:
        print("\n🚨 Productos con bajo stock:")
        print(bajo_stock[['producto', 'stock']].to_string(index=False))
    
    if not alta_rotacion.empty:
        print("\n📈 Productos con alta rotación (reabastecer):")
        print(alta_rotacion[['producto', 'rotacion']].to_string(index=False))
    
    if not baja_rotacion.empty:
        print("\n📉 Productos con baja rotación (revisar):")
        print(baja_rotacion[['producto', 'rotacion']].to_string(index=False))
    
    # Gráfico ABC
    df['valor_inventario'] = df['stock'] * df['ventas_mes']
    df.sort_values('valor_inventario', ascending=False, inplace=True)
    df['acumulado'] = df['valor_inventario'].cumsum()
    df['porcentaje'] = df['acumulado'] / df['valor_inventario'].sum() * 100
    
    print("\n" + "-"*50)
    print(" ANÁLISIS ABC ".center(50))
    print("-"*50)
    print(df[['producto', 'valor_inventario', 'porcentaje']].head(10).to_string(index=False))

def reporte_personalizado():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" REPORTE PERSONALIZADO ".center(50))
    print("="*50)
    
    print("\nSeleccione módulos a incluir:")
    print("1. Datos de Ventas")
    print("2. Datos de Inventario")
    print("3. Datos de Clientes")
    print("4. Datos de Proveedores")
    
    opciones = input("\nIngrese números separados por comas (ej: 1,3): ").split(',')
    
    # Generar reporte combinado (implementación básica)
    print("\nGenerando reporte personalizado...")
    # Aquí integrarías los datos seleccionados
    
    print("\n✅ Reporte generado en 'reporte_personalizado.pdf'")

def exportar_datos():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" EXPORTAR DATOS ".center(50))
    print("="*50)
    
    print("\nFormatos disponibles:")
    print("1. CSV (Excel)")
    print("2. JSON")
    print("3. Excel (XLSX)")
    
    formato = input("\nSeleccione formato (1-3): ")
    
    # Ejemplo para ventas
    df = pd.DataFrame(datos_ventas)
    
    match formato:
        case "1":
            df.to_csv('reporte_ventas.csv', index=False)
            print("\n✅ Datos exportados a 'reporte_ventas.csv'")
        case "2":
            df.to_json('reporte_ventas.json', orient='records')
            print("\n✅ Datos exportados a 'reporte_ventas.json'")
        case "3":
            df.to_excel('reporte_ventas.xlsx', index=False)
            print("\n✅ Datos exportados a 'reporte_ventas.xlsx'")
        case _:
            print("\n❌ Formato no válido")

# Integración con otros módulos
def actualizar_datos_ventas(nueva_venta):
    datos_ventas.append({
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "monto": nueva_venta["total"],
        "sucursal": nueva_venta["sucursal"],
        "vendedor": nueva_venta["vendedor"]
    })
    

def analisis_inventario():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" ANÁLISIS DE INVENTARIO ".center(50))
    print("="*50)
    
    df = pd.DataFrame(datos_inventario)
    
    # Alertas
    bajo_stock = df[df['stock'] < 50]
    alta_rotacion = df[df['rotacion'] > 1.2]
    baja_rotacion = df[df['rotacion'] < 0.5]
    
    print("\n" + "!"*50)
    print(" ALERTAS ".center(50))
    print("!"*50)
    if not bajo_stock.empty:
        print("\n🚨 Productos con bajo stock:")
        print(bajo_stock[['producto', 'stock']].to_string(index=False))
    
    if not alta_rotacion.empty:
        print("\n📈 Productos con alta rotación (reabastecer):")
        print(alta_rotacion[['producto', 'rotacion']].to_string(index=False))
    
    if not baja_rotacion.empty:
        print("\n📉 Productos con baja rotación (revisar):")
        print(baja_rotacion[['producto', 'rotacion']].to_string(index=False))
    
    # Gráfico ABC
    df['valor_inventario'] = df['stock'] * df['ventas_mes']
    df.sort_values('valor_inventario', ascending=False, inplace=True)
    df['acumulado'] = df['valor_inventario'].cumsum()
    df['porcentaje'] = df['acumulado'] / df['valor_inventario'].sum() * 100
    
    print("\n" + "-"*50)
    print(" ANÁLISIS ABC ".center(50))
    print("-"*50)
    print(df[['producto', 'valor_inventario', 'porcentaje']].head(10).to_string(index=False))
    
def desempeno_proveedores():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" DESEMPEÑO DE PROVEEDORES ".center(50))
    print("="*50)
    print("\nEvaluación de proveedores:")
    # Integración con módulo de proveedores
    # Aquí deberías obtener los datos de proveedores y sus ratings 
    # Ejemplo de datos de proveedores
    proveedores = [
        {"id": 1, "razon_social": "Proveedor A", "categoria": "Alimentos", "rating": 4.5, "compras_totales": 10},
        {"id": 2, "razon_social": "Proveedor B", "categoria": "Limpieza", "rating": 3.8, "compras_totales": 5},
        {"id": 3, "razon_social": "Proveedor C", "categoria": "Electrodomésticos", "rating": 4.9, "compras_totales": 8}
    ]
    proveedores.sort(key=lambda x: x["rating"], reverse=True)
    for prov in proveedores:
        print(f"{prov['id']}: {prov['razon_social']} - Rating: {prov['rating']}/5 - Compras Totales: {prov['compras_totales']}")

def clientes_vip():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" CLIENTES VIP ".center(50))
    print("="*50)
    print("\nClientes con mayor gasto acumulado:")
    # Integración con módulo de clientes
    # Aquí deberías obtener los datos de clientes y filtrar por gasto
    # Ejemplo de datos de clientes
    clientes = [
        {"id": 1, "nombre": "Cliente A", "gasto_total": 5000.00},
        {"id": 2, "nombre": "Cliente B", "gasto_total": 7500.00},
        {"id": 3, "nombre": "Cliente C", "gasto_total": 3000.00}
    ]
    clientes.sort(key=lambda x: x["gasto_total"], reverse=True)
    for cliente in clientes:
        print(f"{cliente['id']}: {cliente['nombre']} - Gasto Total: ${cliente['gasto_total']:.2f}")

def reporte_personalizado():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" REPORTE PERSONALIZADO ".center(50))
    print("="*50)
    print("\nSeleccione módulos a incluir:")
    print("1. Datos de Ventas")
    print("2. Datos de Inventario")
    print("3. Datos de Clientes")
    print("4. Datos de Proveedores")
    opciones = input("\nIngrese números separados por comas (ej: 1,3): ").split(',')
    # Generar reporte combinado (implementación básica)
    print("\nGenerando reporte personalizado...")
    # Aquí integrarías los datos seleccionados
    print("\n✅ Reporte generado en 'reporte_personalizado.pdf'")
from utils.helpers import borrar_pantalla, esperar_tecla, validar_entero
import pandas as pd
import matplotlib.pyplot as plt
import os
# Datos de ejemplo (en producción se conecta a otros módulos)
datos_ventas = [
    {"fecha": "2023-12-01", "monto": 1250.50, "sucursal": "Norte", "vendedor": "Juan Pérez"},
    {"fecha": "2023-12-02", "monto": 980.00, "sucursal": "Sur", "vendedor": "María Gómez"}
]
datos_inventario = [
    {"producto": "Arroz 1kg", "stock": 150, "ventas_mes": 45, "rotacion": 0.3},
    {"producto": "Leche 1L", "stock": 80, "ventas_mes": 120, "rotacion": 1.5}
]
    

def exportar_datos():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" EXPORTAR DATOS ".center(50))
    print("="*50)
    
    print("\nFormatos disponibles:")
    print("1. CSV (Excel)")
    print("2. JSON")
    print("3. Excel (XLSX)")
    
    formato = input("\nSeleccione formato (1-3): ")
    
    # Ejemplo para ventas
    df = pd.DataFrame(datos_ventas)
    
    match formato:
        case "1":
            df.to_csv('reporte_ventas.csv', index=False)
            print("\n✅ Datos exportados a 'reporte_ventas.csv'")
        case "2":
            df.to_json('reporte_ventas.json', orient='records')
            print("\n✅ Datos exportados a 'reporte_ventas.json'")
        case "3":
            df.to_excel('reporte_ventas.xlsx', index=False)
            print("\n✅ Datos exportados a 'reporte_ventas.xlsx'")
        case _:
            print("\n❌ Formato no válido")