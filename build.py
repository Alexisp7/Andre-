# -*- coding: utf-8 -*-
"""Generador del sitio de Andreé Salvatierra Baldeón.

Uso:  python3 build.py
Regenera index.html, las tres páginas de curso y apuntes.html a partir
de los datos de CURSOS. Editar aquí es más seguro que editar el HTML.
"""
import os, json

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitio-andree")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"/>\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&amp;family=Inter:wght@300;400;500;600&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>')

NEURON_SVG = '''<span class="logo-neuron">
          <svg viewBox="0 0 32 32" fill="none" stroke="#C8A96E" stroke-width="1.2" stroke-linecap="round">
            <circle cx="13" cy="15" r="4.5"/>
            <circle cx="13" cy="15" r="1.6" fill="#C8A96E" stroke="none"/>
            <path d="M17.5 15h6.5M24 15l3.5-3M24 15l3.5 3"/>
            <path d="M9.4 11.8 5.5 7.5M8.5 15H3.5M9.4 18.2 5.5 22.5M13 19.5v5M13 10.5v-5"/>
            <circle cx="27.5" cy="12" r="1.2" fill="#C8A96E" stroke="none"/>
            <circle cx="27.5" cy="18" r="1.2" fill="#C8A96E" stroke="none"/>
          </svg>
        </span>'''

