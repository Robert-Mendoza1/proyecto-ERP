from modulos import inventario, compras, ventas, proveedores, clientes, reportes
from utils.helpers import borrar_pantalla, esperar_tecla

def menu_principal():
    borrar_pantalla()
    print("\n" + "="*50)
    print(" ERP - GESTIÓN CADENA DE SUMINISTRO MINORISTA ".center(50))
    print("="*50)
    print("\n1. Módulo de Inventario")
    print("2. Módulo de Compras")
    print("3. Módulo de Ventas")
    print("4. Módulo de Proveedores")
    print("5. Módulo de Clientes")
    print("6. Reportes y Analytics")
    print("7. Salir")
    return input("\nSeleccione una opción (1-7): ")

def main():
    while True:
        opcion = menu_principal()
        
        match opcion:
            case "1": inventario.menu()
            case "2": compras.menu()
            case "3": ventas.menu()
            case "4": proveedores.menu()
            case "5": clientes.menu()
            case "6": reportes.menu()
            case "7":
                print("\nSaliendo del sistema...")
                break
            case _:
                print("\n¡Opción no válida!")
        
        esperar_tecla()

if __name__ == "__main__":
    main()