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

from pyhanko.sign import signers
from pyhanko.sign.fields import SigFieldSpec, append_signature_field
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

BASE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(BASE, "originales")
LOGO = os.path.join(BASE, "marca-negro.png")

# Certificado propio (autofirmado) usado para la firma digital que se
# estampa en cada PDF protegido. No es un certificado de una autoridad
# reconocida: los lectores de PDF lo mostrarán como "firma no verificada",
# pero la firma en sí es criptográficamente real y demuestra que el
# archivo salió de Neurona y no fue alterado después.
#
# La clave privada NUNCA se sube al repositorio (ver .gitignore): este
# script la genera sola, en el equipo donde se ejecuta, la primera vez
# que hace falta. Si se genera de nuevo en otro equipo, los PDF firmados
# ahí quedan con una identidad de firma distinta a los anteriores; eso
# no afecta la lectura ni la marca de agua, solo el certificado exacto
# detrás de la firma.
FIRMA_DIR = os.path.join(BASE, "firma")
FIRMA_P12 = os.path.join(FIRMA_DIR, "neurona_firma.p12")
FIRMA_CLAVE = b"neurona-firma-local"
FIRMA_NOMBRE = "Neurona — Dr. Andreé Salvatierra"


def asegurar_certificado():
    """Crea el certificado autofirmado local si todavía no existe."""
    if os.path.exists(FIRMA_P12):
        return
    import datetime
    from cryptography import x509
    from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives.serialization import pkcs12

    clave = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    nombre = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, FIRMA_NOMBRE),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Neurona"),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, "4andree4@gmail.com"),
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PE"),
    ])
    ahora = datetime.datetime.utcnow()
    certificado = (
        x509.CertificateBuilder()
        .subject_name(nombre).issuer_name(nombre).public_key(clave.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(ahora - datetime.timedelta(days=1))
        .not_valid_after(ahora + datetime.timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(x509.KeyUsage(
            digital_signature=True, content_commitment=True, key_encipherment=False,
            data_encipherment=False, key_agreement=False, key_cert_sign=False,
            crl_sign=False, encipher_only=False, decipher_only=False), critical=True)
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.EMAIL_PROTECTION]), critical=False)
        .sign(clave, hashes.SHA256())
    )
    os.makedirs(FIRMA_DIR, exist_ok=True)
    with open(FIRMA_P12, "wb") as f:
        f.write(pkcs12.serialize_key_and_certificates(
            name=b"neurona", key=clave, cert=certificado, cas=None,
            encryption_algorithm=serialization.BestAvailableEncryption(FIRMA_CLAVE),
        ))

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

    # ── Diagonal repetida: el logotipo "Neurona" con "Salvatierra"
    #    debajo, en cada copia. Cada copia (logo + nombre) se rota
    #    sobre su propio centro y solo se dibuja si cabe entera dentro
    #    de la página: así ninguna queda cortada por el borde.
    ANGULO = 32
    rad = math.radians(ANGULO)
    NOMBRE = "Salvatierra"
    FUENTE_NOMBRE = "Helvetica"
    anchoLogo = ancho * 0.26
    altoLogo = anchoLogo * prop
    tamNombre = anchoLogo * 0.072
    espacio = altoLogo * 0.24
    anchoNombre = c.stringWidth(NOMBRE, FUENTE_NOMBRE, tamNombre)

    # Caja local del contenido (logo arriba, nombre debajo), medida
    # desde el punto de rotación (el centro vertical del logo).
    mitadAnchoCaja = max(anchoLogo, anchoNombre) / 2.0
    yArriba = altoLogo / 2.0
    yAbajo = -(altoLogo / 2.0 + espacio + tamNombre)
    esquinasLocales = ((-mitadAnchoCaja, yArriba), (mitadAnchoCaja, yArriba),
                        (-mitadAnchoCaja, yAbajo), (mitadAnchoCaja, yAbajo))
    mitadAncho = max(abs(lx * math.cos(rad) - ly * math.sin(rad)) for lx, ly in esquinasLocales)
    mitadAlto  = max(abs(lx * math.sin(rad) + ly * math.cos(rad)) for lx, ly in esquinasLocales)

    x_ini, x_fin = mitadAncho, ancho - mitadAncho
    y_ini, y_fin = mitadAlto, alto - mitadAlto
    columnas, filas = 3, 3

    c.saveState()
    c.setFillAlpha(OPACIDAD_DIAGONAL)
    c.setFont(FUENTE_NOMBRE, tamNombre)
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
            c.drawCentredString(0, -(altoLogo / 2.0 + espacio + tamNombre * 0.72), NOMBRE)
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

    firmar(destino)
    return len(lector.pages)


def firmar(ruta):
    """Añade la firma digital de Neurona al PDF ya cifrado, sin tocar
    el cifrado ni los permisos existentes (actualización incremental)."""
    asegurar_certificado()
    signer = signers.SimpleSigner.load_pkcs12(FIRMA_P12, passphrase=FIRMA_CLAVE)
    temporal = ruta + ".firmado"
    with open(ruta, "rb") as entrada:
        escritor = IncrementalPdfFileWriter(entrada)
        escritor.encrypt("")  # contraseña de usuario (vacía, como al cifrar)
        append_signature_field(escritor, SigFieldSpec(sig_field_name="FirmaNeurona"))
        metadatos = signers.PdfSignatureMetadata(
            field_name="FirmaNeurona",
            reason="Documento oficial de Neurona",
            location="Perú",
            name=FIRMA_NOMBRE,
        )
        with open(temporal, "wb") as salida:
            signers.sign_pdf(escritor, metadatos, signer=signer, output=salida)
    os.replace(temporal, ruta)


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