PLATE = """\
        <svg viewBox="0 0 560 440" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#C8A96E" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">

          <defs>
            <path id="cerebro" d="M44 186
                     C40 146, 62 112, 98 96
                     C132 80, 172 86, 196 106
                     C220 100, 244 114, 250 140
                     C256 164, 246 186, 228 196
                     C230 210, 222 222, 208 226
                     C202 238, 186 244, 172 240
                     C156 246, 136 244, 124 234
                     C96 234, 72 222, 62 206
                     C50 202, 42 194, 44 186 Z"/>
            <clipPath id="clipCerebro"><use href="#cerebro"/></clipPath>
          </defs>

          <g class="plate-part plate-brain"><g clip-path="url(#clipCerebro)" opacity="0.8">
            <path d="M104 92 C114 116, 108 140, 90 152 C76 162, 62 161, 52 154"/>
            <path d="M140 82 C150 110, 144 136, 124 150 C106 162, 86 162, 74 153"/>
            <path d="M176 86 C184 114, 174 142, 152 154 C132 165, 112 164, 100 156"/>
            <path d="M204 106 C210 132, 200 158, 178 168 C160 177, 142 176, 132 168"/>
            <path d="M230 126 C236 150, 226 170, 208 178 C194 185, 180 184, 172 178"/>
            <path d="M250 152 C250 172, 238 186, 222 190"/>
            <path d="M70 176 C84 168, 102 170, 112 180"/>
            <path d="M88 200 C104 190, 124 191, 136 202"/>
            <path d="M128 220 C142 211, 160 211, 172 220"/>
            <path d="M56 132 C68 124, 82 124, 92 130"/>
          </g>

          <g clip-path="url(#clipCerebro)">
            <path d="M88 182 C102 152, 140 138, 176 147 C198 152, 212 165, 216 180" stroke-width="1.4"/>
            <path d="M97 187 C110 163, 142 151, 174 158 C192 162, 204 172, 208 184" stroke-width="0.9" opacity="0.7"/>
            <path d="M118 196 C132 182, 158 178, 178 186" stroke-width="0.8" opacity="0.55"/>
          </g>

          <use href="#cerebro" stroke-width="1.3"/>

          <g opacity="0.95">
            <path d="M186 224
                     C204 214, 232 218, 244 234
                     C256 250, 250 272, 230 278
                     C212 283, 194 275, 188 260
                     C184 250, 183 236, 186 224 Z" stroke-width="1.2"/>
            <path d="M192 232 C210 224, 232 230, 241 244" stroke-width="0.75" opacity="0.75"/>
            <path d="M189 244 C206 235, 228 241, 239 256" stroke-width="0.75" opacity="0.75"/>
            <path d="M188 256 C204 247, 224 252, 234 266" stroke-width="0.75" opacity="0.75"/>
            <path d="M191 266 C204 259, 218 262, 226 272" stroke-width="0.75" opacity="0.75"/>
          </g>

          <g stroke-width="1.25">
            <path d="M148 224
                     C154 236, 158 246, 162 254
                     C168 266, 172 280, 170 296"/>
            <path d="M182 220
                     C184 234, 186 244, 188 252
                     C192 266, 192 282, 188 298"/>
            <path d="M170 296 C176 300, 182 300, 188 298" stroke-width="1.1"/>
          </g>
          <g stroke-width="0.75" opacity="0.7">
            <path d="M158 248 C166 253, 176 254, 186 250"/>
            <path d="M166 272 C173 277, 181 277, 189 274"/>
          </g>

          </g>
          <g class="plate-part plate-link">
          <circle cx="150" cy="98" r="4.5" stroke-width="1.3"/>
          <path d="M154 95 L310 78" stroke-width="0.6" opacity="0.5"/>
          <path d="M154 102 L310 150" stroke-width="0.6" opacity="0.5"/>

          </g>
          <g class="plate-part plate-zoom1">
            <circle cx="372" cy="114" r="72" stroke-width="1.3"/>
            <clipPath id="c1"><circle cx="372" cy="114" r="70"/></clipPath>
            <g clip-path="url(#c1)">
              <g stroke-width="0.7" opacity="0.4">
                <path d="M298 58 H448"/><path d="M298 76 H448"/><path d="M298 98 H448"/>
                <path d="M298 124 H448"/><path d="M298 148 H448"/><path d="M298 168 H448"/>
              </g>
              <g stroke-width="0.95">
                <circle cx="322" cy="68" r="2.4"/><circle cx="350" cy="66" r="2.4"/>
                <circle cx="384" cy="69" r="2.4"/><circle cx="416" cy="67" r="2.4"/>

                <g><circle cx="332" cy="88" r="3.4"/><path d="M332 84 v-6 M328 85 l-5 -5 M336 85 l5 -5 M332 92 v7"/></g>
                <g><circle cx="368" cy="86" r="3.4"/><path d="M368 82 v-6 M364 83 l-5 -5 M372 83 l5 -5 M368 90 v7"/></g>
                <g><circle cx="404" cy="89" r="3.4"/><path d="M404 85 v-6 M400 86 l-5 -5 M408 86 l5 -5 M404 93 v7"/></g>

                <g><path d="M316 116 l6 -10 l6 10 Z" stroke-width="1.1"/><path d="M322 106 v-9 M322 97 l-5 -6 M322 97 l5 -6 M316 116 l-7 6 M328 116 l7 6 M322 116 v13"/></g>
                <g><path d="M356 118 l6 -10 l6 10 Z" stroke-width="1.1"/><path d="M362 108 v-9 M362 99 l-5 -6 M362 99 l5 -6 M356 118 l-7 6 M368 118 l7 6 M362 118 v13"/></g>
                <g><path d="M396 115 l6 -10 l6 10 Z" stroke-width="1.1"/><path d="M402 105 v-9 M402 96 l-5 -6 M402 96 l5 -6 M396 115 l-7 6 M408 115 l7 6 M402 115 v13"/></g>
                <g><path d="M430 120 l6 -10 l6 10 Z" stroke-width="1.1"/><path d="M436 110 v-9 M436 101 l-5 -6 M436 101 l5 -6 M430 120 l-7 6 M442 120 l7 6 M436 120 v11"/></g>

                <g><circle cx="336" cy="140" r="3"/><path d="M336 137 v-6 M336 143 v7 M333 138 l-6 -4 M339 138 l6 -4"/></g>
                <g><circle cx="376" cy="142" r="3"/><path d="M376 139 v-6 M376 145 v7 M373 140 l-6 -4 M379 140 l6 -4"/></g>
                <g><circle cx="414" cy="139" r="3"/><path d="M414 136 v-6 M414 142 v7 M411 137 l-6 -4 M417 137 l6 -4"/></g>

                <circle cx="330" cy="160" r="2.2"/><circle cx="362" cy="162" r="2.2"/>
                <circle cx="396" cy="159" r="2.2"/><circle cx="426" cy="161" r="2.2"/>
              </g>
            </g>
          </g>

          <g class="plate-part plate-link2">
            <path d="M330 172 L338 262" stroke-width="0.6" opacity="0.5"/>
            <path d="M428 158 L510 262" stroke-width="0.6" opacity="0.5"/>
          </g>

          <g class="plate-part plate-zoom2">
            <circle cx="424" cy="314" r="100" stroke-width="1.3"/>
            <clipPath id="c2"><circle cx="424" cy="314" r="98"/></clipPath>
            <g clip-path="url(#c2)">
              <g stroke-width="1.15">
                <path d="M424 286 L424 258"/>
                <path d="M424 258 L404 238 M424 258 L446 236"/>
                <path d="M404 238 L392 226 M404 238 L398 222"/>
                <path d="M446 236 L458 224 M446 236 L442 220"/>
                <path d="M392 226 L384 218 M398 222 L394 212"/>
                <path d="M458 224 L466 216 M442 220 L440 210"/>

                <path d="M410 304 L386 314 M386 314 L366 322 M386 314 L374 328"/>
                <path d="M410 308 L390 330 M390 330 L378 344"/>
                <path d="M438 304 L462 314 M462 314 L482 322 M462 314 L474 328"/>
                <path d="M438 308 L458 330 M458 330 L470 344"/>
              </g>

              <path d="M424 284 L408 306 L440 306 Z" stroke-width="1.5"/>
              <circle cx="424" cy="298" r="5.5" stroke-width="1"/>
              <circle cx="424" cy="298" r="2" fill="#C8A96E" stroke="none"/>

              <path d="M424 306 L424 318" stroke-width="1.2"/>
              <g stroke-width="1.05">
                <rect x="418" y="317" width="12" height="19" rx="6"/>
                <rect x="418" y="341" width="12" height="19" rx="6"/>
                <rect x="418" y="365" width="12" height="19" rx="6"/>
                <path d="M424 336 v5 M424 360 v5 M424 384 v4"/>
              </g>
              <path d="M424 388 L406 400 M424 388 L424 404 M424 388 L442 400" stroke-width="1.1"/>
              <g stroke-width="0.9">
                <circle cx="404" cy="402" r="2.6"/><circle cx="424" cy="407" r="2.6"/><circle cx="444" cy="402" r="2.6"/>
                <circle cx="383" cy="217" r="2" opacity="0.85"/><circle cx="467" cy="215" r="2" opacity="0.85"/>
                <circle cx="393" cy="211" r="2" opacity="0.85"/><circle cx="439" cy="209" r="2" opacity="0.85"/>
              </g>
            </g>
          </g>
        </svg>
"""

