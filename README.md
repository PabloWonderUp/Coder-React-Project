# Excel Invoice

Hola Cande! Soy Churro y te voy a ayudar a facturar.

Este proyecto tiene dos partes:
1. **Un script de Python** que lee tus facturas en PDF y saca los datos importantes en formato JSON.
2. **Un script de Google Sheets** que toma ese JSON y lo carga directo en tu hoja de cálculo. Sin cuentas raras ni configuraciones complicadas.

---

## Paso 1: Extraer datos de las facturas PDF

### Instalación (una sola vez)

Abrí la terminal y ejecutá:

```bash
pip install -r requirements.txt
```

### Procesar facturas

Para una factura:

```bash
python3 procesar_facturas.py factura.pdf
```

Para varias facturas de una:

```bash
python3 procesar_facturas.py factura1.pdf factura2.pdf factura3.pdf
```

Si querés guardar el resultado en un archivo:

```bash
python3 procesar_facturas.py factura.pdf -o resultado.json
```

Esto te va a generar un JSON con los datos de cada factura. Copiá ese JSON porque lo vas a necesitar en el paso 2.

### Ejemplo de lo que genera

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

El número de factura muestra solo los últimos 3 dígitos (por ejemplo, si la factura es 0001-00001874, vas a ver "874").

---

## Paso 2: Cargar los datos en Google Sheets

Acá no necesitás instalar nada ni conectar cuentas. Todo se hace desde tu Google Sheets.

### Configuración (una sola vez)

1. Abrí tu Google Spreadsheet donde querés cargar las facturas
2. Andá al menú **Extensiones > Apps Script**
3. Borrá todo el código que aparece ahí
4. Abrí el archivo `cargar_en_sheets.gs` de este proyecto, copiá TODO el contenido y pegalo en el editor de Apps Script
5. Hacé clic en **Guardar** (o Ctrl+S)
6. Cerrá la pestaña de Apps Script
7. Recargá tu hoja de cálculo (F5)

Listo! Ahora vas a ver un nuevo menú **"Facturas"** en la barra de menú de tu Google Sheets.

### Uso diario

1. Ejecutá `procesar_facturas.py` con tus PDFs (Paso 1)
2. Copiá el JSON que te genera
3. En tu Google Sheet, andá a **Facturas > Cargar JSON**
4. Pegá el JSON en el cuadro que aparece
5. Hacé clic en **"Cargar en la hoja"**

Los datos se agregan automáticamente como nuevas filas. Si es la primera vez, también te crea los encabezados.

Si necesitás crear o recrear los encabezados manualmente, usá **Facturas > Crear encabezados**.

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
