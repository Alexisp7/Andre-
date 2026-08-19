# -*- coding: utf-8 -*-
"""Estampa la marca de agua y cifra los apuntes.

Uso:  python3 proteger.py

Lee los PDF limpios de ./originales/ y escribe los protegidos en
sitio-andree/apuntes/<curso>/. Los originales nunca se tocan, así que
el script se puede volver a ejecutar sin que la marca se acumule.
"""
import io, math, os, secrets

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

BASE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(BASE, "originales")
LOGO = os.path.join(BASE, "marca-negro.png")

# A qué curso va cada archivo
DESTINOS = {
    "01-introduccion-psicofarmacologia.pdf": "psicofarmacologia",
    "02-psicofarmacologia.pdf":              "psicofarmacologia",
    "03-biologia-celular.pdf":               "psicofarmacologia",
    "04-biologia-molecular.pdf":             "psicofarmacologia",
    "05-farmacocinetica.pdf":                "psicofarmacologia",
    "06-farmacodinamia.pdf":                 "psicofarmacologia",
    "07-farmacolomica.pdf":                  "psicofarmacologia",
    "08-respuesta-clinica.pdf":              "psicofarmacologia",
    "09-desarrollo-medicamentos.pdf":        "psicofarmacologia",
    "10-bioequivalentes-biosimilares.pdf":   "psicofarmacologia",
    "11-factores-modificadores.pdf":         "psicofarmacologia",
    "12-neurotransmisores.pdf":              "psicofarmacologia",
    "13-ansioliticos.pdf":                   "psicofarmacologia",
    "14-antidepresivos.pdf":                 "psicofarmacologia",
    "15-antipsicoticos.pdf":                 "psicofarmacologia",
    "16-hipnoticos.pdf":                     "psicofarmacologia",
    "17-estabilizadores-humor.pdf":          "psicofarmacologia",
    "18-psicoestimulantes.pdf":              "psicofarmacologia",
    "19-toxicomanias.pdf":                   "psicofarmacologia",
    "20-etica.pdf":                          "psicofarmacologia",
}

AUTOR = "Dr. Andreé Salvatierra"
AVISO = "Apuntes de libre distribución con atribución"

# Intensidad de la marca. Subir = más visible.
OPACIDAD_DIAGONAL = 0.08
OPACIDAD_PIE      = 0.42