NAV_ITEMS = [("index.html", "Inicio"), ("farmacologia.html", "Farmacología"),
             ("neuroanatomia.html", "Neuroanatomía"),
             ("neurofisiologia.html", "Neurofisiología"), ("apuntes.html", "Apuntes")]


def header(active):
    links = []
    for href, label in NAV_ITEMS:
        cls = ' class="active"' if href == active else ''
        links.append('<a href="%s"%s>%s</a>' % (href, cls, label))
    nav = '<span class="nav-sep">|</span>'.join(links)
    return '''  <header class="header">
    <div class="header-greek-bar"></div>
    <div class="header-inner">
      <div class="logo-group">
        %s
        <div class="site-logo">
          <span class="site-logo-name">Dr. Andreé Salvatierra</span>
          <span class="site-logo-subtitle">Neurociencia · Farmacología</span>
        </div>
      </div>
      <nav class="main-nav">%s</nav>
    </div>
    <div class="header-border"></div>
  </header>''' % (NEURON_SVG, nav)


FOOTER = '''  <footer class="footer-wrap" id="contacto">
    <div class="footer">
      <div class="footer-top">
        <div class="footer-logo-group">
          <span class="footer-phi">Ψ</span>
          <div>
            <div class="footer-logo-name">Dr. Andreé Salvatierra Baldeón</div>
            <div class="footer-logo-sub">Neurociencia · Farmacología</div>
          </div>
        </div>
        <div class="footer-links-col">
          <div class="footer-col">
            <div class="footer-col-title">Cursos</div>
            <a href="farmacologia.html">Farmacología</a>
            <a href="neuroanatomia.html">Neuroanatomía</a>
            <a href="neurofisiologia.html">Neurofisiología</a>
          </div>
          <div class="footer-col">
            <div class="footer-col-title">Biblioteca</div>
            <a href="apuntes.html">Catálogo de apuntes</a>
            <a href="index.html#sobre">Sobre el autor</a>
          </div>
          <div class="footer-col">
            <div class="footer-col-title">Contacto</div>
            <a href="mailto:correo@ejemplo.com">correo@ejemplo.com</a>
            <a href="#">ORCID</a>
            <a href="#">Google Scholar</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span class="footer-copy">© 2026 Dr. Andreé Salvatierra Baldeón · Apuntes de libre distribución con atribución</span>
      </div>
    </div>
  </footer>'''


def page(title, desc, active, body, body_class=""):
    return '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>%s</title>
  <meta name="description" content="%s"/>
  %s
  <link rel="stylesheet" href="css/theme.css"/>
</head>
<body%s>

%s

%s

%s

