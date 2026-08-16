# Neurona — Dr. Andreé Salvatierra

Sitio estático con los apuntes de clase de cuatro cursos: **Biopsicología**,
**Neuroanatomía**, **Neuropsicología** y **Psicofarmacología**.
Sin build, sin dependencias: HTML + un CSS. Se publica tal cual en GitHub Pages.

**Estado actual:** 20 apuntes publicados (914 páginas), todos en
Psicofarmacología. Los otros tres cursos tienen temario provisional y ningún
PDF todavía.

---

## Publicar en GitHub Pages

```bash
git init
git add .
git commit -m "Biblioteca de apuntes — versión inicial"
git branch -M main
git remote add origin https://github.com/USUARIO/REPO.git
git push -u origin main
```

Luego en GitHub: **Settings → Pages → Source: Deploy from a branch → Branch: `main` / `(root)`**.
El sitio queda en `https://USUARIO.github.io/REPO/`.

> Los PDFs pesan ~27 MB en total. Está dentro de lo que GitHub admite sin problema.

---

## Estructura

```
.
├── index.html                 Portada: logotipo, nombre y sobre el autor
├── contacto.html              Teléfono, correo, perfiles y formulario
├── materiales.html            Las cuatro tarjetas de curso
├── investigacion.html         Publicaciones, tesis, conferencias y distinciones
├── biopsicologia.html         Temario provisional
├── neuroanatomia.html         Temario provisional
├── neuropsicologia.html       Temario provisional
├── psicofarmacologia.html     Temario + 6 apuntes
├── apuntes.html               Catálogo con buscador y filtros
├── noticias.html              Actividad: lo que se escribe a mano
├── noticias.json              Las entradas de noticias (se edita a mano)
├── visor.html                 Visor de apuntes (no se enlaza a los PDF)
├── css/theme.css              Todo el estilo (un solo archivo)
├── fonts/neurona.woff2        Tipografía del logotipo, recortada (3,9 KB)
├── img/                       Neuronas, retrato, escudos y media de noticias
│   └── noticias/              Carteles y el vídeo de las publicaciones
└── apuntes/
    ├── biopsicologia/         (vacío)
    ├── neuroanatomia/         (vacío)
    ├── neuropsicologia/       (vacío)
    ├── psicofarmacologia/     6 PDFs
    └── manifiesto.json        Listado generado
```

---

## Añadir o cambiar apuntes

El HTML se genera desde `build.py`, que está **un nivel arriba** de esta carpeta.
Editar ahí es más seguro que editar cinco archivos HTML a mano.

Cada tema es una tupla de cuatro campos:

```python
("PK-01", "Farmacocinética: absorción, distribución…", "05-farmacocinetica.pdf", 93)
#  código   título que se muestra                        archivo PDF (o None)      páginas
```

Para publicar un apunte nuevo:

1. Copia el PDF **limpio** a `originales/` con un nombre en minúsculas y sin tildes.
2. Añade una línea al diccionario `DESTINOS` de `proteger.py` indicando a qué curso va.
3. En `build.py`, busca el curso y la unidad, y cambia el `None` por el nombre del
   archivo (o añade una tupla nueva).
4. Ejecuta `python3 proteger.py` y después `python3 build.py`.

Las páginas se regeneran solas: portada, página del curso, catálogo y sus filtros.
Los contadores ("4 apuntes", "93 pág.") se calculan a partir de los datos, no hay que
tocarlos. Añadir o quitar un curso de la lista `CURSOS` crea o borra su página, su
tarjeta en la portada, su pestaña y su filtro en el catálogo.

Si solo quieres **reemplazar** un PDF por una versión corregida, sobrescribe el de
`originales/` conservando el mismo nombre y vuelve a ejecutar `proteger.py`.

### Cambiar el temario

