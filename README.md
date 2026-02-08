# Excel Invoice

Hola Cande! Soy Churro y te voy a ayudar a facturar.

Este proyecto hace dos cosas:
1. Lee tus facturas en PDF y saca los datos importantes.
2. Carga esos datos en tu Google Sheets automáticamente.

Todo está explicado paso a paso, seguí las instrucciones en orden y vas a ver que es fácil.

---

## Paso 1: Preparar tu computadora (una sola vez)

Antes de empezar, necesitás tener **Python** instalado. Si ya lo tenés, salteá al paso 1.2.

### 1.1 Instalar Python

1. Abrí tu navegador y entrá a https://www.python.org/downloads/
2. Hacé clic en el botón amarillo grande que dice **"Download Python"**
3. Abrí el archivo que se descargó
4. **MUY IMPORTANTE**: En la primera pantalla del instalador, marcá la casilla que dice **"Add Python to PATH"** (está abajo de todo)
5. Hacé clic en **"Install Now"** y esperá a que termine

### 1.2 Abrir la terminal

La terminal es una ventana donde vas a escribir comandos. No te asustes, solo vas a copiar y pegar lo que te digo acá.

**En Windows:**
- Apretá la tecla de **Windows** (la del logo) + la letra **R** al mismo tiempo
- Se abre un cuadrito. Escribí `cmd` y apretá **Enter**
- Se abre una ventana negra. Esa es la terminal.

**En Mac:**
- Apretá **Cmd + Espacio** (se abre el buscador Spotlight)
- Escribí `Terminal` y apretá **Enter**

### 1.3 Ir a la carpeta del proyecto

Ahora necesitás decirle a la terminal dónde están los archivos. Supongamos que descargaste este proyecto en tu carpeta de Descargas:

**En Windows**, copiá y pegá esto en la terminal y apretá **Enter**:
```
cd %USERPROFILE%\Downloads\Coder-React-Project
```

**En Mac**, copiá y pegá esto en la terminal y apretá **Enter**:
```
cd ~/Downloads/Coder-React-Project
```

(Si lo guardaste en otra carpeta, cambiá la ruta por la que corresponda.)

### 1.4 Instalar lo que necesita el script

Copiá y pegá esto en la terminal y apretá **Enter**:

```
pip install -r requirements.txt
```

Va a aparecer texto en la pantalla, esperá a que termine. Cuando vuelvas a ver el cursor parpadeando, ya está.

---

## Paso 2: Procesar tus facturas PDF

Cada vez que tengas facturas nuevas, hacé lo siguiente:

### 2.1 Poné tus PDFs en la carpeta del proyecto

Copiá los archivos PDF de las facturas y pegalos dentro de la carpeta del proyecto (la misma donde están `procesar_facturas.py` y los demás archivos).

### 2.2 Abrí la terminal y andá a la carpeta

(Si ya la tenés abierta del paso anterior, salteá esto.)

Igual que antes:
- **Windows**: tecla Windows + R, escribí `cmd`, Enter
- **Mac**: Cmd + Espacio, escribí `Terminal`, Enter

Y después el comando `cd` del paso 1.3 para ir a la carpeta del proyecto.

### 2.3 Ejecutá el script

Copiá y pegá esto en la terminal, pero **cambiá `factura.pdf` por el nombre real de tu archivo**:

```
python procesar_facturas.py factura.pdf -o resultado.json
```

Por ejemplo, si tu factura se llama `factura_marzo_2025.pdf`:

```
python procesar_facturas.py factura_marzo_2025.pdf -o resultado.json
```

Si tenés **varias facturas**, podés ponerlas todas juntas:

```
python procesar_facturas.py factura1.pdf factura2.pdf factura3.pdf -o resultado.json
```

### 2.4 Copiá el resultado

Ahora tenés un archivo nuevo llamado `resultado.json` en la carpeta del proyecto.

1. Abrí el archivo `resultado.json` (hacele doble clic o clic derecho > "Abrir con" > Bloc de notas)
2. Seleccioná **todo** el contenido (Ctrl+A)
3. Copialo (Ctrl+C)

Lo que vas a ver es algo así:

```json
{
  "proveedor": "Juan Pérez S.A.",
  "tipo_gastos": "",
  "detalle": "",
  "monto": "38000.00",
  "nota": "",
  "nro_factura": "874",
  "transferencia": ""
}
```

El número de factura muestra solo los últimos 3 dígitos. Por ejemplo, si la factura completa es 0001-00001874, vas a ver "874".

Ese texto que copiaste lo vas a necesitar en el siguiente paso. **No cierres el bloc de notas todavía.**

---

## Paso 3: Cargar los datos en Google Sheets

### Configuración (una sola vez)

Esto lo hacés una sola vez. Después ya queda listo para siempre.

1. Abrí tu Google Spreadsheet donde querés cargar las facturas
2. En el menú de arriba, hacé clic en **Extensiones**
3. Hacé clic en **Apps Script** (se abre una pestaña nueva)
4. En esa pestaña nueva vas a ver un editor con código. **Seleccioná todo** (Ctrl+A) y **borralo** (tecla Suprimir o Backspace)
5. Ahora abrí el archivo `cargar_en_sheets.gs` de este proyecto (está en la misma carpeta). Abrilo con el Bloc de notas (clic derecho > "Abrir con" > Bloc de notas)
6. Seleccioná **todo** el contenido (Ctrl+A) y copialo (Ctrl+C)
7. Volvé a la pestaña de Apps Script y pegalo (Ctrl+V)
8. Hacé clic en el ícono de **Guardar** (el disquete arriba) o apretá Ctrl+S
9. Cerrá la pestaña de Apps Script
10. **Recargá** tu hoja de cálculo (apretá F5 o Ctrl+R)

Si todo salió bien, ahora vas a ver un nuevo menú que dice **"Facturas"** en la barra de arriba de tu Google Sheet (al lado de "Herramientas").

### Cargar las facturas (uso diario)

Cada vez que proceses facturas nuevas (Paso 2), hacé esto:

1. En tu Google Sheet, hacé clic en el menú **Facturas** (arriba)
2. Hacé clic en **Cargar JSON**
3. Se abre un cuadro con un espacio en blanco grande
4. Pegá ahí el contenido que copiaste del archivo `resultado.json` (Ctrl+V)
5. Hacé clic en el botón **"Cargar en la hoja"**
6. Va a aparecer un mensaje diciendo cuántas facturas se cargaron. Hacé clic en **Aceptar**

Listo! Los datos ya están en tu hoja. Cada vez que cargues facturas nuevas, se agregan abajo de las anteriores.

**Nota:** La primera vez que lo uses, Google te puede pedir permiso para ejecutar el script. Dale clic a "Permitir" o "Autorizar". Es normal, solo pasa una vez.

---

## Resumen rápido (cuando ya le agarres la mano)

1. Poné los PDFs en la carpeta del proyecto
2. Abrí la terminal, andá a la carpeta, ejecutá:
   ```
   python procesar_facturas.py factura.pdf -o resultado.json
   ```
3. Abrí `resultado.json`, seleccioná todo (Ctrl+A), copiá (Ctrl+C)
4. En Google Sheets: **Facturas > Cargar JSON** > pegá > **Cargar en la hoja**

---

## Datos que se extraen de cada factura

| Columna        | Qué es                                           |
|----------------|--------------------------------------------------|
| Proveedor      | Razón social de quien emite la factura           |
| Tipo de Gastos | "Coord. Dptos." o "Coord. Areas" si aplica       |
| Detalle        | (vacío)                                          |
| Monto          | Importe total, sin $ ni puntos de miles          |
| Nota           | Observaciones que tenga la factura               |
| Nro. Factura   | Últimos 3 dígitos del número de comprobante      |
| Transferencia  | (vacío)                                          |

---

## Algo no funciona?

- **"python no se reconoce como comando"**: Probá escribir `python3` en vez de `python`. Si tampoco funciona, volvé al Paso 1.1 y reinstalá Python asegurándote de marcar "Add Python to PATH".
- **"No se encontró el archivo"**: Revisá que el nombre del PDF esté bien escrito y que el archivo esté en la carpeta del proyecto.
- **No aparece el menú "Facturas" en Google Sheets**: Recargá la página (F5). Si sigue sin aparecer, repetí la configuración del Paso 3.
