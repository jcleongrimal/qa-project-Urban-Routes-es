# Urban Routes — Pruebas automatizadas de interfaz de usuario

Proyecto del **Sprint 9 de QA Engineering de TripleTen**. Automatiza en Python el flujo de solicitud de un taxi en la aplicación web **Urban Routes**, utilizando **Selenium WebDriver**, **pytest** y el patrón de diseño **Page Object Model (POM)**.

## Descripción del proyecto

El proyecto comprueba las acciones del usuario para solicitar un taxi: configurar las direcciones de origen y destino, seleccionar la tarifa Comfort, confirmar el número telefónico, agregar una tarjeta, escribir un mensaje al conductor, activar manta y pañuelos, solicitar dos helados y verificar que aparezca la ventana **«Buscar automóvil»**.

La comprobación posterior de la información del conductor es opcional en el enunciado de TripleTen y no está automatizada en esta entrega.

## Tecnologías y técnicas utilizadas

- **Python 3** para implementar las pruebas.
- **Selenium WebDriver** para interactuar con los elementos de la interfaz en Google Chrome.
- **pytest** para ejecutar pruebas y validar resultados mediante `assert`.
- **Page Object Model (POM)** para separar los localizadores y métodos de interacción de los casos de prueba.
- **WebDriverWait** y condiciones esperadas para gestionar elementos que cargan dinámicamente.
- **Localizadores** por ID, nombre de clase, CSS y XPath.
- **Registros de rendimiento de Chrome** y la función provista por TripleTen `retrieve_phone_code()` para obtener el código de confirmación de la aplicación de prueba.

## Archivos principales

| Archivo | Función |
| --- | --- |
| `main.py` | Clase `UrbanRoutesPage`, pruebas `TestUrbanRoutes` y función de recuperación del código telefónico. |
| `data.py` | URL del entorno Urban Routes y datos empleados por las pruebas. |
| `README.md` | Descripción e instrucciones de ejecución. |

## Requisitos previos

- Python 3 instalado.
- Google Chrome instalado.
- Conexión a Internet y acceso al entorno de pruebas de TripleTen.
- Bibliotecas Python `selenium` y `pytest`.

## Instalación y ejecución

En PowerShell, desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install selenium pytest
```

> Si el entorno virtual `.venv` ya existe y tiene instaladas las dependencias, basta con activarlo. Selenium puede gestionar el controlador compatible de Chrome mediante Selenium Manager.

Comprueba que la dirección `urban_routes_url` definida en `data.py` corresponde a un servidor **Urban Routes activo** de TripleTen. Estos entornos pueden caducar; en ese caso, actualiza únicamente la URL con la proporcionada para el proyecto.

Ejecuta las ocho pruebas:

```powershell
python -m pytest main.py -v
```

Para ejecutar una sola prueba, por ejemplo la solicitud completa del taxi:

```powershell
python -m pytest main.py::TestUrbanRoutes::test_book_taxi -v
```

## Casos automatizados

| Prueba | Escenario |
| --- | --- |
| `test_set_route` | Introducir origen y destino. |
| `test_select_comfort_tariff` | Seleccionar la tarifa Comfort. |
| `test_phone_number` | Introducir y confirmar el teléfono mediante el código obtenido del entorno de pruebas. |
| `test_add_card` | Completar el formulario para agregar una tarjeta. |
| `test_driver_message` | Introducir y comprobar el mensaje para el conductor. |
| `test_blanket_and_tissues` | Activar y comprobar la opción de manta y pañuelos. |
| `test_two_ice_creams` | Solicitar y comprobar exactamente dos helados. |
| `test_book_taxi` | Completar el recorrido y verificar la aparición del modal «Buscar automóvil». |

## Resultado de la última ejecución local

En la ejecución conjunta comunicada el **11 de noviembre de 2026**, pytest informó **8 pruebas aprobadas en 30,64 segundos** (`8 passed in 30.64s`). Este resultado describe esa ejecución; puede cambiar según la disponibilidad del servidor de pruebas y el entorno local.

## Notas

- Los datos de `data.py` son valores destinados al entorno de práctica; no se utilizan credenciales reales.
- La función `retrieve_phone_code()` se conserva según la plantilla proporcionada por TripleTen.
- El navegador se abre durante las pruebas y se cierra al finalizar la clase de pruebas.
