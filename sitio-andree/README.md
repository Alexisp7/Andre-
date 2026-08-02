# Neurona — Dr. Andreé Salvatierra

Sitio estático con los apuntes de clase de cuatro cursos: **Biopsicología**,
**Neuroanatomía**, **Neuropsicología** y **Psicofarmacología**.
Sin build, sin dependencias: HTML + un CSS. Se publica tal cual en GitHub Pages.

**Estado actual:** 6 apuntes publicados, todos en Psicofarmacología. Los otros
tres cursos tienen temario provisional y ningún PDF todavía.

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

> Los PDFs pesan ~10 MB en total. Está dentro de lo que GitHub admite sin problema.

---

## Estructura

```
.
├── index.html                 Portada
├── biopsicologia.html         Temario provisional
├── neuroanatomia.html         Temario provisional
├── neuropsicologia.html       Temario provisional
├── psicofarmacologia.html     Temario + 6 apuntes
├── apuntes.html               Catálogo con buscador y filtros
├── css/theme.css              Todo el estilo (un solo archivo)
├── img/                       Neuronas de la portada
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

1. Copia el PDF a `apuntes/<curso>/` con un nombre en minúsculas y sin tildes.
2. En `build.py`, busca el curso y la unidad, y cambia el `None` por el nombre del archivo
   (o añade una tupla nueva).
3. Ejecuta `python3 build.py` desde la carpeta que contiene el script.

Las páginas se regeneran solas: portada, página del curso, catálogo y sus filtros.
Los contadores ("4 apuntes", "93 pág.") se calculan a partir de los datos, no hay que
tocarlos. Añadir o quitar un curso de la lista `CURSOS` crea o borra su página, su
tarjeta en la portada, su pestaña y su filtro en el catálogo.

Si solo quieres **reemplazar** un PDF por una versión corregida, sobrescribe el archivo
conservando el mismo nombre. No hay que regenerar nada.

### Cambiar el temario

Los temarios de Biopsicología, Neuroanatomía y Neuropsicología son provisionales — los
escribí a partir del contenido estándar de esos cursos, no del programa real de Andreé.
Cámbialos en `build.py` (listas `unidades`) y vuelve a ejecutarlo.

### Los seis PDFs

Los seis apuntes viven en Psicofarmacología, repartidos en cuatro unidades:
introducción, bases celulares y moleculares, farmacocinética y farmacodinamia.
Es el orden en que venían numerados en el original.

---

## Editar textos

- **Logotipo** — es un dibujo en SVG, no texto. Ver la sección *El logotipo* más abajo.
- **Subtítulo del encabezado** — en `build.py`, función `header()`.
- **Antetítulo de la portada** — en `build.py`, función `build_index()`.
- **Correo y enlaces académicos** — en `build.py`, constante `FOOTER`. Ahora dicen
  `correo@ejemplo.com` y `#`.
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

La palabra **Neurona** no es texto: es un dibujo vectorial. Partí de las formas de
una serif itálica, las convertí a trazados y les añadí a mano el rasgo que subraya
la palabra, con grosor variable —grueso en el centro, afilado en las puntas—.

Ventajas de que sea un dibujo y no una fuente: se ve idéntico en cualquier
dispositivo, no parpadea mientras carga la tipografía, y escala sin perder nitidez.

**Cómo está montado.** El trazado se define una sola vez por página, dentro de un
`<symbol id="marcaNeurona">` justo después de `<body>`. Los tres sitios donde
aparece —encabezado, portada y pie— lo referencian con `<use href="#marcaNeurona"/>`.
Así el dibujo pesa una vez y no tres.

**Color.** Los trazados usan `fill="currentColor"`, así que el logotipo toma el color
del contenedor. En `theme.css`:

```css
.site-logo-marca { color: var(--black); width: 128px; }   /* encabezado */
.library-hero-name { color: var(--gold); }                /* portada */
.footer-marca { color: var(--gold); width: 150px; }       /* pie */
```

Para cambiar el tamaño se toca solo el `width`; la altura se ajusta sola.

**Regenerarlo.** El trazado se generó con `fontTools` a partir de Lora Italic en peso
600, escalando a 200 px de altura de em, y luego se le añadió el rasgo a mano. Si
alguna vez hay que rehacerlo, está incrustado en `build.py` como `WORDMARK_DEFS`.

---

## Notas técnicas

- Sin frameworks ni build de verdad. `build.py` solo concatena plantillas de texto.
- El buscador del catálogo es JavaScript plano e ignora tildes.
- Responsive hasta 360 px. En móvil el menú superior se oculta.
- Tipografía y paleta compartidas con el sitio de física; los elementos propios son
  el logotipo dibujado y el icono de neurona del encabezado.

---

© 2026 Dr. Andreé Salvatierra · Apuntes de libre distribución con atribución