Los temarios de Biopsicología, Neuroanatomía y Neuropsicología son provisionales — los
escribí a partir del contenido estándar de esos cursos, no del programa real de Andreé.
Cámbialos en `build.py` (listas `unidades`) y vuelve a ejecutarlo.

### Los veinte PDFs

Todos viven en Psicofarmacología, repartidos en diez unidades que respetan la
numeración con la que Andreé los tiene ordenados:

| Unidad | Apuntes | Páginas |
|---|---|---|
| I · Introducción a la psicofarmacología | 1, 2 | 20 |
| II · Bases celulares y moleculares | 3, 4 | 94 |
| III · Farmacocinética | 5 | 93 |
| IV · Farmacodinamia | 6 | 43 |
| V · Variabilidad de la respuesta | 7, 8 | 75 |
| VI · Desarrollo del medicamento | 9, 10 | 106 |
| VII · Factores modificadores | 11 | 35 |
| VIII · Neurotransmisión y psicofármacos | 12, 13, 14, 15, 16, 17, 18 | 360 |
| IX · Toxicomanías | 19 | 55 |
| X · Ética de la práctica farmacológica | 20 | 33 |

---

## Protección de los apuntes

Antes que nada, con honestidad: **en un sitio estático no se puede impedir la
descarga**. El navegador tiene que recibir el archivo para poder mostrarlo, así
que quien sepa abrir las herramientas de desarrollador podrá quedárselo. Lo que
sí se puede hacer —y está hecho— es poner el listón alto y dejar marcado el
material para que, si sale de aquí, se sepa de quién es.

### Lo que es permanente

**Marca de agua incrustada.** Cada una de las 914 páginas lleva el logotipo
caligráfico y el nombre estampados en el propio PDF, no superpuestos por el navegador: una
diagonal muy tenue repetida por toda la página y un pie con el logotipo, el
nombre y el aviso de uso. Va dentro del archivo, así que sobrevive a cualquier
copia. El lado derecho del pie se deja libre a propósito porque ahí está la
firma que Andreé ya lleva en sus diapositivas.

**Cifrado AES-256 con permisos denegados.** Los archivos se abren sin
contraseña, pero llevan denegados imprimir, copiar texto, extraer contenido y
modificar. Los lectores que respetan la norma —Acrobat, Vista Previa, Edge—
hacen caso. La contraseña de propietario se genera al azar en cada ejecución y
no se guarda: nadie puede levantar esas restricciones, ni siquiera nosotros.

### Lo que es fricción

**Visor propio.** `visor.html` dibuja las páginas en lienzos con PDF.js. No hay
etiqueta `<embed>` ni `<iframe>`, así que no aparece la barra del visor de PDF
del navegador con su botón de descarga y su botón de imprimir. Ninguna página
del sitio enlaza ya a un archivo `.pdf`.

**Solo abre lo que está en el catálogo.** El visor compara el parámetro `?doc=`
con una lista incrustada; escribir otra ruta a mano no carga nada.

**Bloqueos de interfaz.** Sin menú contextual, sin arrastrar imágenes, sin
Ctrl+S, Ctrl+P ni Ctrl+U, y una regla de impresión que deja la hoja en blanco
con un aviso.

### Regenerar los apuntes protegidos

Los PDF **limpios** viven en `originales/`, un nivel arriba de esta
carpeta, y nunca se tocan. El script `proteger.py` los lee de ahí y escribe los
protegidos en `apuntes/`:

```bash
python3 proteger.py
```

Se puede ejecutar las veces que haga falta: como siempre parte de los
originales, la marca no se acumula. Para añadir un apunte nuevo, se copia el PDF
limpio a `originales/`, se añade una línea al diccionario `DESTINOS` indicando a
qué curso va, y se ejecuta el script.

Dos números para ajustar la marca, al principio de `proteger.py`:

```python
OPACIDAD_DIAGONAL = 0.055   # la diagonal repetida
OPACIDAD_PIE      = 0.42    # el logotipo y el nombre del pie
```

