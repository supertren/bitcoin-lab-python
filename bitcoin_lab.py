#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Laboratorio de Bitcoin Sencillo
-------------------------------
Este script demuestra operaciones básicas con Bitcoin usando la biblioteca 'bit'.
Incluye la generación de direcciones, consulta de saldos y simulación de transacciones.
"""

import bit
from bit import Key
from bit.network import get_fee_cached
from bit.format import bytes_to_wif
import os
import secrets
import requests

def generar_clave_privada():
    """Genera una clave privada aleatoria para Bitcoin."""
    # Generamos 32 bytes aleatorios (256 bits) de entropía
    entropía = secrets.token_bytes(32)
    # Convertimos los bytes a formato WIF (Wallet Import Format)
    clave_privada_wif = bytes_to_wif(entropía, compressed=True)
    return clave_privada_wif

def crear_billetera():
    """Crea una nueva billetera de Bitcoin."""
    clave_privada = generar_clave_privada()
    billetera = Key(clave_privada)
    return {
        'clave_privada': billetera.to_wif(),
        'dirección': billetera.address,
        'formato': 'P2PKH (Legacy)'
    }

def crear_billetera_segwit():
    """Crea una nueva billetera SegWit de Bitcoin."""
    clave_privada = generar_clave_privada()
    billetera = bit.SegWitKey.from_wif(Key(clave_privada).to_wif())
    return {
        'clave_privada': billetera.to_wif(),
        'dirección': billetera.segwit_address,
        'formato': 'P2SH-P2WPKH (SegWit)'
    }

def obtener_saldo(dirección):
    """Obtiene el saldo de una dirección de Bitcoin en satoshis."""
    try:
        return bit.network.get_balance(dirección)
    except Exception as e:
        return f"Error al obtener saldo: {e}"

def obtener_historial_transacciones(dirección):
    """Obtiene el historial de transacciones de una dirección de Bitcoin."""
    try:
        return bit.network.get_transactions(dirección)
    except Exception as e:
        return f"Error al obtener historial: {e}"

def estimar_comisión():
    """Estima la comisión actual de la red Bitcoin en satoshis/byte."""
    try:
        return get_fee_cached()
    except Exception as e:
        return f"Error al estimar comisión: {e}"

def obtener_precio_bitcoin():
    """Obtiene el precio actual de Bitcoin en USD."""
    try:
        respuesta = requests.get('https://api.coindesk.com/v1/bpi/currentprice/USD.json')
        datos = respuesta.json()
        return float(datos['bpi']['USD']['rate'].replace(',', ''))
    except Exception as e:
        return f"Error al obtener precio: {e}"

def simular_transacción(origen_wif, destino_dirección, cantidad_btc):
    """Simula una transacción de Bitcoin (sin enviarla realmente)."""
    try:
        billetera = Key(origen_wif)
        tx_hex = billetera.create_transaction(
            [(destino_dirección, cantidad_btc, 'btc')],
            fee=estimar_comisión(),
            absolute_fee=True,
            message='Transacción de prueba del laboratorio de Bitcoin'
        )
        return {
            'origen': billetera.address,
            'destino': destino_dirección,
            'cantidad_btc': cantidad_btc,
            'tx_hex': tx_hex
        }
    except Exception as e:
        return f"Error al crear transacción: {e}"

def mostrar_menu():
    """Muestra el menú principal del laboratorio."""
    print("\n===== LABORATORIO DE BITCOIN =====")
    print("1. Crear nueva billetera Bitcoin (Legacy)")
    print("2. Crear nueva billetera Bitcoin (SegWit)")
    print("3. Consultar saldo de dirección")
    print("4. Consultar historial de transacciones")
    print("5. Estimar comisión actual de la red")
    print("6. Consultar precio actual de Bitcoin")
    print("7. Simular transacción")
    print("0. Salir")
    print("================================")

def main():
    """Función principal del laboratorio."""
    billeteras = []
    
    while True:
        mostrar_menu()
        opción = input("\nSeleccione una opción: ")
        
        if opción == "1":
            nueva_billetera = crear_billetera()
            billeteras.append(nueva_billetera)
            print("\n--- NUEVA BILLETERA CREADA (LEGACY) ---")
            print(f"Dirección: {nueva_billetera['dirección']}")
            print(f"Clave privada (WIF): {nueva_billetera['clave_privada']}")
            print("IMPORTANTE: Guarde su clave privada en un lugar seguro!")
            
        elif opción == "2":
            nueva_billetera = crear_billetera_segwit()
            billeteras.append(nueva_billetera)
            print("\n--- NUEVA BILLETERA CREADA (SEGWIT) ---")
            print(f"Dirección: {nueva_billetera['dirección']}")
            print(f"Clave privada (WIF): {nueva_billetera['clave_privada']}")
            print("IMPORTANTE: Guarde su clave privada en un lugar seguro!")
            
        elif opción == "3":
            dirección = input("Ingrese la dirección de Bitcoin: ")
            saldo = obtener_saldo(dirección)
            if isinstance(saldo, int):
                print(f"\nSaldo: {saldo} satoshis ({saldo/100000000:.8f} BTC)")
            else:
                print(saldo)
                
        elif opción == "4":
            dirección = input("Ingrese la dirección de Bitcoin: ")
            transacciones = obtener_historial_transacciones(dirección)
            if isinstance(transacciones, list):
                print(f"\nHistorial de transacciones para {dirección}:")
                for i, tx in enumerate(transacciones, 1):
                    print(f"{i}. TxID: {tx}")
            else:
                print(transacciones)
                
        elif opción == "5":
            comisión = estimar_comisión()
            if isinstance(comisión, int):
                print(f"\nComisión estimada: {comisión} satoshis/byte")
            else:
                print(comisión)
                
        elif opción == "6":
            precio = obtener_precio_bitcoin()
            if isinstance(precio, float):
                print(f"\nPrecio actual de Bitcoin: ${precio:,.2f} USD")
            else:
                print(precio)
                
        elif opción == "7":
            if not billeteras:
                print("\nPrimero debe crear al menos una billetera (opción 1 o 2).")
                continue
                
            print("\nBilleteras disponibles:")
            for i, wallet in enumerate(billeteras, 1):
                print(f"{i}. {wallet['dirección']} ({wallet['formato']})")
                
            try:
                índice = int(input("\nSeleccione billetera de origen (número): ")) - 1
                if índice < 0 or índice >= len(billeteras):
                    print("Selección inválida.")
                    continue
                    
                origen_wif = billeteras[índice]['clave_privada']
                destino = input("Ingrese dirección de destino: ")
                cantidad = float(input("Ingrese cantidad en BTC: "))
                
                resultado = simular_transacción(origen_wif, destino, cantidad)
                if isinstance(resultado, dict):
                    print("\n--- TRANSACCIÓN SIMULADA ---")
                    print(f"Origen: {resultado['origen']}")
                    print(f"Destino: {resultado['destino']}")
                    print(f"Cantidad: {resultado['cantidad_btc']} BTC")
                    print(f"Transacción hex: {resultado['tx_hex'][:64]}...")
                    print("NOTA: Esta es solo una simulación, no se ha enviado ninguna transacción real.")
                else:
                    print(resultado)
            except ValueError:
                print("Entrada inválida. Ingrese un número válido.")
                
        elif opción == "0":
            print("\nGracias por usar el Laboratorio de Bitcoin. ¡Hasta pronto!")
            break
            
        else:
            print("\nOpción inválida. Por favor, seleccione una opción válida.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
