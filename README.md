# Excel Invoice - Procesador de Facturas Argentinas

Script para extraer datos de facturas argentinas en PDF y generar JSON estructurado.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Factura única
```bash
python3 procesar_facturas.py factura.pdf
```

### Múltiples facturas
```bash
python3 procesar_facturas.py factura1.pdf factura2.pdf factura3.pdf
```

### Guardar resultado en archivo
```bash
python3 procesar_facturas.py factura.pdf -o resultado.json
```

### Modo depuración (muestra el texto extraído)
```bash
python3 procesar_facturas.py factura.pdf --texto
```

## Datos extraídos

| Campo          | Descripción                                      |
|----------------|--------------------------------------------------|
| proveedor      | Razón social del emisor                          |
| tipo_gastos    | "Coord. Dptos." o "Coord. Areas" (si aplica)    |
| detalle        | (vacío)                                          |
| monto          | Importe total sin $ ni separador de miles        |
| nota           | Observaciones de la factura                      |
| nro_factura    | Número de comprobante (ej: 0001-00001874)        |
| transferencia  | (vacío)                                          |

## Ejemplo de salida

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