> **Importante:** `originales/` no debe subirse a GitHub. El `.gitignore` ya lo
> excluye, pero conviene comprobarlo antes del primer `push`.

---

## Editar textos

- **Logotipo** — es texto con una tipografía propia. Ver la sección *El logotipo*.
- **Subtítulo del encabezado** — en `build.py`, función `header()`.
- **Antetítulo de la portada** — en `build.py`, función `build_index()`.
- **Correo y enlaces académicos** — en `build.py`, constante `FOOTER`.
- **Botones de perfil** — en `build.py`, lista `PERFILES`.
- **Bio de la portada** — en `build.py`, función `build_index()`.
- **Ficha y bibliografía de un curso** — en `build.py`, claves `ficha` y `bibliografia`.

### Colores

Todo el tema sale de las variables al inicio de `css/theme.css`:

```css
:root {
  --gold: #C8A96E;       /* único color visible en reposo */
  --blue: #1B3A5C;       /* azul profundo: fondos al pasar el cursor */
  --blue-mid: #2E5A88;   /* azul de los efectos y sombras */
  --blue-soft: #6E9BC4;  /* azul claro sobre fondo oscuro */
  --black: #111111;
  --border: #E0DDD8;
  --ink: #0B0E14;      /* fondo de la portada */
}
```

**Regla del azul:** en reposo el sitio es dorado sobre blanco, sin una sola
traza de azul. El azul aparece únicamente mientras el cursor está encima de
algo o un campo tiene el foco — sombras, filetes de 2 px, el ícono del curso,
el anillo del buscador. Nunca se ven los dos colores a la vez.

Todas esas reglas están agrupadas al final de `theme.css` bajo el comentario
`AZUL — únicamente en interacción`. Cambiar `--blue-mid` cambia todos los
efectos de una vez; borrar ese bloque deja el sitio íntegramente dorado.

---

## La portada

Ocupa el alto de la pantalla. La cabecera está fija y visible desde el
principio, igual que en el resto de páginas.

**Rótulos.** El titular es el logotipo dibujado en dorado y debajo va
"Dr. Andreé Salvatierra". El antetítulo dice solo "Biblioteca abierta de apuntes".

**Fondo de color entero.** Sin foto, sin vídeo, sin degradados: un solo color
plano, `--ink: #0B0E14`, un tinta muy oscuro con sesgo azul que hace de puente
entre el dorado y el azul del tema.

**Las neuronas.** A cada lado hay un grupo de neuronas en WebP con transparencia
(`img/neuronas-a.webp` y `img/neuronas-b.webp`), al 52 % y 46 % de opacidad.
Entran con un fundido escalonado al cargar y no se mueven más. Están sangradas
—se salen un poco por los bordes— para que no parezcan pegatinas centradas.

| Archivo | Contenido | Medidas |
|---|---|---|
| `neuronas-a.webp` | Neurona azul + dorada | 334 × 462 · 63 KB |
| `neuronas-b.webp` | Neurona dorada + azul | 393 × 380 · 64 KB |

Se muestran casi a tamaño original (máximo 360 y 400 px de ancho), así que no
hay reescalado que las emborrone.

### Ajustes rápidos

```css
--ink: #0B0E14;                    /* color de fondo, en :root */
@keyframes neuronaIn  { ... to { opacity: 0.52; } }   /* neurona izquierda */
@keyframes neuronaInB { ... to { opacity: 0.46; } }   /* neurona derecha */
.hero-neurona.izq { left: -3vw; width: clamp(220px, 26vw, 360px); }
```

Subir las opacidades hace las neuronas más presentes; bajarlas, casi invisibles.

### Cambiar las neuronas

Los archivos salieron de una lámina con seis recortes. Cada recorte traía un
halo rectangular grisáceo que había que eliminar; el proceso fue:

1. **Máscara por luminancia** — se descarta todo lo que brille por debajo del
   26 % y se hace transición suave hasta el 50 %. Eso borra la neblina de fondo
   y conserva las neuronas.
