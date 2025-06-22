"""
Controlador para la gestión de facturas electrónicas y generación de PDFs en la aplicación.

Términos clave:
- Factura: Comprobante que documenta una transacción de venta de bienes o servicios.
- PDF: Formato de archivo portátil para representar documentos, ideal para facturas.
- reportlab: Librería de Python para generar PDFs de forma programática.
- Controller: Se encarga de la lógica asociada a la generación y almacenamiento de facturas.
"""

from flask import jsonify, request
import json, os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_from_directory
from controllers.caja_controller import cargar_caja, guardar_caja

FACTURAS_FILE = "data/facturas.json"
VENTAS_FILE = "data/ventas.json"
PDF_DIR = "data/facturas_pdf"


def cargar_facturas():
    """
    Carga todas las facturas desde el archivo JSON.
    Si el archivo no existe, lo crea con una lista vacía.

    Returns:
        list: Lista de facturas almacenadas.
    """
    if not os.path.exists(FACTURAS_FILE):
        os.makedirs(os.path.dirname(FACTURAS_FILE), exist_ok=True)
        with open(FACTURAS_FILE, "w") as f:
            json.dump([], f)
    with open(FACTURAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_facturas(facturas):
    """
    Guarda la lista de facturas en el archivo JSON.

    Args:
        facturas (list): Lista de facturas a guardar.
    """
    with open(FACTURAS_FILE, "w", encoding="utf-8") as f:
        json.dump(facturas, f, indent=2, ensure_ascii=False)


def cargar_ventas():
    """
    Carga todas las ventas desde el archivo JSON.
    Si el archivo no existe, retorna una lista vacía.

    Returns:
        list: Lista de ventas almacenadas.
    """
    if not os.path.exists(VENTAS_FILE):
        return []
    with open(VENTAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generar_id_factura(facturas):
    """
    Genera un ID único para la nueva factura basado en el año, mes y cantidad de facturas
    existentes en el mes actual. Ejemplo: FAC-2025-06-001.

    Args:
        facturas (list): Lista de facturas existentes.

    Returns:
        str: ID generado para la factura.
    """
    ahora = datetime.now()
    año_mes = ahora.strftime("%Y-%m")
    correlativos = [f for f in facturas if f["id"].startswith(f"FAC-{año_mes}")]
    numero = len(correlativos) + 1
    return f"FAC-{año_mes}-{str(numero).zfill(3)}"


def generar_pdf_factura(factura):
    """
    Genera un archivo PDF con los datos de la factura recibida utilizando la librería reportlab.

    Args:
        factura (dict): Datos de la factura (cliente, fecha, items, total, etc.).

    Returns:
        str: Ruta del archivo PDF generado.
    """
    os.makedirs(PDF_DIR, exist_ok=True)
    pdf_path = os.path.join(PDF_DIR, f"{factura['id']}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # --------- Estilo general ----------
    margen = 40
    y = height - margen

    # --------- Encabezado: Logo y empresa ----------
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#10B981"))  # verde suave
    c.drawString(margen, y, "Caja Plus")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    y -= 30

    # --------- Info factura ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margen, y, f"Factura: {factura['id']}")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(margen, y, f"Fecha: {factura['fecha']}")
    y -= 15
    c.drawString(margen, y, f"Cliente: {factura['cliente']}")
    y -= 30

    # --------- Tabla de items ----------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, y, "Detalle de productos:")
    y -= 20

    # Encabezado tabla
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.grey)
    c.rect(margen, y - 4, width - 2 * margen, 20, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.drawString(margen + 10, y + 2, "Producto")
    c.drawString(width / 2 - 40, y + 2, "Cantidad")
    c.drawRightString(width - margen - 10, y + 2, "Precio Unitario")
    y -= 22

    # Filas
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    for item in factura.get("items", []):
        if y < 80:
            c.showPage()
            y = height - margen

        nombre = item.get("nombre", "Producto")
        cantidad = item.get("cantidad", 1)
        precio = item.get("precio_unitario", 0)

        c.drawString(margen + 10, y, nombre)
        c.drawString(width / 2 - 40, y, str(cantidad))
        c.drawRightString(width - margen - 10, y, f"${precio:.2f}")
        y -= 18

    # --------- Total ----------
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - margen - 10, y, f"Total: ${factura['total']:.2f}")

    # --------- Footer ----------
    y -= 40
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, y, "Gracias por confiar en Caja Plus. www.cajaplus.com")

    c.save()
    return pdf_path


def generar_factura():
    """
    Endpoint para generar una nueva factura a partir de una venta existente.
    Recibe los datos por POST (venta_id y cliente), busca la venta, crea una nueva factura,
    guarda el PDF, actualiza la caja y retorna los datos de la factura.

    Returns:
        Response: JSON con los datos de la factura y ruta del PDF.
    """
    data = request.get_json()
    print(data)
    venta_id = data.get("venta_id")
    cliente = data.get("cliente")

    if not venta_id or not cliente:
        return jsonify({"error": "Faltan datos requeridos (venta_id o cliente)"}), 400

    ventas = cargar_ventas()
    venta = next((v for v in ventas if v.get("id") == venta_id), None)

    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404

    facturas = cargar_facturas()
    nuevo_id = generar_id_factura(facturas)

    nueva_factura = {
        "id": nuevo_id,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cliente": cliente,
        "venta_id": venta_id,
        "precio_unitario": venta.get("precio_unitario", 0),
        "items": venta.get("items", []),
        "total": venta.get("total", 0),
    }

    facturas.append(nueva_factura)
    guardar_facturas(facturas)
    pdf_path = generar_pdf_factura(nueva_factura)

    # Asociar la factura al movimiento correspondiente en la caja
    caja = cargar_caja()
    for movimiento in caja["movimientos"]:
        if movimiento.get("id") == venta_id:
            movimiento["factura_id"] = nuevo_id
            break
    guardar_caja(caja)

    return (
        jsonify(
            {
                "message": "Factura generada correctamente",
                "factura": nueva_factura,
                "pdf": pdf_path,
            }
        ),
        201,
    )


def descargar_pdf(nombre_archivo):
    """
    Endpoint para descargar un archivo PDF de factura desde el directorio correspondiente.

    Args:
        nombre_archivo (str): Nombre del archivo PDF a descargar.

    Returns:
        Response: Envío del archivo PDF como respuesta HTTP.
    """
    return send_from_directory(PDF_DIR, nombre_archivo, as_attachment=False)
