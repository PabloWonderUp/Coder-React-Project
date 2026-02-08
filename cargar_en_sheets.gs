/**
 * Google Apps Script para cargar facturas desde JSON a Google Sheets.
 *
 * INSTRUCCIONES:
 * 1. Abrí tu Google Spreadsheet
 * 2. Menú: Extensiones > Apps Script
 * 3. Borrá todo el código que aparece y pegá este archivo completo
 * 4. Guardá (Ctrl+S) y cerrá el editor
 * 5. Recargá la hoja: va a aparecer un nuevo menú "Facturas"
 * 6. Usá "Facturas > Cargar JSON" para pegar el JSON y cargar los datos
 */

var COLUMNAS = [
  "Proveedor",
  "Tipo de Gastos",
  "Detalle",
  "Monto",
  "Nota",
  "Nro. Factura",
  "Transferencia"
];

var CAMPOS = [
  "proveedor",
  "tipo_gastos",
  "detalle",
  "monto",
  "nota",
  "nro_factura",
  "transferencia"
];

/**
 * Agrega el menú personalizado al abrir la hoja.
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("Facturas")
    .addItem("Cargar JSON", "mostrarDialogo")
    .addItem("Crear encabezados", "crearEncabezados")
    .addToUi();
}

/**
 * Crea los encabezados en la primera fila de la hoja activa.
 */
function crearEncabezados() {
  var hoja = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var primeraFila = hoja.getRange(1, 1, 1, COLUMNAS.length).getValues()[0];
  var estaVacia = primeraFila.every(function(celda) { return celda === ""; });

  if (!estaVacia) {
    var ui = SpreadsheetApp.getUi();
    var respuesta = ui.alert(
      "La primera fila ya tiene datos. ¿Querés reemplazarla con los encabezados?",
      ui.ButtonSet.YES_NO
    );
    if (respuesta !== ui.Button.YES) return;
  }

  hoja.getRange(1, 1, 1, COLUMNAS.length).setValues([COLUMNAS]);
  hoja.getRange(1, 1, 1, COLUMNAS.length)
    .setFontWeight("bold")
    .setBackground("#4a86c8")
    .setFontColor("#ffffff");

  SpreadsheetApp.getUi().alert("Encabezados creados correctamente.");
}

/**
 * Muestra el diálogo para pegar el JSON.
 */
function mostrarDialogo() {
  var html = HtmlService
    .createHtmlOutput(
      '<style>' +
      '  body { font-family: Arial, sans-serif; padding: 10px; }' +
      '  textarea { width: 100%; height: 200px; font-family: monospace; font-size: 12px; }' +
      '  button { margin-top: 10px; padding: 8px 20px; background: #4a86c8; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }' +
      '  button:hover { background: #3a76b8; }' +
      '  .info { color: #666; font-size: 12px; margin-bottom: 8px; }' +
      '</style>' +
      '<p class="info">Pegá acá el JSON generado por <b>procesar_facturas.py</b>:</p>' +
      '<textarea id="json-input" placeholder=\'{"proveedor": "...", "monto": "..."}\n\no\n\n[{"proveedor": "..."}, {"proveedor": "..."}]\'></textarea>' +
      '<br>' +
      '<button onclick="enviar()">Cargar en la hoja</button>' +
      '<script>' +
      '  function enviar() {' +
      '    var json = document.getElementById("json-input").value;' +
      '    if (!json.trim()) { alert("Pegá el JSON primero"); return; }' +
      '    google.script.run' +
      '      .withSuccessHandler(function(msg) { alert(msg); google.script.host.close(); })' +
      '      .withFailureHandler(function(err) { alert("Error: " + err.message); })' +
      '      .procesarJSON(json);' +
      '  }' +
      '</script>'
    )
    .setWidth(500)
    .setHeight(340);

  SpreadsheetApp.getUi().showModalDialog(html, "Cargar facturas desde JSON");
}

/**
 * Procesa el JSON recibido y agrega las filas a la hoja.
 * @param {string} jsonStr - JSON con una factura o un array de facturas.
 * @return {string} Mensaje de resultado.
 */
function procesarJSON(jsonStr) {
  var datos;
  try {
    datos = JSON.parse(jsonStr);
  } catch (e) {
    throw new Error("El JSON no es válido. Revisá que esté bien copiado.");
  }

  // Normalizar: si es un objeto, meterlo en un array
  if (!Array.isArray(datos)) {
    datos = [datos];
  }

  var hoja = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // Verificar si hay encabezados, si no crearlos
  var primeraFila = hoja.getRange(1, 1, 1, COLUMNAS.length).getValues()[0];
  var estaVacia = primeraFila.every(function(celda) { return celda === ""; });
  if (estaVacia) {
    hoja.getRange(1, 1, 1, COLUMNAS.length).setValues([COLUMNAS]);
    hoja.getRange(1, 1, 1, COLUMNAS.length)
      .setFontWeight("bold")
      .setBackground("#4a86c8")
      .setFontColor("#ffffff");
  }

  // Construir filas
  var filas = datos.map(function(factura) {
    return CAMPOS.map(function(campo) {
      return factura[campo] !== undefined ? String(factura[campo]) : "";
    });
  });

  // Encontrar la siguiente fila vacía
  var ultimaFila = hoja.getLastRow();
  var filaInicio = ultimaFila + 1;

  // Insertar todas las filas de una vez
  hoja.getRange(filaInicio, 1, filas.length, COLUMNAS.length).setValues(filas);

  return filas.length + " factura(s) cargada(s) correctamente.";
}