2. **Desvanecido radial** — una elipse suave difumina los bordes para que el
   rectángulo del recorte desaparezca del todo.
3. **WebP con alfa** — cinco veces más ligero que PNG con la misma calidad.

Si cambias las imágenes, lo único que importa es que lleguen con fondo
transparente y bordes desvanecidos; si no, se verá el recuadro.

---

## El logotipo

La palabra **Neurona** es texto de verdad, escrito con la tipografía caligráfica
**Miracle History**. Nada de trazados ni de SVG: es un `<span>` con una clase.

```html
<span class="marca-neurona site-logo-marca">Neurona</span>
```

**La fuente va recortada.** `fonts/neurona.woff2` contiene solo los glifos de
esas siete letras, así que pesa **3,9 KB** en vez de los 97 KB del `.ttf`
completo. Se declara una vez en `theme.css`:

```css
@font-face {
  font-family: 'Miracle History';
  src: url('../fonts/neurona.woff2') format('woff2');
  font-display: swap;
}
```

Si el archivo fallara, `font-display: swap` deja Cormorant Garamond como
respaldo y la página sigue leyéndose.

### Tamaño y posición

Al ser texto, se controla con `font-size` y con márgenes normales. Los tres
sitios donde aparece:

```css
.site-logo-marca   { font-size: 47px;  }              /* encabezado */
.library-hero-name { font-size: clamp(72px, 12vw, 176px); }  /* portada */
.footer-marca      { font-size: 54px;  }              /* pie */
.marca-neurona     { line-height: 0.86; }             /* aprieta la caja */
```

`line-height: 0.86` es lo que quita el aire que la fuente reserva por encima de
las letras. Para subir o bajar el logotipo se toca el `margin` de cada uno; para
agrandarlo, el `font-size`.

### Regenerar la fuente recortada

```python
from fontTools import subset
from fontTools.ttLib import TTFont
f = TTFont("Miracle History.ttf")
s = subset.Subsetter(options=subset.Options(layout_features=["liga","kern","calt","rlig"]))
s.populate(text="Neurona ")
s.subset(f)
f.flavor = "woff2"
f.save("neurona.woff2")
```

El `.ttf` original está guardado un nivel arriba, junto a `build.py`.

> **Licencia.** Miracle History (fikryalstudio.com) es de uso personal. Este
> sitio es un repositorio académico gratuito y sin ánimo de lucro, así que
> encaja, pero si algún día se le da un uso comercial hay que comprar la
> licencia. Ten en cuenta que publicar la fuente en la web la deja descargable,
> aunque el subconjunto solo sirva para escribir "Neurona".

### La marca de agua de los PDF

El sello de los apuntes usa `marca-negro.png`, un PNG de la misma palabra
generado aparte. Si cambias el logotipo y quieres que los PDF vayan a juego,
regenera ese PNG y vuelve a ejecutar `proteger.py`:

```python
from PIL import Image, ImageDraw, ImageFont
f = ImageFont.truetype("Miracle History.ttf", 400)
c = f.getbbox("Neurona")
im = Image.new("RGBA", (c[2]-c[0]+20, c[3]-c[1]+20), (0,0,0,0))
ImageDraw.Draw(im).text((10-c[0], 10-c[1]), "Neurona", font=f, fill=(0,0,0,255))
im.save("marca-negro.png")
```

---

## Sobre el autor

La sección se armó con el PPT del CV: el retrato, la trayectoria y los escudos
salieron de ahí.

**Escudos.** Diez instituciones en dos grupos: *Formación*, en orden
cronológico —pregrado, especialidad, los dos másteres, doctorado y
posdoctorado—, y *Estancias e investigación*. Están en `img/escudos/` en WebP
con fondo transparente; se muestran en gris al 60 % y recuperan su color al
pasar el cursor, para que la rejilla no se convierta en una feria de logos.

