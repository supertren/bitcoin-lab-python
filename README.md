# Laboratorio de Bitcoin en Python

Este proyecto es un laboratorio sencillo para aprender y experimentar con operaciones básicas de Bitcoin utilizando Python.

## Características

- Creación de billeteras Bitcoin (Legacy y SegWit)
- Consulta de saldos de direcciones Bitcoin
- Consulta de historial de transacciones
- Estimación de comisiones de la red Bitcoin
- Consulta del precio actual de Bitcoin
- Simulación de transacciones (sin envío real)

## Requisitos

- Python 3.6 o superior
- Bibliotecas:
  - bit
  - requests

## Instalación

1. Clonar este repositorio:
```
git clone https://github.com/tu-usuario/bitcoin-lab-python.git
cd bitcoin-lab-python
```

2. Instalar las dependencias:
```
pip install bit requests
```

## Uso

Ejecutar el script principal:
```
python bitcoin_lab.py
```

El programa mostrará un menú interactivo con las siguientes opciones:

1. Crear nueva billetera Bitcoin (Legacy)
2. Crear nueva billetera Bitcoin (SegWit)
3. Consultar saldo de dirección
4. Consultar historial de transacciones
5. Estimar comisión actual de la red
6. Consultar precio actual de Bitcoin
7. Simular transacción
0. Salir

## Importante

- Este es un laboratorio educativo y no debe usarse para manejar fondos reales.
- Las claves privadas generadas son solo para fines de aprendizaje.
- Las transacciones son simuladas y no se envían realmente a la red Bitcoin.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerir cambios o mejoras.
