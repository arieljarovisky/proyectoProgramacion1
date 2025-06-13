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
    if not os.path.exists(FACTURAS_FILE):
        os.makedirs(os.path.dirname(FACTURAS_FILE), exist_ok=True)
        with open(FACTURAS_FILE, "w") as f:
            json.dump([], f)
    with open(FACTURAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_facturas(facturas):
    with open(FACTURAS_FILE, "w", encoding="utf-8") as f:
        json.dump(facturas, f, indent=2, ensure_ascii=False)


def cargar_ventas():
    if not os.path.exists(VENTAS_FILE):
        return []
    with open(VENTAS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generar_id_factura(facturas):
    ahora = datetime.now()
    año_mes = ahora.strftime("%Y-%m")
    correlativos = [f for f in facturas if f["id"].startswith(f"FAC-{año_mes}")]
    numero = len(correlativos) + 1
    return f"FAC-{año_mes}-{str(numero).zfill(3)}"


def generar_pdf_factura(factura):
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
    return send_from_directory(PDF_DIR, nombre_archivo, as_attachment=False)