Las rejillas **no llevan recuadro**: entre una institución y la siguiente hay
solo una línea vertical corta y centrada, nunca de borde a borde. Se dibuja con
`.escudo::before` y se oculta en el primer elemento de cada fila con
`:nth-child(6n+1)` en Formación y `:nth-child(4n+1)` en Estancias. Si cambias el
número de columnas hay que ajustar esos múltiplos, o volverán a aparecer líneas
al principio de fila.

Los escudos están escritos como HTML en `build.py`, dentro de la sección
`<div class="escudos">`; añadir uno es copiar el WebP y duplicar un `<figure>`.

**Botones de perfil.** Cinco enlaces —LinkedIn, ResearchGate, CTI Vitae, ORCID y
Google Scholar— con iconos dibujados a un solo trazo, en el mismo lenguaje que el
resto del sitio. Todos abren en pestaña nueva con `rel="noopener"`. Están en la
lista `PERFILES` de `build.py`, junto a los iconos.

**Datos de contacto.** El correo es `4andree4@gmail.com` y los registros
profesionales (CPsP, RNE, RENACYT) van bajo la biografía.

> El retrato y los escudos proceden del PPT que hizo Andreé. Los logotipos
> institucionales son marcas de sus respectivas universidades y se usan aquí de
> forma descriptiva, para señalar dónde estudió y trabajó.

---

## Noticias

### Lo que LinkedIn no permite

Empiezo por lo importante: **LinkedIn no deja sacar automáticamente las
publicaciones de un perfil personal.** No hay RSS, la API pública no expone el
muro de una persona —solo páginas de empresa, y con permisos aprobados— y raspar
el sitio va contra sus condiciones y está bloqueado técnicamente. Cualquiera que
prometa lo contrario está describiendo algo que se rompe a las pocas semanas.

Así que la sección funciona con dos fuentes que sí son fiables:

### 1. Entradas escritas a mano (`noticias.json`)

Es un archivo de texto sencillo. Cada entrada tiene fecha, etiqueta, título,
texto y un enlace opcional:

```json
{
  "fecha": "2026-09-12",
  "etiqueta": "Congreso",
  "titulo": "Ponencia en el Congreso Peruano de Neurología",
  "texto": "Presentación sobre marcadores cognitivos tempranos.",
  "enlace": "https://…"
}
```

Las nuevas van **arriba del todo**. La página las ordena por fecha de todos
modos, pero así se trabaja más cómodo.

**No hay que ejecutar nada.** La web lee el archivo en el navegador, de forma que
editarlo desde GitHub —se puede hacer desde el móvil, con el lápiz de la interfaz
web— actualiza el sitio en cuanto se guarda.

En la portada **no se lista nada**: al final de *Sobre el autor* hay solo un
botón que dice «Noticias» y lleva a la página completa. **Tampoco aparece en el
menú superior**, a propósito.

### 2. Botón a LinkedIn

Al lado de las entradas hay un botón que lleva a su perfil. Es lo más cerca que
se puede estar de "seguir su actividad" sin inventar una integración que no
existe.

> **Nota para pruebas locales.** Como las entradas se cargan con `fetch`, abrir
> `index.html` con doble clic no las mostrará: el navegador bloquea la lectura de
> archivos locales. Para verlo en el ordenador, desde la carpeta del sitio:
> `python3 -m http.server` y abrir `http://localhost:8000`. En GitHub Pages
> funciona sin más.

---

## El menú

Cuatro pestañas y nada más:

| Pestaña | Qué es |
|---|---|
| **Inicio** | Logotipo, nombre y la sección del autor. Nada de cursos. |
| **Materiales de clase** | Desplegable con los cuatro cursos; la pestaña en sí lleva a una página con las cuatro tarjetas. |
| **Investigación** | Publicaciones, tesis dirigidas, conferencias y distinciones, tomadas del CV. |
| **Noticias** | Lo que se escribe a mano en `noticias.json`. |
| **Contacto** | Página propia: teléfono, correo, perfiles y formulario, todo a la vista. |

