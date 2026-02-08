#!/usr/bin/env python3
"""
Procesador de facturas argentinas en PDF.
Extrae datos clave de cada factura y genera un JSON estructurado.
"""

import argparse
import json
import os
import re
import sys

import pdfplumber


def extraer_texto(pdf_path: str) -> list[str]:
    """Extrae el texto de cada página del PDF."""
    paginas = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if texto:
                paginas.append(texto)
    return paginas


def buscar_patron(texto: str, patrones: list[str], grupo: int = 1) -> str:
    """Busca múltiples patrones regex en el texto y devuelve la primera coincidencia."""
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(grupo).strip()
    return ""


def extraer_proveedor(texto: str) -> str:
    """Extrae el nombre del proveedor / razón social del emisor."""
    patrones = [
        r"Raz[oó]n\s*Social\s*[:\-]?\s*(.+)",
        r"Apellido\s*y\s*Nombre\s*[/o]*\s*Raz[oó]n\s*Social\s*[:\-]?\s*(.+)",
        r"Nombre\s*(?:de\s*)?(?:Fantas[ií]a)?\s*[:\-]?\s*(.+)",
        r"Emisor\s*[:\-]?\s*(.+)",
    ]
    resultado = buscar_patron(texto, patrones)
    if resultado:
        # Limpiar texto residual después del nombre
        resultado = re.split(r"\s{2,}|\t|CUIT|Domicilio", resultado)[0].strip()
    return resultado


def extraer_nro_factura(texto: str) -> str:
    """Extrae el número de comprobante de la factura."""
    patrones = [
        r"Comp\.?\s*Nro\.?\s*[:\-]?\s*([\d]{4,5}\s*[-–]\s*[\d]+)",
        r"Nro\.?\s*(?:de\s*)?(?:Comp(?:robante)?|Factura)\s*[:\-]?\s*([\d]{4,5}\s*[-–]\s*[\d]+)",
        r"Punto\s*de\s*Venta\s*[:\-]?\s*(\d{4,5})\s*[-–]\s*Comp\.?\s*Nro\.?\s*[:\-]?\s*(\d+)",
        r"N[°º]?\s*[:\-]?\s*([\d]{4,5}\s*[-–]\s*[\d]+)",
    ]

    # Intentar primero los patrones de número completo
    for patron in patrones[:2]:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return re.sub(r"\s+", "", match.group(1))

    # Patrón de punto de venta + número separados
    match = re.search(patrones[2], texto, re.IGNORECASE)
    if match:
        punto_venta = match.group(1).zfill(4)
        numero = match.group(2).zfill(8)
        return f"{punto_venta}-{numero}"

    # Patrón genérico
    match = re.search(patrones[3], texto, re.IGNORECASE)
    if match:
        return re.sub(r"\s+", "", match.group(1))

    return ""


def extraer_monto(texto: str) -> str:
    """Extrae el monto total de la factura."""
    patrones = [
        r"Importe\s*Total\s*[:\$]?\s*\$?\s*([\d.,]+)",
        r"Total\s*[:\$]?\s*\$?\s*([\d.,]+)",
        r"TOTAL\s*[:\$]?\s*\$?\s*([\d.,]+)",
        r"Importe\s*(?:Otros\s*Tributos|Neto)\s*[:\$]?\s*\$?\s*([\d.,]+)",
    ]

    # Buscar el importe total (priorizar "Importe Total")
    for patron in patrones:
        matches = re.findall(patron, texto, re.IGNORECASE)
        if matches:
            # Tomar el último match (generalmente el total final)
            monto_str = matches[-1]
            return normalizar_monto(monto_str)
    return ""


def normalizar_monto(monto_str: str) -> str:
    """
    Normaliza un string de monto argentino a formato numérico.
    Argentina usa punto como separador de miles y coma como decimal.
    Ejemplo: "38.000,50" -> "38000.50"
    """
    monto_str = monto_str.strip()

    # Detectar formato argentino (punto = miles, coma = decimal)
    if "," in monto_str and "." in monto_str:
        # Tiene ambos: 38.000,50 -> quitar puntos de miles, reemplazar coma por punto
        monto_str = monto_str.replace(".", "").replace(",", ".")
    elif "," in monto_str:
        # Solo coma: 38000,50 -> reemplazar coma por punto decimal
        monto_str = monto_str.replace(",", ".")
    elif monto_str.count(".") > 1:
        # Múltiples puntos como separador de miles: 38.000.000 -> quitar puntos
        monto_str = monto_str.replace(".", "")

    try:
        valor = float(monto_str)
        return f"{valor:.2f}"
    except ValueError:
        return monto_str