</body>
</html>
''' % (title, desc, FONTS, (' class="%s"' % body_class) if body_class else '',
       header(active), body, FOOTER)


# ══════════════════════════════════════════════════════════════
#  DATOS DE LOS CURSOS
#  Cada tema es (código, título, archivo_pdf o None, nº de páginas)
# ══════════════════════════════════════════════════════════════

CURSOS = [
{
 "slug": "farmacologia",
 "nombre": "Farmacología",
 "titulo_html": 'Farma<em>cología</em>',
 "eyebrow": "Curso 01 · Ciencias básicas",
 "ornamento": "Rx",
 "icono": '<path d="M10.5 3.5 3.9 10.1a4.7 4.7 0 0 0 6.6 6.6l6.6-6.6a4.7 4.7 0 0 0-6.6-6.6Z"/><path d="M7.2 6.8 14 13.6"/><circle cx="18.5" cy="18.5" r="3.5"/><path d="M16.5 18.5h4M18.5 16.5v4"/>',
 "tag": "Curso 01 · Ciencias básicas",
 "resumen": "De las bases celulares y moleculares a la farmacocinética, la farmacodinamia y la psicofarmacología clínica.",
 "sub": "De las bases celulares y moleculares del organismo a la farmacocinética, la farmacodinamia y la psicofarmacología clínica.",
 "ficha": [("Nivel", "Pregrado · Ciencias básicas"),
           ("Unidades", "4"),
           ("Apuntes", "6 publicados"),
           ("Páginas", "250 en total"),
           ("Formato", "Diapositivas en PDF"),
           ("Autor", "Dr. Andreé Salvatierra")],
 "bibliografia": [
   "Goodman &amp; Gilman. <em>Las bases farmacológicas de la terapéutica</em>.",
   "Katzung, B. <em>Farmacología básica y clínica</em>.",
   "Rang &amp; Dale. <em>Farmacología</em>.",
   "Stahl, S. <em>Psicofarmacología esencial</em>."],
 "intro": "El curso abre por donde importa: qué es la psicofarmacología y sobre qué actúa. Después baja a las bases celulares y moleculares, y solo entonces entra a los dos pilares clásicos — qué le hace el organismo al fármaco (PK) y qué le hace el fármaco al organismo (PD).",
 "unidades": [
   {"num": "I", "nombre": "Introducción a la psicofarmacología", "horas": "20 pág.", "temas": [
     ("PSF-01", "Introducción a la psicofarmacología", "01-introduccion-psicofarmacologia.pdf", 9),
     ("PSF-02", "Psicofarmacología y neurotransmisión química", "02-psicofarmacologia.pdf", 11)]},
   {"num": "II", "nombre": "Bases celulares y moleculares", "horas": "94 pág.", "temas": [
     ("BIO-01", "Biología celular", "03-biologia-celular.pdf", 53),
     ("BIO-02", "Biología molecular", "04-biologia-molecular.pdf", 41)]},
   {"num": "III", "nombre": "Farmacocinética", "horas": "93 pág.", "temas": [
     ("PK-01", "Farmacocinética: absorción, distribución, metabolismo y excreción", "05-farmacocinetica.pdf", 93)]},
   {"num": "IV", "nombre": "Farmacodinamia", "horas": "43 pág.", "temas": [
     ("PD-01", "Farmacodinamia: ligando, receptor y efecto farmacológico", "06-farmacodinamia.pdf", 43)]}],
},
{
 "slug": "neuroanatomia",
 "nombre": "Neuroanatomía",
 "titulo_html": 'Neuro<em>anatomía</em>',
 "eyebrow": "Curso 02 · Morfología",
 "ornamento": "Ω",
 "icono": '<path d="M8.5 3.2a3.4 3.4 0 0 0-3.2 4.2A3.3 3.3 0 0 0 3.4 12a3.3 3.3 0 0 0 1.4 4.8 3.4 3.4 0 0 0 5.1 3.3"/><path d="M15.5 3.2a3.4 3.4 0 0 1 3.2 4.2A3.3 3.3 0 0 1 20.6 12a3.3 3.3 0 0 1-1.4 4.8 3.4 3.4 0 0 1-5.1 3.3"/><path d="M12 3.6v17M9 8h6M9.5 13h5"/>',
 "tag": "Curso 02 · Morfología",
 "resumen": "Organización estructural del sistema nervioso, de la médula a la corteza, con correlación clínica.",
 "sub": "Organización estructural del sistema nervioso: médula, tronco encefálico, cerebelo y corteza, con correlación clínico-anatómica.",
 "ficha": [("Nivel", "Pregrado · Morfología"),
           ("Unidades", "4"),
           ("Apuntes", "En preparación"),
           ("Formato", "Diapositivas en PDF"),
           ("Autor", "Dr. Andreé Salvatierra")],
 "bibliografia": [
   "Snell, R. <em>Neuroanatomía clínica</em>.",
   "Haines, D. <em>Principios de neurociencia</em>.",
   "Nolte, J. <em>El cerebro humano</em>.",
   "Netter, F. <em>Atlas de neuroanatomía y neurofisiología</em>."],
 "intro": "Temario provisional. Los apuntes de este curso todavía no se han digitalizado; se irán publicando conforme avance el ciclo.",
 "unidades": [
   {"num": "I", "nombre": "Organización general y médula espinal", "horas": "—", "temas": [
     ("NA-01", "Organización del sistema nervioso", None, 0),
     ("NA-02", "Médula espinal: sustancia gris y blanca", None, 0),
     ("NA-03", "Nervios espinales, dermatomas y miotomas", None, 0)]},
   {"num": "II", "nombre": "Tronco encefálico y cerebelo", "horas": "—", "temas": [
     ("TE-01", "Bulbo, protuberancia y mesencéfalo", None, 0),
     ("TE-02", "Nervios craneales y sus núcleos", None, 0),
     ("TE-03", "Cerebelo: lóbulos y circuitería", None, 0)]},
   {"num": "III", "nombre": "Diencéfalo y telencéfalo", "horas": "—", "temas": [
     ("DT-01", "Tálamo, hipotálamo y epitálamo", None, 0),
     ("DT-02", "Ganglios basales y circuitos motores", None, 0),
     ("DT-03", "Corteza cerebral y áreas de Brodmann", None, 0),
     ("DT-04", "Sistema límbico, hipocampo y amígdala", None, 0)]},
   {"num": "IV", "nombre": "Vías, irrigación y clínica", "horas": "—", "temas": [
     ("VC-01", "Vías ascendentes y descendentes", None, 0),
     ("VC-02", "Polígono de Willis e irrigación encefálica", None, 0),
     ("VC-03", "Meninges, LCR y sistema ventricular", None, 0)]}],
},
{
 "slug": "neurofisiologia",
 "nombre": "Neurofisiología",
 "titulo_html": 'Neuro<em>fisiología</em>',
 "eyebrow": "Curso 03 · Función",
 "ornamento": "Δ",
 "icono": '<path d="M1.5 14h3l2-8 3 15 3-19 3 15 2-6h5"/>',
 "tag": "Curso 03 · Función",
 "resumen": "Cómo el tejido nervioso genera electricidad y la convierte en percepción, movimiento y memoria.",
 "sub": "Cómo el tejido nervioso genera electricidad, la transmite y la convierte en percepción, movimiento y memoria.",
 "ficha": [("Nivel", "Pregrado · Fisiología"),
           ("Unidades", "4"),
           ("Apuntes", "En preparación"),
           ("Formato", "Diapositivas en PDF"),
           ("Autor", "Dr. Andreé Salvatierra")],
 "bibliografia": [
   "Kandel, E. <em>Principios de neurociencia</em>.",
   "Purves, D. <em>Neurociencia</em>.",
   "Bear, Connors &amp; Paradiso. <em>Neurociencia: explorando el cerebro</em>.",
   "Guyton &amp; Hall. <em>Tratado de fisiología médica</em>."],
 "intro": "Temario provisional. Los apuntes de este curso todavía no se han digitalizado; se irán publicando conforme avance el ciclo.",
 "unidades": [
   {"num": "I", "nombre": "Excitabilidad de membrana", "horas": "—", "temas": [
     ("EM-01", "Potencial de reposo y bomba Na⁺/K⁺", None, 0),
     ("EM-02", "Potencial de acción y canales de voltaje", None, 0),
     ("EM-03", "Conducción saltatoria", None, 0)]},
   {"num": "II", "nombre": "Sinapsis y plasticidad", "horas": "—", "temas": [
     ("SP-01", "Transmisión sináptica química y eléctrica", None, 0),
     ("SP-02", "Integración sináptica", None, 0),
     ("SP-03", "LTP, LTD y bases celulares de la memoria", None, 0)]},
   {"num": "III", "nombre": "Sistemas sensoriales y motores", "horas": "—", "temas": [
     ("SM-01", "Transducción sensorial y campos receptivos", None, 0),
     ("SM-02", "Visión: de la retina a V1", None, 0),
     ("SM-03", "Audición, sistema vestibular y somatosensación", None, 0),
     ("SM-04", "Control motor: reflejos y unidad motora", None, 0)]},
   {"num": "IV", "nombre": "Ritmos, sueño y cognición", "horas": "—", "temas": [
     ("RC-01", "EEG: ritmos delta, theta, alfa, beta y gamma", None, 0),
     ("RC-02", "Arquitectura del sueño", None, 0),
     ("RC-03", "Atención, memoria de trabajo y oscilaciones", None, 0)]}],
},
]

STATUS_READY = '<span class="topic-status ready">Apunte PDF</span>'
STATUS_SOON = '<span class="topic-status">En preparación</span>'


def n_pdfs(c):
    return sum(1 for u in c["unidades"] for t in u["temas"] if t[2])


def n_temas(c):
    return sum(len(u["temas"]) for u in c["unidades"])


# ══════════════════════════════════════════════════════════════
#  PORTADA
# ══════════════════════════════════════════════════════════════

def build_index():
    tarjetas = []
    for i, c in enumerate(CURSOS):
        romano = ["I", "II", "III"][i]
        pub = n_pdfs(c)
        meta = ('<span><strong>%d</strong> unidades</span>\n            '
                '<span><strong>%s</strong> apuntes</span>' % (
                    len(c["unidades"]), pub if pub else "—"))
        tarjetas.append('''        <a href="%s.html" class="shelf-card">
          <span class="shelf-num">%s</span>
          <div class="shelf-icon">
            <svg viewBox="0 0 24 24">%s</svg>
          </div>
          <p class="shelf-tag">%s</p>
          <h3 class="shelf-title">%s</h3>
          <p class="shelf-desc">%s</p>
          <div class="shelf-meta">
            %s
          </div>
          <span class="shelf-cta">Entrar a la sala</span>
        </a>''' % (c["slug"], romano, c["icono"], c["tag"], c["nombre"],
                    c["resumen"], meta))

    body = '''  <section class="library-hero" id="portada">
    <div class="hero-neurona izq" aria-hidden="true">
      <img src="img/neuronas-a.webp" alt="" width="334" height="462" loading="eager" decoding="async"/>
    </div>
    <div class="hero-neurona der" aria-hidden="true">
      <img src="img/neuronas-b.webp" alt="" width="393" height="380" loading="eager" decoding="async"/>
    </div>
    <div class="library-hero-inner">
      <p class="hero-eyebrow">Biblioteca abierta de apuntes · Neurociencia</p>
      <h1 class="library-hero-name"><em>A.</em> Salvatierra</h1>
      <p class="library-hero-role">
        Neurocientífico <span class="title-sep">·</span> Docente <span class="title-sep">·</span> Investigador
      </p>
    </div>
  </section>

  <section id="cursos">
    <div class="section">
      <div class="section-header">
        <p class="section-eyebrow">Salas de la biblioteca</p>
        <h2 class="section-title">Los tres <em>cursos</em></h2>
      </div>

      <div class="library-grid">

