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

NAV_ITEMS = [("index.html", "Inicio"),
             ("biopsicologia.html", "Biopsicología"),
             ("neuroanatomia.html", "Neuroanatomía"),
             ("neuropsicologia.html", "Neuropsicología"),
             ("psicofarmacologia.html", "Psicofarmacología")]


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
          <span class="marca-neurona site-logo-marca">Neurona</span>
          <span class="site-logo-subtitle">Dr. Andreé Salvatierra</span>
        </div>
      </div>
      <nav class="main-nav">%s</nav>
    </div>
    <div class="header-border"></div>
  </header>''' % (NEURON_SVG, nav)


FOOTER = ('''  <footer class="footer-wrap" id="contacto">
    <div class="footer">
      <div class="footer-top">
        <div class="footer-logo-group">
          <div>
            <span class="marca-neurona footer-marca">Neurona</span>
            <div class="footer-logo-sub">Dr. Andreé Salvatierra</div>
          </div>
        </div>
        <div class="footer-links-col">
          <div class="footer-col">
            <div class="footer-col-title">Cursos</div>
            <a href="biopsicologia.html">Biopsicología</a>
            <a href="neuroanatomia.html">Neuroanatomía</a>
            <a href="neuropsicologia.html">Neuropsicología</a>
            <a href="psicofarmacologia.html">Psicofarmacología</a>
          </div>
          <div class="footer-col">
            <div class="footer-col-title">Biblioteca</div>
            <a href="apuntes.html">Catálogo de apuntes</a>
            <a href="noticias.html">Noticias</a>
            <a href="index.html#sobre">Sobre el autor</a>
          </div>
          <div class="footer-col">
            <div class="footer-col-title">Contacto</div>
            <a href="mailto:4andree4@gmail.com">4andree4@gmail.com</a>
            <a href="https://orcid.org/0000-0002-0638-563X" target="_blank" rel="noopener">ORCID</a>
            <a href="https://scholar.google.com/citations?user=h9P861oAAAAJ&amp;hl=es" target="_blank" rel="noopener">Google Scholar</a>
            <a href="https://www.linkedin.com/in/a-salvatierra" target="_blank" rel="noopener">LinkedIn</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span class="footer-copy">© 2026 Dr. Andreé Salvatierra · Apuntes de libre distribución con atribución</span>
      </div>
    </div>
  </footer>''')


def page(title, desc, active, body, body_class=""):
    return '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>%s</title>
  <meta name="description" content="%s"/>
  <link rel="icon" href="favicon.svg" type="image/svg+xml"/>
  <link rel="icon" href="favicon.png" sizes="32x32" type="image/png"/>
  <link rel="apple-touch-icon" href="apple-touch-icon.png"/>
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
 "slug": "biopsicologia",
 "nombre": "Biopsicología",
 "titulo_html": 'Bio<em>psicología</em>',
 "eyebrow": "Curso 01 · Fundamentos",
 "ornamento": "β",
 "icono": '<path d="M12 3.4c-3 0-5.4 2.2-5.4 5 0 1 .3 1.9.8 2.7-1 .9-1.6 2.1-1.6 3.4 0 2.7 2.3 4.9 5.2 4.9 .4 0 .7 0 1-.1"/><path d="M12 3.4c3 0 5.4 2.2 5.4 5 0 1-.3 1.9-.8 2.7 1 .9 1.6 2.1 1.6 3.4 0 2.7-2.3 4.9-5.2 4.9-.4 0-.7 0-1-.1"/><path d="M12 3.6v16.8"/><circle cx="7.4" cy="9.2" r="1.1"/><circle cx="16.6" cy="14.4" r="1.1"/>',
 "tag": "Curso 01 · Fundamentos",
 "resumen": "Las bases biológicas de la conducta: de la célula nerviosa a los sistemas que producen comportamiento.",
 "sub": "Las bases biológicas de la conducta. Cómo el sistema nervioso, las hormonas y la evolución dan forma a lo que hacemos, sentimos y recordamos.",
 "ficha": [("Nivel", "Pregrado · Fundamentos"),
           ("Unidades", "4"),
           ("Apuntes", "En preparación"),
           ("Formato", "Diapositivas en PDF"),
           ("Autor", "Dr. Andreé Salvatierra")],
 "bibliografia": [
   "Pinel, J. <em>Biopsicología</em>.",
   "Kalat, J. <em>Psicología biológica</em>.",
   "Carlson, N. <em>Fisiología de la conducta</em>.",
   "Rosenzweig, M. <em>Psicología biológica</em>."],
 "intro": "Temario provisional. Los apuntes de este curso todavía no se han digitalizado; se irán publicando conforme avance el ciclo.",
 "unidades": [
   {"num": "I", "nombre": "Bases celulares del sistema nervioso", "horas": "—", "temas": [
     ("BP-01", "La neurona y la glía: estructura y función", None, 0),
     ("BP-02", "Potencial de membrana y potencial de acción", None, 0),
     ("BP-03", "Sinapsis y neurotransmisores", None, 0)]},
   {"num": "II", "nombre": "Organización del sistema nervioso", "horas": "—", "temas": [
     ("BP-04", "Sistema nervioso central y periférico", None, 0),
     ("BP-05", "Sistema nervioso autónomo", None, 0),
     ("BP-06", "Desarrollo y plasticidad del sistema nervioso", None, 0)]},
   {"num": "III", "nombre": "Sistemas sensoriales y motores", "horas": "—", "temas": [
     ("BP-07", "Visión, audición y sentidos químicos", None, 0),
     ("BP-08", "Control motor y movimiento", None, 0)]},
   {"num": "IV", "nombre": "Conducta y regulación", "horas": "—", "temas": [
     ("BP-09", "Sueño y ritmos biológicos", None, 0),
     ("BP-10", "Hormonas, emoción y estrés", None, 0),
     ("BP-11", "Aprendizaje y memoria", None, 0)]}],
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
     ("NA-04", "Bulbo, protuberancia y mesencéfalo", None, 0),
     ("NA-05", "Nervios craneales y sus núcleos", None, 0),
     ("NA-06", "Cerebelo: lóbulos y circuitería", None, 0)]},
   {"num": "III", "nombre": "Diencéfalo y telencéfalo", "horas": "—", "temas": [
     ("NA-07", "Tálamo, hipotálamo y epitálamo", None, 0),
     ("NA-08", "Ganglios basales y circuitos motores", None, 0),
     ("NA-09", "Corteza cerebral y áreas de Brodmann", None, 0),
     ("NA-10", "Sistema límbico, hipocampo y amígdala", None, 0)]},
   {"num": "IV", "nombre": "Vías, irrigación y clínica", "horas": "—", "temas": [
     ("NA-11", "Vías ascendentes y descendentes", None, 0),
     ("NA-12", "Polígono de Willis e irrigación encefálica", None, 0),
     ("NA-13", "Meninges, LCR y sistema ventricular", None, 0)]}],
},
{
 "slug": "neuropsicologia",
 "nombre": "Neuropsicología",
 "titulo_html": 'Neuro<em>psicología</em>',
 "eyebrow": "Curso 03 · Clínica",
 "ornamento": "Ψ",
 "icono": '<path d="M4.6 12a7.4 7.4 0 0 1 14.8 0v4.4a2.6 2.6 0 0 1-2.6 2.6h-1.2"/><path d="M4.6 12v5.2M19.4 12v5.2"/><circle cx="9" cy="12.4" r="1.2"/><circle cx="15" cy="12.4" r="1.2"/><path d="M9 15.6c1.6 1.4 4.4 1.4 6 0"/>',
 "tag": "Curso 03 · Clínica",
 "resumen": "Qué se pierde cuando el cerebro se lesiona: funciones superiores, síndromes y evaluación.",
 "sub": "La relación entre lesión cerebral y función mental. Afasias, agnosias, apraxias y los síndromes que revelan cómo está organizada la cognición.",
 "ficha": [("Nivel", "Pregrado · Clínica"),
           ("Unidades", "4"),
           ("Apuntes", "En preparación"),
           ("Formato", "Diapositivas en PDF"),
           ("Autor", "Dr. Andreé Salvatierra")],
 "bibliografia": [
   "Lezak, M. <em>Neuropsychological Assessment</em>.",
   "Kolb &amp; Whishaw. <em>Neuropsicología humana</em>.",
   "Ardila &amp; Ostrosky. <em>Diagnóstico del daño cerebral</em>.",
   "Luria, A. <em>Las funciones corticales superiores del hombre</em>."],
 "intro": "Temario provisional. Los apuntes de este curso todavía no se han digitalizado; se irán publicando conforme avance el ciclo.",
 "unidades": [
   {"num": "I", "nombre": "Fundamentos y método", "horas": "—", "temas": [
     ("NP-01", "Historia y modelos en neuropsicología", None, 0),
     ("NP-02", "Lateralización y especialización hemisférica", None, 0),
     ("NP-03", "Métodos de estudio y neuroimagen", None, 0)]},
   {"num": "II", "nombre": "Lenguaje y funciones simbólicas", "horas": "—", "temas": [
     ("NP-04", "Afasias: clasificación y correlato anatómico", None, 0),
     ("NP-05", "Alexias, agrafias y acalculias", None, 0)]},
   {"num": "III", "nombre": "Percepción, acción y memoria", "horas": "—", "temas": [
     ("NP-06", "Agnosias visuales, auditivas y táctiles", None, 0),
     ("NP-07", "Apraxias y trastornos del movimiento intencional", None, 0),
     ("NP-08", "Amnesias y sistemas de memoria", None, 0)]},
   {"num": "IV", "nombre": "Funciones ejecutivas y evaluación", "horas": "—", "temas": [
     ("NP-09", "Síndrome frontal y funciones ejecutivas", None, 0),
     ("NP-10", "Atención y heminegligencia", None, 0),
     ("NP-11", "Baterías y protocolos de evaluación", None, 0)]}],
},
{
 "slug": "psicofarmacologia",
 "nombre": "Psicofarmacología",
 "titulo_html": 'Psico<em>farmacología</em>',
 "eyebrow": "Curso 04 · Clínica",
 "ornamento": "Rx",
 "icono": '<circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="1.1"/><path d="M15.2 12h5M3.8 12h5M12 3.4v5.4M12 15.2v5.4"/><path d="M14.9 9.1 18 6M9.1 14.9 6 18M14.9 14.9 18 18M9.1 9.1 6 6"/>',
 "tag": "Curso 04 · Clínica",
 "resumen": "De las bases celulares y moleculares a la acción de los psicofármacos sobre la neurotransmisión.",
 "sub": "Los elementos centrales de la psicofarmacología asociados a los síndromes clínicos. De la célula y la molécula a la farmacocinética, la farmacodinamia y la acción sobre la transmisión sináptica.",
 "ficha": [("Nivel", "Pregrado · Clínica"),
           ("Unidades", "4"),
           ("Apuntes", "6 publicados"),
           ("Páginas", "250 en total"),
           ("Formato", "Diapositivas en PDF"),
           ("Autor", "Dr. Andreé Salvatierra")],
 "bibliografia": [
   "Stahl, S. <em>Psicofarmacología esencial</em>.",
   "Julien, R. <em>Manual de psicofarmacología</em>.",
   "Goodman &amp; Gilman. <em>Las bases farmacológicas de la terapéutica</em>.",
   "Katzung, B. <em>Farmacología básica y clínica</em>."],
 "intro": "El curso abre por donde importa: qué es la psicofarmacología y sobre qué actúa. La mayoría de psicofármacos ejercen su efecto interviniendo algún mecanismo de la transmisión sináptica química. De ahí baja a las bases celulares y moleculares, y termina con los dos pilares clásicos: qué le hace el organismo al fármaco y qué le hace el fármaco al organismo.",
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
]

STATUS_READY = '<span class="topic-status ready">Leer apunte</span>'
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
        romano = ["I", "II", "III", "IV", "V"][i]
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
      <h1 class="marca-neurona library-hero-name">Neurona</h1>
      <p class="hero-lema"><span>Biblioteca abierta de apuntes</span></p>
      <p class="library-hero-role">Dr. Andreé Salvatierra</p>
    </div>
  </section>

  <section id="cursos">
    <div class="section">
      <div class="section-header">
        <p class="section-eyebrow">Salas de la biblioteca</p>
        <h2 class="section-title">Los cuatro <em>cursos</em></h2>
      </div>

      <div class="library-grid">

%s

      </div>

      <div class="courses-show-more">
        <a href="apuntes.html" class="btn-show-more">Ver el catálogo completo</a>
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

      <div class="autor-grid">
        <div class="autor-retrato">
          <img src="img/autor.webp" alt="Dr. Andreé Salvatierra Baldeón"
               width="600" height="950" loading="lazy" decoding="async"/>
          <div class="corner-ornament tl"></div>
          <div class="corner-ornament tr"></div>
          <div class="corner-ornament bl"></div>
          <div class="corner-ornament br"></div>
        </div>

        <div class="autor-texto">
          <h3 class="autor-nombre">Andreé Salvatierra Baldeón</h3>

          <p class="about-body">Posdoctorado en la unidad de cognición y conducta del Instituto Nacional de Neurología y Neurocirugía de México. Doctor en neurociencias por la Facultad de Medicina de la Universidad Nacional Mayor de San Marcos, especialista en neuropsicología por la Universidad Nacional Federico Villarreal, máster en psicofarmacología por la Universidad de Valencia, máster en farmacología por la Facultad de Medicina de la Universidad Autónoma de Barcelona y psicólogo por la Universidad Continental.</p>

          <p class="about-body">Estancias de investigación y formación en el departamento de salud pública y la escuela profesional de neurociencias de la UNAM, en la Universidad Pedagógica Nacional de México y en la unidad de ensayos clínicos del Institut Hospital del Mar d’Investigacions Mèdiques. Pasantías en la Universidad de Antioquia y en la Facultad de Psicología de la UNAM; rotante en la unidad de neuropsiquiatría, el centro de investigaciones cerebrales y la unidad de neuroimagen del INNN.</p>

          <p class="autor-registros">
            <span>CPsP <strong>32563</strong></span>
            <span>RNE <strong>622</strong></span>
            <span>RENACYT <strong>P0093916</strong></span>
          </p>

          <div class="perfiles">
            <a class="perfil" href="https://www.linkedin.com/in/a-salvatierra" target="_blank" rel="noopener noreferrer"><span class="perfil-icono"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="2.6" width="18.8" height="18.8" rx="3.4"/><circle cx="7.6" cy="7.7" r="1.15" fill="currentColor" stroke="none"/><path d="M7.6 10.8v6.6"/><path d="M11.4 17.4v-6.6"/><path d="M11.4 13.2c0-1.5 1.1-2.5 2.5-2.5s2.5 1 2.5 2.5v4.2"/></svg></span><span>LinkedIn</span></a>\n            <a class="perfil" href="https://www.researchgate.net/profile/Andree-Salvatierra-Baldeon?ev=hdr_xprf" target="_blank" rel="noopener noreferrer"><span class="perfil-icono"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="2.6" width="18.8" height="18.8" rx="3.4"/><path d="M8.6 17.2V7.4h3.1c1.7 0 2.7 1 2.7 2.5s-1 2.5-2.7 2.5H9.9"/><path d="M12 12.4l3 4.8"/></svg></span><span>ResearchGate</span></a>\n            <a class="perfil" href="https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=93916" target="_blank" rel="noopener noreferrer"><span class="perfil-icono"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="4.6" width="18.8" height="14.8" rx="2.4"/><circle cx="8.6" cy="11" r="2.1"/><path d="M5.2 16.4c.5-1.6 1.8-2.5 3.4-2.5s2.9.9 3.4 2.5"/><path d="M14.8 10.2h4M14.8 13.4h4"/></svg></span><span>CTI Vitae</span></a>\n            <a class="perfil" href="https://orcid.org/0000-0002-0638-563X" target="_blank" rel="noopener noreferrer"><span class="perfil-icono"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.4"/><circle cx="8.5" cy="7.9" r="0.95" fill="currentColor" stroke="none"/><path d="M8.5 10.6v6.4"/><path d="M12.4 17v-6.4h2.1a3.2 3.2 0 0 1 0 6.4Z"/></svg></span><span>ORCID</span></a>\n            <a class="perfil" href="https://scholar.google.com/citations?user=h9P861oAAAAJ&amp;hl=es" target="_blank" rel="noopener noreferrer"><span class="perfil-icono"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.6 22 8.6l-10 5-10-5Z"/><path d="M5.6 11v4.8c0 1.9 2.9 3.4 6.4 3.4s6.4-1.5 6.4-3.4V11"/><path d="M21.2 9.2v5.2"/></svg></span><span>Google Scholar</span></a>
          </div>
        </div>
      </div>

      <div class="escudos-bloque">
        <p class="escudos-titulo">Formación</p>
        <div class="escudos escudos--seis">
            <figure class="escudo">\n              <img src="img/escudos/continental.webp" alt="Universidad Continental" loading="lazy" decoding="async"/>\n              <figcaption><strong>Universidad Continental</strong><span>Pregrado en psicología</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/villarreal.webp" alt="U. N. Federico Villarreal" loading="lazy" decoding="async"/>\n              <figcaption><strong>U. N. Federico Villarreal</strong><span>Especialidad en neuropsicología</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/valencia.webp" alt="Universitat de València" loading="lazy" decoding="async"/>\n              <figcaption><strong>Universitat de València</strong><span>Máster en psicofarmacología</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/uab.webp" alt="U. Autònoma de Barcelona" loading="lazy" decoding="async"/>\n              <figcaption><strong>U. Autònoma de Barcelona</strong><span>Máster en farmacología</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/unmsm.webp" alt="UNMSM" loading="lazy" decoding="async"/>\n              <figcaption><strong>UNMSM</strong><span>Doctorado en neurociencias</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/innn.webp" alt="INNN · México" loading="lazy" decoding="async"/>\n              <figcaption><strong>INNN · México</strong><span>Posdoctorado</span></figcaption>\n            </figure>
        </div>

        <p class="escudos-titulo">Estancias e investigación</p>
        <div class="escudos escudos--cuatro">
            <figure class="escudo">\n              <img src="img/escudos/unam.webp" alt="UNAM · México" loading="lazy" decoding="async"/>\n              <figcaption><strong>UNAM · México</strong><span>Salud pública y neurociencias</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/upn.webp" alt="U. Pedagógica Nacional" loading="lazy" decoding="async"/>\n              <figcaption><strong>U. Pedagógica Nacional</strong><span>México</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/imim.webp" alt="IMIM · Hospital del Mar" loading="lazy" decoding="async"/>\n              <figcaption><strong>IMIM · Hospital del Mar</strong><span>Unidad de ensayos clínicos</span></figcaption>\n            </figure>\n            <figure class="escudo">\n              <img src="img/escudos/antioquia.webp" alt="U. de Antioquia" loading="lazy" decoding="async"/>\n              <figcaption><strong>U. de Antioquia</strong><span>Colombia</span></figcaption>\n            </figure>
        </div>
      </div>

      <div class="linea-corta"></div>

      <div class="courses-show-more">
        <a href="noticias.html" class="btn-show-more">Noticias</a>
      </div>
    </div>
  </section>

''' % ("\n\n".join(tarjetas))

    html = page("Neurona — Dr. Andreé Salvatierra",
                "Neurona: biblioteca de apuntes del Dr. Andreé Salvatierra. Biopsicología, Neuroanatomía, Neuropsicología y Psicofarmacología.",
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
                    '            <a href="visor.html?doc=%s/%s" class="topic-row">\n'
                    '              <span class="topic-name">%s</span>\n'
                    '              %s\n'
                    '            </a>' % (c["slug"], pdf, name, STATUS_READY))
            else:
                temas.append(
                    '            <div class="topic-row">\n'
                    '              <span class="topic-name">%s</span>\n'
                    '              %s\n'
                    '            </div>' % (name, STATUS_SOON))
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
                '<em>Leer apunte</em> se abren en el visor del sitio. Los que dicen '
                '<em>En preparación</em> aún no se han digitalizado. El material se '
                'consulta en línea; no está disponible para descarga.')
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
            <a href="apuntes.html" class="btn-show-more">Ver todos los apuntes</a>
          </div>
        </div>

      </div>
    </div>
  </section>''' % (c["eyebrow"], c["titulo_html"], c["sub"], c["ornamento"],
                   tabs_html, ficha, biblio, c["intro"],
                   "\n".join(unidades), nota)

    html = page("%s — Neurona · Dr. Andreé Salvatierra" % c["nombre"],
                c["sub"], "%s.html" % c["slug"], body)
    open(os.path.join(OUT, "%s.html" % c["slug"]), "w", encoding="utf-8").write(html)
    print("  ✓ %s.html  (%d apuntes / %d temas)" % (c["slug"], pub, n_temas(c)))


# ══════════════════════════════════════════════════════════════
#  CATÁLOGO
# ══════════════════════════════════════════════════════════════

def build_apuntes():
    filtros = ['          <button class="notes-filter" data-filter="%s">%s</button>'
               % (c["slug"], c["nombre"]) for c in CURSOS]
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
                    '        <a href="visor.html?doc=%s/%s" class="note-row"\n'
                    '           data-course="%s" data-search="%s">\n'
                    '          <span class="note-main">\n'
                    '            <span class="note-title">%s</span>\n'
                    '            <span class="note-sub">Unidad %s · %s</span>\n'
                    '          </span>\n'
                    '          <span class="note-course">%s</span>\n'
                    '          <span class="note-pages">%d pág.</span>\n'
                    '          <span class="note-dl">Leer</span>\n'
                    '        </a>' % (c["slug"], pdf, c["slug"], busca, name,
                                      u["num"], u["nombre"], c["nombre"], pags))
    total = i

    body = '''  <section class="page-hero">
    <div class="page-hero-inner">
      <p class="hero-eyebrow" style="margin-bottom:18px;">Catálogo completo</p>
      <h1 class="page-hero-title">La <em>biblioteca</em></h1>
      <p class="page-hero-sub">%d apuntes publicados, ordenados por curso y unidad. Busca por tema, filtra por curso, abre el PDF.</p>
    </div>
    <div class="page-hero-ornament">N</div>
  </section>

  <section id="recientes">
    <div class="section">
      <div class="notes-toolbar">
        <input type="search" id="noteSearch" class="notes-search" placeholder="Buscar un tema… (ej. receptores, célula, absorción, sinapsis)" autocomplete="off"/>
        <div class="notes-filters">
          <button class="notes-filter is-active" data-filter="all">Todos</button>