El desplegable se abre al pasar el cursor y también con el teclado
(`:focus-within`), así que funciona sin ratón. La pestaña queda marcada como
activa tanto en la página de materiales como dentro de cualquier curso.

Para añadir o cambiar entradas del menú se edita `NAV_ITEMS` en `build.py`. Cada
entrada es `(archivo, etiqueta, hijos)`; si `hijos` es `None`, es un enlace
normal; si es una lista, se convierte en desplegable.

### De dónde salen los datos

Todo el contenido de *Sobre el autor* e *Investigación* viene del CV real
(`CV_Andreé Salvatierra.docx`): la biografía, la formación con sus años, las
estancias, la docencia de pregrado y posgrado, las publicaciones, las tesis
dirigidas, las conferencias y las distinciones. Si el CV cambia, se actualizan
las listas correspondientes en `build.py` y se vuelve a ejecutar.

### Investigación y Noticias son cosas distintas

- **Investigación** = artículos y producción científica, tomados del CV: 12
  publicaciones con su DOI, 3 tesis dirigidas, 11 conferencias magistrales y las
  distinciones. Están en `build.py` como listas (`PUBLICACIONES`, `TESIS`,
  `CONFERENCIAS`, `DISTINCIONES`); para añadir una, se copia la línea de arriba
  y se ejecuta `python3 build.py`.
- **Noticias** = congresos, premios, docencia, colaboraciones. Eso se escribe a
  mano en `noticias.json`, que es lo que se sincronizaría con LinkedIn si
  LinkedIn lo permitiera —y no lo permite, ver más arriba.

---

## El bloque de contacto

Al final de Inicio hay un **Contáctame** plegado. Se abre hacia abajo al pulsarlo
y trae los datos de contacto a la izquierda y un formulario a la derecha. Está
hecho con `<details>`/`<summary>`, así que funciona sin JavaScript: si el
navegador tuviera los scripts desactivados, el bloque se sigue abriendo.

La pestaña **Contacto** del menú apunta a `index.html#contactame`; un pequeño
script detecta ese ancla y abre el bloque solo, incluso si vienes desde otra
página.

### El formulario y el correo

Aquí hay un límite del que conviene ser consciente: **un sitio estático no puede
procesar formularios**. No hay servidor que reciba nada. Así que el botón
*Enviar* compone un correo con lo que se ha escrito y abre el programa de correo
del visitante con el mensaje ya redactado, dirigido a `4andree4@gmail.com`.

Ventaja: funciona desde el primer día, sin registrarse en ningún sitio y sin que
los mensajes pasen por terceros. Inconveniente: el visitante ve abrirse su
cliente de correo, y si usa webmail sin configurar puede resultarle raro.

Si algún día se prefiere que el mensaje llegue sin abrir el cliente de correo,
basta con darse de alta en un servicio gratuito como Formspree y cambiar el
formulario por:

```html
<form action="https://formspree.io/f/TU_CODIGO" method="POST">
```

…quitando el `<script>` que hay debajo. El resto del diseño no cambia.

---

## Notas técnicas

- Sin frameworks ni build de verdad. `build.py` solo concatena plantillas de texto.
- El buscador del catálogo es JavaScript plano e ignora tildes.
- Responsive hasta 360 px. En móvil el menú superior se oculta.
- Tipografía y paleta compartidas con el sitio de física; los elementos propios son
  el logotipo dibujado y el icono de neurona del encabezado.

---

© 2026 Dr. Andreé Salvatierra · Apuntes de libre distribución con atribución


---

## Lo último que se cambió