%s

      </div>

      <div class="courses-show-more">
        <a href="apuntes.html" class="btn-show-more"><span class="psi-btn">Ψ</span> Ver el catálogo completo</a>
      </div>
    </div>
  </section>

  <hr class="gold-line"/>

  <section id="sobre">
    <div class="section">
      <div class="section-header">
        <p class="section-eyebrow">Quién escribe esto</p>
        <h2 class="section-title">Sobre <em>el autor</em></h2>
      </div>

      <div style="max-width:760px;">
        <p class="about-body">El Dr. Andreé Salvatierra Baldeón es neurocientífico y docente. Dicta Farmacología, Neuroanatomía y Neurofisiología, tres cursos que comparten una misma obsesión: entender cómo una molécula, una vía o un potencial de acción terminan produciendo comportamiento.</p>

        <p class="about-body">Este sitio no es un portafolio. Es una biblioteca: cada apunte que aparece aquí fue escrito por él para dictar clase, y se publica tal como está.</p>

        <blockquote class="about-quote">Un apunte guardado en un cajón no le sirve a nadie. Este es el cajón, pero abierto.</blockquote>

        <p class="about-body">El material se actualiza conforme avanza cada ciclo. Si encuentras un error — y los habrá — escríbele; corregirlo mejora el apunte para todos los que vengan después.</p>

        <div class="skills-row">
          <span class="skill-tag accent">Farmacología</span>
          <span class="skill-tag accent">Neuroanatomía</span>
          <span class="skill-tag accent">Neurofisiología</span>
          <span class="skill-tag">Psicofarmacología</span>
          <span class="skill-tag">Neurotransmisión</span>
          <span class="skill-tag">Docencia universitaria</span>
        </div>
      </div>
    </div>
  </section>''' % ("\n\n".join(tarjetas))

    html = page("Dr. Andreé Salvatierra Baldeón — Biblioteca de Neurociencia",
                "Apuntes de Farmacología, Neuroanatomía y Neurofisiología del Dr. Andreé Salvatierra Baldeón. Acceso abierto.",
                "index.html", body)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("  ✓ index.html")


# ══════════════════════════════════════════════════════════════
#  PÁGINAS DE CURSO
# ══════════════════════════════════════════════════════════════

def build_curso(c):
    ficha = "\n".join(
        '            <div class="aside-item"><span>%s</span><span>%s</span></div>' % (k, v)
        for k, v in c["ficha"])
    biblio = "\n".join('            <div class="aside-bib">%s</div>' % b
                       for b in c["bibliografia"])

    unidades = []
    for u in c["unidades"]:
        temas = []
        for code, name, pdf, pags in u["temas"]:
            if pdf:
                temas.append(
                    '            <a href="apuntes/%s/%s" class="topic-row" target="_blank" rel="noopener">\n'
                    '              <span class="topic-code">%s</span>\n'
                    '              <span class="topic-name">%s</span>\n'
                    '              %s\n'
                    '            </a>' % (c["slug"], pdf, code, name, STATUS_READY))
            else:
                temas.append(
                    '            <div class="topic-row">\n'
                    '              <span class="topic-code">%s</span>\n'
                    '              <span class="topic-name">%s</span>\n'
                    '              %s\n'
                    '            </div>' % (code, name, STATUS_SOON))
        unidades.append(
            '        <div class="unit-block">\n'
            '          <div class="unit-head">\n'
            '            <span class="unit-num">%s</span>\n'
            '            <span class="unit-name">%s</span>\n'
            '            <span class="unit-hours">%s</span>\n'
            '          </div>\n'
            '          <div class="unit-body">\n%s\n          </div>\n'
            '        </div>' % (u["num"], u["nombre"], u["horas"], "\n".join(temas)))

    tabs = []
    for o in CURSOS:
        cls = ' class="tab-active"' if o["slug"] == c["slug"] else ''
        tabs.append('<a href="%s.html"%s>%s</a>' % (o["slug"], cls, o["nombre"]))
    tabs_html = '\n      <span class="tab-sep">|</span>\n      '.join(tabs)

    pub = n_pdfs(c)
    if pub:
        nota = ('<strong>Sobre los apuntes.</strong> Los temas marcados como '
                '<em>Apunte PDF</em> abren el documento directamente. Los que dicen '
                '<em>En preparación</em> aún no se han digitalizado. Todo el material '
                'es de libre uso citando la fuente.')
    else:
        nota = ('<strong>Curso en preparación.</strong> El temario que aparece arriba es '
                'provisional y todavía no tiene apuntes publicados. Los documentos se irán '
                'subiendo conforme avance el ciclo.')

    body = '''  <section class="page-hero">
    <div class="page-hero-inner">
      <p class="hero-eyebrow" style="margin-bottom:18px;">%s</p>
      <h1 class="page-hero-title">%s</h1>
      <p class="page-hero-sub">%s</p>
    </div>
    <div class="page-hero-ornament">%s</div>
  </section>

  <section class="courses-tabs-section">
    <div class="courses-tabs">
      <a href="index.html#cursos">Todos</a>
      <span class="tab-sep">|</span>
      %s
      <span class="tab-sep">|</span>
      <a href="apuntes.html">Catálogo</a>
    </div>
  </section>

  <section>
    <div class="section">
      <div class="syllabus-grid">

        <aside class="syllabus-aside">
          <div class="aside-card">
            <p class="aside-label">Ficha del curso</p>