%s
        </div>
      </div>

      <div class="notes-table" id="notesTable">
%s
      </div>
      <p class="notes-empty" id="notesEmpty" style="display:none;">No hay apuntes que coincidan con esa búsqueda.</p>

      <div class="callout">
        <strong>El catálogo crece cada ciclo.</strong> Biopsicología, Neuroanatomía y Neuropsicología todavía no tienen apuntes publicados; su temario provisional puede consultarse en la página de cada curso.
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
  </script>''' % (total, "\n".join(filtros), "\n".join(rows))

    html = page("Catálogo de apuntes — Neurona",
                "Catálogo completo de apuntes del Dr. Andreé Salvatierra.",
                "apuntes.html", body)
    open(os.path.join(OUT, "apuntes.html"), "w", encoding="utf-8").write(html)
    print("  ✓ apuntes.html  (%d apuntes)" % total)
    return total



# ══════════════════════════════════════════════════════════════
#  VISOR DE APUNTES
#  Dibuja el PDF en lienzos: no hay enlace al archivo ni barra
#  del navegador, así que tampoco botón de descarga.
# ══════════════════════════════════════════════════════════════

def build_visor():
    catalogo = {}
    for c in CURSOS:
        for u in c["unidades"]:
            for code, name, pdf, pags in u["temas"]:
                if pdf:
                    catalogo["%s/%s" % (c["slug"], pdf)] = {
                        "titulo": name, "curso": c["nombre"],
                        "unidad": "Unidad %s · %s" % (u["num"], u["nombre"]),
                        "paginas": pags,
                    }

    body = '''  <section class="visor-cab">
    <div class="visor-cab-inner">
      <a href="apuntes.html" class="visor-volver">Volver al catálogo</a>
      <div class="visor-titulos">
        <h1 class="visor-titulo" id="vTitulo">Cargando…</h1>
        <p class="visor-meta" id="vMeta"></p>
      </div>
      <div class="visor-paginas" id="vPaginas"></div>
    </div>
  </section>

  <section class="visor-zona">
    <div class="visor-aviso" id="vAviso" hidden></div>
    <div class="visor-lienzos" id="vLienzos" oncontextmenu="return false"></div>
    <p class="visor-pie">
      Material del Dr. Andreé Salvatierra. Uso educativo; prohibida su
      descarga, reproducción y distribución.
    </p>
  </section>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
  <script>
    var CATALOGO = %s;

    (function () {
      var zona    = document.getElementById('vLienzos');
      var aviso   = document.getElementById('vAviso');
      var titulo  = document.getElementById('vTitulo');
      var meta    = document.getElementById('vMeta');
      var contador= document.getElementById('vPaginas');

      function fallo(txt) {
        aviso.hidden = false; aviso.textContent = txt;
        titulo.textContent = 'Apunte no disponible';
      }

      var doc = new URLSearchParams(location.search).get('doc') || '';
      /* Solo se admiten rutas que estén en el catálogo: nada de cargar
         archivos arbitrarios desde la barra de direcciones. */
      var ficha = Object.prototype.hasOwnProperty.call(CATALOGO, doc) ? CATALOGO[doc] : null;
      if (!ficha) { fallo('Ese apunte no existe en el catálogo.'); return; }

      titulo.textContent = ficha.titulo;
      meta.textContent = ficha.curso + ' · ' + ficha.unidad;
      contador.textContent = ficha.paginas + ' pág.';
      document.title = ficha.titulo + ' — Neurona';

      if (typeof pdfjsLib === 'undefined') {
        fallo('No se pudo cargar el visor. Comprueba tu conexión.'); return;
      }
      pdfjsLib.GlobalWorkerOptions.workerSrc =
        'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

      var escala = Math.min(2, (window.devicePixelRatio || 1) * 1.25);

      pdfjsLib.getDocument({ url: 'apuntes/' + doc, password: '' }).promise.then(function (pdf) {
        var ancho = zona.clientWidth || 900;
        var cadena = Promise.resolve();
        for (var n = 1; n <= pdf.numPages; n++) {
          (function (n) {
            cadena = cadena.then(function () {
              return pdf.getPage(n).then(function (pagina) {
                var base = pagina.getViewport({ scale: 1 });
                var vista = pagina.getViewport({ scale: (ancho / base.width) * escala });

                var hoja = document.createElement('div');
                hoja.className = 'visor-hoja';
                var lienzo = document.createElement('canvas');
                lienzo.width = vista.width; lienzo.height = vista.height;
                lienzo.style.width = '100%%'; lienzo.style.height = 'auto';
                var num = document.createElement('span');
                num.className = 'visor-num'; num.textContent = n + ' / ' + pdf.numPages;
                hoja.appendChild(lienzo); hoja.appendChild(num);
                zona.appendChild(hoja);

                return pagina.render({
                  canvasContext: lienzo.getContext('2d', { alpha: false }),
                  viewport: vista
                }).promise;
              });
            });
          })(n);
        }
        return cadena;
      }).catch(function () {
        fallo('No se pudo abrir el apunte.');
      });

      /* Fricción: ni menú contextual, ni arrastrar, ni atajos de guardado. */
      document.addEventListener('contextmenu', function (e) { e.preventDefault(); });
      document.addEventListener('dragstart', function (e) { e.preventDefault(); });
      document.addEventListener('keydown', function (e) {
        var k = (e.key || '').toLowerCase();
        if ((e.ctrlKey || e.metaKey) && ['s', 'p', 'u'].indexOf(k) !== -1) {
          e.preventDefault();
        }
      });
    })();
  </script>''' % json.dumps(catalogo, ensure_ascii=False)

    html = page("Visor de apuntes — Neurona",
                "Visor de apuntes del Dr. Andreé Salvatierra.",
                "apuntes.html", body)
    html = html.replace("<head>", "<head>\n  <meta name=\"robots\" content=\"noindex\"/>")
    open(os.path.join(OUT, "visor.html"), "w", encoding="utf-8").write(html)
    print("  ✓ visor.html  (%d apuntes en el catálogo)" % len(catalogo))



# ══════════════════════════════════════════════════════════════
#  NOTICIAS
#  Las entradas viven en noticias.json y se leen en el navegador,
#  así que basta con editar ese archivo: no hay que regenerar nada.
# ══════════════════════════════════════════════════════════════

ORCID_ID = "0000-0002-0638-563X"
LINKEDIN = "https://www.linkedin.com/in/a-salvatierra"

JS_NOTICIAS = """
    function fechaLarga(iso) {
      var p = (iso || '').split('-');
      if (p.length !== 3) return iso || '';
      var meses = ['enero','febrero','marzo','abril','mayo','junio','julio',
                   'agosto','septiembre','octubre','noviembre','diciembre'];
      return parseInt(p[2], 10) + ' de ' + meses[parseInt(p[1], 10) - 1] + ' de ' + p[0];
    }

    function limpiar(t) {
      var d = document.createElement('div');
      d.textContent = t == null ? '' : String(t);
      return d.innerHTML;
    }

    function pintarNoticias(destino, entradas, tope) {
      if (!destino) return;
      if (!entradas.length) {
        destino.innerHTML = '<p class="noticias-vacio">Todavía no hay entradas publicadas.</p>';
        return;
      }
      entradas.sort(function (a, b) { return (b.fecha || '').localeCompare(a.fecha || ''); });
      if (tope) entradas = entradas.slice(0, tope);
      destino.innerHTML = entradas.map(function (n) {
        var enlace = n.enlace
          ? '<a class="noticia-enlace" href="' + limpiar(n.enlace) +
            '" target="_blank" rel="noopener noreferrer">Ver más</a>'
          : '';
        return '<article class="noticia">' +
                 '<div class="noticia-meta">' +
                   '<time datetime="' + limpiar(n.fecha) + '">' + limpiar(fechaLarga(n.fecha)) + '</time>' +
                   (n.etiqueta ? '<span class="noticia-etiqueta">' + limpiar(n.etiqueta) + '</span>' : '') +
                 '</div>' +
                 '<div class="noticia-cuerpo">' +
                   '<h3 class="noticia-titulo">' + limpiar(n.titulo) + '</h3>' +
                   '<p class="noticia-texto">' + limpiar(n.texto) + '</p>' +
                   enlace +
                 '</div>' +
               '</article>';
      }).join('');
    }

    function cargarNoticias(destino, tope) {
      if (!destino) return;
      fetch('noticias.json', { cache: 'no-cache' })
        .then(function (r) { return r.json(); })
        .then(function (d) { pintarNoticias(destino, d.entradas || [], tope); })
        .catch(function () {
          destino.innerHTML = '<p class="noticias-vacio">No se pudieron cargar las entradas. ' +
            'Si estás viendo la página desde el disco, ábrela con un servidor local.</p>';
        });
    }
"""

JS_ORCID = """
    /* Publicaciones: se leen de ORCID, que sí tiene API pública.
       Si falla, el bloque se oculta y no pasa nada. */
    function cargarPublicaciones(destino, seccion) {
      if (!destino) return;
      fetch('https://pub.orcid.org/v3.0/%s/works', { headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          var obras = (d.group || []).map(function (g) {
            var w = g['work-summary'][0];
            var anio = w['publication-date'] && w['publication-date'].year
                     ? w['publication-date'].year.value : '';
            var revista = w['journal-title'] ? w['journal-title'].value : '';
            var doi = '';
            (g['external-ids'] && g['external-ids']['external-id'] || []).forEach(function (e) {
              if (e['external-id-type'] === 'doi') doi = e['external-id-value'];
            });
            return { titulo: w.title.title.value, anio: anio, revista: revista, doi: doi };
          });
          obras.sort(function (a, b) { return (b.anio || '').localeCompare(a.anio || ''); });
          if (!obras.length) { if (seccion) seccion.hidden = true; return; }
          destino.innerHTML = obras.map(function (o) {
            var url = o.doi ? 'https://doi.org/' + o.doi : '';
            var titulo = url
              ? '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + limpiar(o.titulo) + '</a>'
              : limpiar(o.titulo);
            return '<li class="publicacion">' +
                     '<span class="publicacion-anio">' + limpiar(o.anio || '—') + '</span>' +
                     '<span class="publicacion-datos">' +
                       '<span class="publicacion-titulo">' + titulo + '</span>' +
                       (o.revista ? '<span class="publicacion-revista">' + limpiar(o.revista) + '</span>' : '') +
                     '</span>' +
                   '</li>';
          }).join('');
        })
        .catch(function () { if (seccion) seccion.hidden = true; });
    }
""" % ORCID_ID


def build_noticias():
    body = '''  <section class="page-hero">
    <div class="page-hero-inner">
      <p class="hero-eyebrow" style="margin-bottom:18px;">Actividad reciente</p>
      <h1 class="page-hero-title">Noti<em>cias</em></h1>
      <p class="page-hero-sub">Congresos, publicaciones, docencia y apariciones. Lo que va ocurriendo, en orden.</p>
    </div>
    <div class="page-hero-ornament">§</div>
  </section>

  <section>
    <div class="section">
      <div class="noticias-grid">
        <div>
          <div class="noticias" id="listaNoticias">
            <p class="noticias-vacio">Cargando…</p>
          </div>
        </div>

        <aside class="noticias-lateral">
          <div class="aside-card">
            <p class="aside-label">Seguir la actividad</p>
            <p class="lateral-texto">LinkedIn es donde el Dr. Salvatierra publica el día a día: congresos, clases y colaboraciones.</p>
            <a class="perfil perfil--bloque" href="%s" target="_blank" rel="noopener noreferrer">
              <span class="perfil-icono"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="2.6" width="18.8" height="18.8" rx="3.4"/><circle cx="7.6" cy="7.7" r="1.15" fill="currentColor" stroke="none"/><path d="M7.6 10.8v6.6"/><path d="M11.4 17.4v-6.6"/><path d="M11.4 13.2c0-1.5 1.1-2.5 2.5-2.5s2.5 1 2.5 2.5v4.2"/></svg></span>
              <span>Ver actividad en LinkedIn</span>
            </a>
          </div>
        </aside>
      </div>

      <section class="publicaciones-bloque" id="bloquePublicaciones">
        <p class="escudos-titulo">Publicaciones · actualizado desde ORCID</p>
        <ul class="publicaciones" id="listaPublicaciones"></ul>
      </section>
    </div>
  </section>

  <script>
%s
%s
    cargarNoticias(document.getElementById('listaNoticias'), 0);
    cargarPublicaciones(document.getElementById('listaPublicaciones'),
                        document.getElementById('bloquePublicaciones'));
  </script>''' % (LINKEDIN, JS_NOTICIAS, JS_ORCID)

    html = page("Noticias — Neurona · Dr. Andreé Salvatierra",
                "Actividad reciente del Dr. Andreé Salvatierra: congresos, publicaciones y docencia.",
                "noticias.html", body)
    open(os.path.join(OUT, "noticias.html"), "w", encoding="utf-8").write(html)
    print("  ✓ noticias.html")


if __name__ == "__main__":
    print("Generando el sitio…")
    build_index()
    for c in CURSOS:
        build_curso(c)
    total = build_apuntes()
    build_visor()
    build_noticias()

    manifiesto = {}
    for c in CURSOS:
        manifiesto[c["slug"]] = [
            {"codigo": t[0], "titulo": t[1], "archivo": t[2], "paginas": t[3]}
            for u in c["unidades"] for t in u["temas"]]
    ruta = os.path.join(OUT, "apuntes", "manifiesto.json")
    json.dump(manifiesto, open(ruta, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("Listo. %d apuntes publicados." % total)
