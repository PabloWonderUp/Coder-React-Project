# Excel Invoice - Procesador de Facturas Argentinas

Script para extraer datos de facturas argentinas en PDF y exportarlos a Google Sheets.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso básico

### Factura única (salida JSON por consola)
```bash
python3 procesar_facturas.py factura.pdf
```

### Múltiples facturas
```bash
python3 procesar_facturas.py factura1.pdf factura2.pdf factura3.pdf
```

### Guardar resultado en archivo JSON
```bash
python3 procesar_facturas.py factura.pdf -o resultado.json
```

### Modo depuración (muestra el texto extraído)
```bash
python3 procesar_facturas.py factura.pdf --texto
```

## Exportar a Google Sheets

### 1. Configurar credenciales

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un proyecto (o usar uno existente)
3. Habilitar las APIs: **Google Sheets API** y **Google Drive API**
4. Crear una **Cuenta de servicio** (IAM > Cuentas de servicio)
5. Generar una clave JSON y guardarla como `credenciales.json` en la carpeta del proyecto
6. Compartir tu Google Spreadsheet con el email de la cuenta de servicio (el que termina en `@...iam.gserviceaccount.com`)

### 2. Ejecutar con exportación a Sheets

```bash
# Usando el ID del spreadsheet (lo que aparece en la URL entre /d/ y /edit)
python3 procesar_facturas.py factura.pdf --sheets 1AbCdEfGhIjKlMnOpQrStUvWxYz

# Especificar archivo de credenciales y nombre de hoja
python3 procesar_facturas.py factura.pdf \
  --sheets 1AbCdEfGhIjKlMnOpQrStUvWxYz \
  --credenciales mi_cuenta_servicio.json \
  --hoja "Facturas 2025"
```

### Opciones de Google Sheets

| Opción          | Default             | Descripción                                      |
|-----------------|---------------------|--------------------------------------------------|
| `--sheets`      | *(requerido)*       | ID del Google Spreadsheet                        |
| `--credenciales`| `credenciales.json` | Ruta al JSON de cuenta de servicio               |
| `--hoja`        | `Hoja 1`            | Nombre de la hoja de trabajo dentro del Spreadsheet |

## Datos extraídos

| Campo          | Descripción                                      |
|----------------|--------------------------------------------------|
| Proveedor      | Razón social del emisor                          |
| Tipo de Gastos | "Coord. Dptos." o "Coord. Areas" (si aplica)    |
| Detalle        | (vacío)                                          |
| Monto          | Importe total sin $ ni separador de miles        |
| Nota           | Observaciones de la factura                      |
| Nro. Factura   | Número de comprobante (ej: 0001-00001874)        |
| Transferencia  | (vacío)                                          |

## Ejemplo de salida JSON

```json
{
  "proveedor": "Juan Pérez S.A.",
  "tipo_gastos": "",
  "detalle": "",
  "monto": "38000.00",
  "nota": "",
  "nro_factura": "0001-00001874",
  "transferencia": ""
}
```