%s
          </div>
          <div class="aside-card">
            <p class="aside-label">Bibliografía base</p>
%s
          </div>
        </aside>

        <div>
          <div class="section-header" style="margin-bottom:34px;">
            <p class="section-eyebrow">Temario y apuntes</p>
            <h2 class="section-title" style="font-size:38px;">Programa <em>del curso</em></h2>
          </div>

          <p class="about-body" style="margin-bottom:34px;">%s</p>

%s

          <div class="callout">
            %s
          </div>

          <div class="courses-show-more" style="justify-content:flex-start;">
            <a href="apuntes.html" class="btn-show-more"><span class="psi-btn">Ψ</span> Ver todos los apuntes</a>
          </div>
        </div>

      </div>
    </div>
  </section>''' % (c["eyebrow"], c["titulo_html"], c["sub"], c["ornamento"],
                   tabs_html, ficha, biblio, c["intro"],
                   "\n".join(unidades), nota)

    html = page("%s — Dr. Andreé Salvatierra Baldeón" % c["nombre"],
                c["sub"], "%s.html" % c["slug"], body)
    open(os.path.join(OUT, "%s.html" % c["slug"]), "w", encoding="utf-8").write(html)
    print("  ✓ %s.html  (%d apuntes / %d temas)" % (c["slug"], pub, n_temas(c)))


# ══════════════════════════════════════════════════════════════
#  CATÁLOGO
# ══════════════════════════════════════════════════════════════

def build_apuntes():
    rows, i = [], 0
    for c in CURSOS:
        for u in c["unidades"]:
            for code, name, pdf, pags in u["temas"]:
                if not pdf:
                    continue
                i += 1
                busca = (name + " " + c["nombre"] + " " + u["nombre"] + " " + code).lower()
                busca = busca.replace("á", "a").replace("é", "e").replace("í", "i")
                busca = busca.replace("ó", "o").replace("ú", "u")
                rows.append(
                    '        <a href="apuntes/%s/%s" class="note-row" target="_blank" rel="noopener"\n'
                    '           data-course="%s" data-search="%s">\n'
                    '          <span class="note-idx">%02d</span>\n'
                    '          <span class="note-main">\n'
                    '            <span class="note-title">%s</span>\n'
                    '            <span class="note-sub">Unidad %s · %s</span>\n'
                    '          </span>\n'
                    '          <span class="note-course">%s</span>\n'
                    '          <span class="note-pages">%d pág.</span>\n'
                    '          <span class="note-dl">Abrir PDF</span>\n'
                    '        </a>' % (c["slug"], pdf, c["slug"], busca, i, name,
                                      u["num"], u["nombre"], c["nombre"], pags))
    total = i

    body = '''  <section class="page-hero">
    <div class="page-hero-inner">
      <p class="hero-eyebrow" style="margin-bottom:18px;">Catálogo completo</p>
      <h1 class="page-hero-title">La <em>biblioteca</em></h1>
      <p class="page-hero-sub">%d apuntes publicados, ordenados por curso y unidad. Busca por tema, filtra por curso, abre el PDF.</p>
    </div>
    <div class="page-hero-ornament">Ψ</div>
  </section>

  <section id="recientes">
    <div class="section">
      <div class="notes-toolbar">
        <input type="search" id="noteSearch" class="notes-search" placeholder="Buscar un tema… (ej. receptores, célula, absorción)" autocomplete="off"/>
        <div class="notes-filters">
          <button class="notes-filter is-active" data-filter="all">Todos</button>
          <button class="notes-filter" data-filter="farmacologia">Farmacología</button>
          <button class="notes-filter" data-filter="neuroanatomia">Neuroanatomía</button>
          <button class="notes-filter" data-filter="neurofisiologia">Neurofisiología</button>
        </div>
      </div>

      <div class="notes-table" id="notesTable">