**Investigación se escribe desde el CV, no desde ORCID.** Antes la página tiraba
de la API pública de ORCID. La quité: la lista del CV está completa, tiene la
cita entera y el DOI de cada artículo, y no depende de que un servicio externo
responda. Se puede volver atrás si algún día interesa, pero entonces la página
mostraría menos de lo que muestra ahora. Lo que hay:

| Bloque | Cuántos |
|---|---|
| Publicaciones (con DOI cuando lo tienen) | 12 |
| Tesis dirigidas | 3 |
| Conferencias magistrales | 11 |
| Distinciones | 4 |

**Sobre el autor** lleva la biografía del CV, los escudos de formación y los de
las cuatro estancias de investigación.

**Contáctame** es ahora un desplegable de verdad, con su antetítulo, su título
grande y un `+` dorado que gira hasta convertirse en `×` al abrirse. Dentro:
teléfono, correo, LinkedIn, ORCID y los registros académicos.

**El punto que sobraba** en Materiales de clase era el ornamento `§` bajo el
título. Fuera.


---

## Cambios de esta ronda

**Nueve apuntes más.** Del 7 al 15: farmacolómica, respuesta clínica, desarrollo
de medicamentos, bioequivalentes y biosimilares, factores modificadores,
neurotransmisores, ansiolíticos, antidepresivos y antipsicóticos. Ya son 15
apuntes y 715 páginas, todas marcadas y cifradas igual que las anteriores. El
temario pasó de cuatro unidades a ocho.

**Los escudos, solo escudos.** Fuera el grado y los años bajo cada logo: se
entiende con el escudo. Y a color desde que carga la página, no en gris
esperando el cursor.

**Contacto es una pestaña de verdad.** Antes era un ancla que bajaba al final de
Inicio y abría un desplegable. Ahora `contacto.html` es una página como las
demás, con todo visible al entrar: teléfono, correo, LinkedIn, ORCID, registros
y el formulario.


**Fuera la docencia de la portada.** Las dos tablas de cursos (pregrado y
posgrado) se quitaron: la portada tiene que quedar corta. Los datos siguen en
`build.py`, en las listas `DOCENCIA_PRE` y `DOCENCIA_POS`, por si algún día se
quieren en otra página.

**El desplegable de Contáctame vuelve al final de Inicio.** Convive con la
pestaña: en Inicio es un bloque que se abre al pulsarlo, y `contacto.html` sigue
siendo la página con todo a la vista. La pestaña del menú lleva a la página.


---

## Noticias: las publicaciones de LinkedIn

Las cinco entradas de `noticias.json` son las publicaciones reales de su perfil,
pasadas a mano al archivo. Cada una guarda:

| Campo | Qué es |
|---|---|
| `fecha` | La fecha exacta del post, en AAAA-MM-DD |
| `etiqueta` | Formación, Congreso, Reconocimiento, Docencia… |
| `titulo` | Un titular corto, escrito a partir del post |
| `texto` | El texto del post, sin los `hashtag#` ni el «… más» |
| `temas` | Los hashtags, escritos como se leen |
| `imagen` + `alt` | El cartel, en `img/noticias/` |
| `video` + `poster` | Para la entrada que llevaba vídeo |
| `enlace` | El post original en LinkedIn |

Las fechas no son las relativas («hace 3 meses») que muestra LinkedIn: salen del
identificador del propio post, que lleva dentro la marca de tiempo. Por eso son
exactas.

**Media.** Los cuatro carteles se pasaron a WebP (10–130 KB cada uno). El vídeo
de la exposición de maquetas —112 segundos— se reencodó a MP4 de 640 px y pesa
8 MB; es el archivo más grande del sitio después de los apuntes. Se carga con
`preload="none"`, así que solo baja si alguien le da al play.

**Añadir una entrada nueva.** Se copia el bloque de arriba del todo en
`noticias.json`, se cambian los campos y se guarda. Si lleva imagen, se deja en
`img/noticias/` y se apunta la ruta. No hay que ejecutar `build.py`: la página
lee el JSON en el navegador.