def capa(ancho, alto):
    """Genera la capa transparente que se superpone a una página."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(ancho, alto))
    logo = ImageReader(LOGO)
    prop = 0.276250          # alto/ancho del logotipo

    # ── Diagonal repetida: solo el logotipo "Neurona", sin el nombre
    #    debajo de cada copia. Cada copia se rota sobre su propio
    #    centro y solo se dibuja si cabe entera dentro de la página:
    #    así ninguna queda cortada por el borde (se vería "eurona" en
    #    vez de "Neurona" si se permitiera el recorte).
    ANGULO = 32
    rad = math.radians(ANGULO)
    cos_a, sin_a = abs(math.cos(rad)), abs(math.sin(rad))
    anchoLogo = ancho * 0.26
    altoLogo = anchoLogo * prop
    mitadAncho = (anchoLogo * cos_a + altoLogo * sin_a) / 2.0
    mitadAlto  = (anchoLogo * sin_a + altoLogo * cos_a) / 2.0

    x_ini, x_fin = mitadAncho, ancho - mitadAncho
    y_ini, y_fin = mitadAlto, alto - mitadAlto
    columnas, filas = 3, 3

    c.saveState()
    c.setFillAlpha(OPACIDAD_DIAGONAL)
    for i in range(columnas):
        gx = x_ini + (x_fin - x_ini) * (i / (columnas - 1))
        desplazo = anchoLogo * 0.16 if (i % 2) else -anchoLogo * 0.16
        for j in range(filas):
            gy = y_ini + (y_fin - y_ini) * (j / (filas - 1))
            cx_tile = gx + desplazo
            if cx_tile - mitadAncho < 0 or cx_tile + mitadAncho > ancho:
                cx_tile = gx
            c.saveState()
            c.translate(cx_tile, gy)
            c.rotate(ANGULO)
            c.drawImage(logo, -anchoLogo / 2.0, -altoLogo / 2.0,
                        width=anchoLogo, height=altoLogo, mask="auto")
            c.restoreState()
    c.restoreState()

    # ── Pie de página ───────────────────────────────────────────
    margen = ancho * 0.026
    altoPie = alto * 0.052

    c.saveState()
    c.setFillAlpha(0.055)
    c.setFillColorRGB(0, 0, 0)
    c.rect(0, 0, ancho, altoPie, stroke=0, fill=1)
    c.restoreState()

    c.saveState()
    c.setFillAlpha(0.30)
    c.setStrokeAlpha(0.30)
    c.setLineWidth(0.6)
    c.line(margen, altoPie, ancho - margen, altoPie)
    c.restoreState()

    # Solo el logotipo a la izquierda: el nombre ya no se repite aquí
    # porque el propio autor ya lleva su firma en el lado derecho de
    # sus diapositivas.
    c.saveState()
    c.setFillAlpha(OPACIDAD_PIE)
    anchoLogoPie = ancho * 0.105
    c.drawImage(logo, margen, altoPie * 0.30,
                width=anchoLogoPie, height=anchoLogoPie * prop, mask="auto")
    c.restoreState()

    c.saveState()
    c.setFillAlpha(1.0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", ancho * 0.0105)
    c.drawCentredString(ancho / 2.0, altoPie * 0.38, AVISO)
    c.restoreState()

    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def proteger(origen, destino):
    lector = PdfReader(origen)
    escritor = PdfWriter()
    cache = {}

    for pagina in lector.pages:
        caja = pagina.mediabox
        clave = (round(float(caja.width), 1), round(float(caja.height), 1))
        if clave not in cache:
            cache[clave] = capa(*clave)
        pagina.merge_page(cache[clave])
        escritor.add_page(pagina)

    escritor.add_metadata({
        "/Title": os.path.basename(origen),
        "/Author": AUTOR,
        "/Creator": "Neurona — biblioteca de apuntes",
        "/Subject": "Material de clase. Uso educativo; prohibida su distribución.",
    })

    # Se abre sin contraseña, pero sin permiso de imprimir, copiar ni modificar.
    # Partimos de todos los permisos y quitamos los que nos interesan, para no
    # tocar los bits reservados que exige la especificación del formato.
    from pypdf.constants import UserAccessPermissions as P
    DENEGAR = (P.PRINT | P.MODIFY | P.EXTRACT | P.ADD_OR_MODIFY |
               P.FILL_FORM_FIELDS | P.EXTRACT_TEXT_AND_GRAPHICS |
               P.ASSEMBLE_DOC | P.PRINT_TO_REPRESENTATION)
    escritor.encrypt(
        user_password="",
        owner_password=secrets.token_urlsafe(24),
        permissions_flag=P.all() & ~DENEGAR,
        algorithm="AES-256",
    )

    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "wb") as f:
        escritor.write(f)
    return len(lector.pages)


if __name__ == "__main__":
    print("Protegiendo los apuntes…")
    total = 0
    for archivo, curso in sorted(DESTINOS.items()):
        origen = os.path.join(ORIG, archivo)
        if not os.path.exists(origen):
            print("  ! falta %s en originales/" % archivo)
            continue
        destino = os.path.join(BASE, "sitio-andree", "apuntes", curso, archivo)
        n = proteger(origen, destino)
        kb = os.path.getsize(destino) / 1024
        print("  ✓ %-42s %3d pág · %5.0f KB" % (archivo, n, kb))
        total += n
    print("Listo. %d páginas marcadas y cifradas." % total)