def extraer_notas(texto: str) -> str:
    """Extrae observaciones o notas de la factura."""
    patrones = [
        r"Observaciones?\s*[:\-]?\s*(.+?)(?:\n\n|\nCAE|\nC\.A\.E|\nFecha\s*(?:de\s*)?Vto)",
        r"Notas?\s*[:\-]?\s*(.+?)(?:\n\n|\nCAE|\nC\.A\.E|\nFecha\s*(?:de\s*)?Vto)",
        r"Comentarios?\s*[:\-]?\s*(.+?)(?:\n\n|\nCAE|\nC\.A\.E|\nFecha\s*(?:de\s*)?Vto)",
    ]
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
        if match:
            nota = match.group(1).strip()
            # Limpiar saltos de línea internos
            nota = re.sub(r"\s*\n\s*", " ", nota).strip()
            if nota and nota.lower() not in ("n/a", "-", ""):
                return nota
    return ""


def detectar_facturas_en_texto(paginas: list[str]) -> list[str]:
    """
    Detecta si hay múltiples facturas en el PDF.
    Cada factura suele comenzar con un encabezado de tipo de comprobante.
    """
    texto_completo = "\n\n--- NUEVA PAGINA ---\n\n".join(paginas)

    # Intentar dividir por marcadores comunes de inicio de factura
    marcadores = [
        r"(?=FACTURA\s+[A-Z])",
        r"(?=NOTA\s+DE\s+(?:CR[ÉE]DITO|D[ÉE]BITO)\s+[A-Z])",
        r"(?=RECIBO\s+[A-Z])",
        r"(?=Cod\.\s*\d+\s*[-–]?\s*FACTURA)",
    ]

    patron_completo = "|".join(marcadores)
    partes = re.split(patron_completo, texto_completo, flags=re.IGNORECASE)
    partes = [p.strip() for p in partes if p and p.strip()]

    if len(partes) > 1:
        return partes

    # Si no se detectaron múltiples facturas, tratar todo como una sola
    return [texto_completo]


def procesar_factura(texto: str) -> dict:
    """Procesa el texto de una factura y extrae los datos estructurados."""
    proveedor = extraer_proveedor(texto)
    nro_factura = extraer_nro_factura(texto)
    monto = extraer_monto(texto)
    nota = extraer_notas(texto)

    return {
        "proveedor": proveedor if proveedor else "N/D",
        "tipo_gastos": "",
        "detalle": "",
        "monto": monto if monto else "N/D",
        "nota": nota,
        "nro_factura": nro_factura if nro_factura else "N/D",
        "transferencia": "",
    }


def procesar_pdf(pdf_path: str) -> list[dict] | dict:
    """Procesa un archivo PDF y retorna los datos extraídos."""
    if not os.path.isfile(pdf_path):
        print(f"Error: No se encontró el archivo '{pdf_path}'", file=sys.stderr)
        sys.exit(1)

    paginas = extraer_texto(pdf_path)
    if not paginas:
        print(f"Error: No se pudo extraer texto de '{pdf_path}'", file=sys.stderr)
        sys.exit(1)

    facturas_texto = detectar_facturas_en_texto(paginas)
    resultados = [procesar_factura(texto) for texto in facturas_texto]

    if len(resultados) == 1:
        return resultados[0]
    return resultados


def main():
    parser = argparse.ArgumentParser(
        description="Procesa facturas argentinas en PDF y extrae datos en JSON."
    )
    parser.add_argument(
        "archivos",
        nargs="+",
        help="Ruta(s) al archivo(s) PDF de factura(s)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Archivo de salida JSON (por defecto: stdout)",
    )
    parser.add_argument(
        "--texto",
        action="store_true",
        help="Mostrar también el texto extraído del PDF (para depuración)",
    )

    args = parser.parse_args()

    todos_los_resultados = []

    for pdf_path in args.archivos:
        if args.texto:
            paginas = extraer_texto(pdf_path)
            print(f"\n{'='*60}", file=sys.stderr)
            print(f"Texto extraído de: {pdf_path}", file=sys.stderr)
            print(f"{'='*60}", file=sys.stderr)
            for i, pagina in enumerate(paginas, 1):
                print(f"\n--- Página {i} ---", file=sys.stderr)
                print(pagina, file=sys.stderr)

        resultado = procesar_pdf(pdf_path)
        if isinstance(resultado, list):
            todos_los_resultados.extend(resultado)
        else:
            todos_los_resultados.append(resultado)

    # Salida JSON
    if len(todos_los_resultados) == 1:
        salida = todos_los_resultados[0]
    else:
        salida = todos_los_resultados

    json_str = json.dumps(salida, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_str + "\n")
        print(f"Resultado guardado en '{args.output}'")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