%s
      </div>
      <p class="notes-empty" id="notesEmpty" style="display:none;">No hay apuntes que coincidan con esa búsqueda.</p>

      <div class="callout">
        <strong>El catálogo crece cada ciclo.</strong> Neuroanatomía y Neurofisiología todavía no tienen apuntes publicados; su temario provisional puede consultarse en la página de cada curso.
      </div>
    </div>
  </section>

  <script>
    (function () {
      var search = document.getElementById('noteSearch');
      var rows = Array.prototype.slice.call(document.querySelectorAll('.note-row'));
      var empty = document.getElementById('notesEmpty');
      var buttons = Array.prototype.slice.call(document.querySelectorAll('.notes-filter'));
      var activeFilter = 'all';

      function normalize(s) {
        return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
      }

      function apply() {
        var q = normalize(search.value.trim());
        var visible = 0;
        rows.forEach(function (row) {
          var matchCourse = activeFilter === 'all' || row.dataset.course === activeFilter;
          var matchText = !q || normalize(row.dataset.search).indexOf(q) !== -1;
          var show = matchCourse && matchText;
          row.classList.toggle('is-hidden', !show);
          if (show) visible++;
        });
        empty.style.display = visible ? 'none' : 'block';
      }

      search.addEventListener('input', apply);
      buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          buttons.forEach(function (b) { b.classList.remove('is-active'); });
          btn.classList.add('is-active');
          activeFilter = btn.dataset.filter;
          apply();
        });
      });
    })();
  </script>''' % (total, "\n".join(rows))

    html = page("Catálogo de apuntes — Dr. Andreé Salvatierra Baldeón",
                "Catálogo de apuntes de Farmacología, Neuroanatomía y Neurofisiología.",
                "apuntes.html", body)
    open(os.path.join(OUT, "apuntes.html"), "w", encoding="utf-8").write(html)
    print("  ✓ apuntes.html  (%d apuntes)" % total)
    return total


if __name__ == "__main__":
    print("Generando el sitio…")
    build_index()
    for c in CURSOS:
        build_curso(c)
    total = build_apuntes()

    manifiesto = {}
    for c in CURSOS:
        manifiesto[c["slug"]] = [
            {"codigo": t[0], "titulo": t[1], "archivo": t[2], "paginas": t[3]}
            for u in c["unidades"] for t in u["temas"]]
    ruta = os.path.join(OUT, "apuntes", "manifiesto.json")
    json.dump(manifiesto, open(ruta, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("Listo. %d apuntes publicados." % total)
