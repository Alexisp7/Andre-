/* Navegación SPA entre las páginas con franja de video: intercepta los
   clics en enlaces internos, trae la página siguiente por fetch() y
   reemplaza solo el texto de la franja (.page-hero-inner) y el
   contenido de abajo (#spaMain) — el menú y el propio <video> de
   fondo nunca se tocan, así que jamás se recargan ni reinician: el
   video sigue reproduciéndose sin cortes de una "página" a la
   siguiente.

   La portada (index.html) usa la MISMA sección .page-hero que las
   demás páginas, solo que con el modificador .page-hero--portada
   (pantalla completa en vez de franja) — así que el mismo <video>,
   nunca destruido, sirve para ambos casos: al navegar hacia o desde
   la portada simplemente se agrega/quita esa clase, y como el video
   queda anclado abajo y la sección tiene overflow:hidden, la
   transición de altura por CSS hace que se vea como si el video
   "subiera" (se encoge hasta la franja) o "bajara" (vuelve a pantalla
   completa) — es el mismo elemento, solo más o menos recortado.

   visor.html también entra: su cabecera ahora es la misma franja
   .page-hero. Su propio script (pdf.js) se desmonta y se vuelve a
   montar solo en cada visita (ver el desmontaje al principio de ese
   script en visor.html) para no ir acumulando listeners globales al
   ver varios apuntes seguidos sin recargar la página real.

   Si algo no cuadra (fetch falla, la página no tiene la estructura
   esperada, JS deshabilitado), todo cae de vuelta a una navegación
   real — nunca deja al sitio en un estado roto. */
(function () {
  'use strict';

  var PAGINAS = [
    'index.html', 'materiales.html', 'investigacion.html', 'noticias.html',
    'apuntes.html', 'contacto.html', 'biopsicologia.html', 'neuroanatomia.html',
    'neuropsicologia.html', 'psicofarmacologia.html', 'visor.html'
  ];

  // Qué pestaña(s) del menú marcar como activa para cada página.
  var ACTIVOS = {
    'index.html': { inicio: true },
    'materiales.html': { cursos: true },
    'psicofarmacologia.html': { subActiva: true },
    'investigacion.html': { investigacion: true },
    'noticias.html': { noticias: true },
    'biopsicologia.html': { subActiva: true },
    'neuroanatomia.html': { cursos: true },
    'neuropsicologia.html': { cursos: true },
    'visor.html': { cursos: true }
  };

  var HERO_SEL = '.page-hero-inner';
  var MAIN_SEL = '#spaMain';
  var DURACION_SALIDA = 200; // ms — debe calzar con .spa-hero-sale en theme.css

  function archivoDe(url) {
    var partes = url.pathname.split('/');
    return partes[partes.length - 1] || 'index.html';
  }

  function esElegible(archivo) {
    return PAGINAS.indexOf(archivo) !== -1;
  }

  function irReal(href) {
    location.href = href;
  }

  function actualizarNav(archivo) {
    var nav = document.getElementById('heroNavFlotante');
    if (!nav) return;
    var enlaces = nav.querySelectorAll('a');
    enlaces.forEach(function (a) { a.classList.remove('active', 'sub-activa'); });

    var cfg = ACTIVOS[archivo] || {};
    var mapa = {
      inicio: 'a[href="index.html"]',
      cursos: 'a[href="materiales.html"]',
      investigacion: 'a[href="investigacion.html"]',
      noticias: 'a[href="noticias.html"]'
    };
    Object.keys(mapa).forEach(function (clave) {
      if (!cfg[clave]) return;
      var a = nav.querySelector(mapa[clave]);
      if (a) a.classList.add('active');
    });
    if (cfg.subActiva) {
      var sub = nav.querySelector('.nav-submenu a[href="' + archivo + '"]');
      if (sub) sub.classList.add('sub-activa');
    }
  }

  /* Los <script> insertados vía innerHTML no se ejecutan solos — hay
     que reemplazar cada uno por un elemento <script> recién creado
     para que el navegador sí los corra (misma técnica que usan pjax y
     turbo). Un <script src="..."> creado así, por defecto, el
     navegador lo trata como si tuviera "async": se ejecuta en cuanto
     termina de descargar, sin esperar su turno — así que si depués
     viene un <script> propio que asume que la librería externa ya
     cargó (como pdf.js en visor.html), puede correr primero y
     encontrarla todavía sin definir. async=false antes de insertarlo
     hace que el navegador respete el orden del documento, igual que
     con un <script> normal del HTML original. */
  function ejecutarScripts(contenedor) {
    var scripts = contenedor.querySelectorAll('script');
    scripts.forEach(function (viejo) {
      var nuevo = document.createElement('script');
      nuevo.async = false;
      for (var i = 0; i < viejo.attributes.length; i++) {
        nuevo.setAttribute(viejo.attributes[i].name, viejo.attributes[i].value);
      }
      nuevo.textContent = viejo.textContent;
      viejo.parentNode.replaceChild(nuevo, viejo);
    });
  }

  /* Quita la clase de la animación de entrada en cuanto termina de
     jugar, en vez de dejarla puesta para siempre. Con fill-mode
     "both" el navegador mantiene fijo el transform del último
     fotograma incluso después de terminar — y aunque ese transform
     sea "sin mover nada" (translateY(0)), su valor calculado sigue
     siendo una matriz, no la palabra "none": eso convierte al
     elemento en el "containing block" de cualquier descendiente
     position:fixed suyo (como los controles del visor en pantalla
     completa simulada), que dejan de anclarse a la pantalla real y
     pasan a anclarse a este elemento en su lugar. Sacando la clase
     una vez terminada la animación, el elemento vuelve a quedar sin
     transform de ningún tipo. */
  function reiniciarAnimacion(el, clase) {
    el.classList.remove(clase);
    void el.offsetWidth; // fuerza reflow para reiniciar la animación
    el.classList.add(clase);
    el.addEventListener('animationend', function fin(e) {
      if (e.target !== el) return;
      el.classList.remove(clase);
      el.removeEventListener('animationend', fin);
    });
  }

  function moverFoco(heroActual) {
    var titulo = heroActual.querySelector('.page-hero-title') || heroActual.querySelector('.library-hero-name') || heroActual.querySelector('.visor-titulo');
    if (!titulo) return;
    if (!titulo.hasAttribute('tabindex')) titulo.setAttribute('tabindex', '-1');
    titulo.focus({ preventScroll: true });
  }

  var generacion = 0;

  function navegar(url, conHistoria) {
    var miGeneracion = ++generacion;
    var archivo = archivoDe(url);
    var esPortada = archivo === 'index.html';

    var heroActual = document.querySelector(HERO_SEL);
    var mainActual = document.querySelector(MAIN_SEL);
    if (!heroActual || !mainActual) { irReal(url.href); return; }

    var heroSeccion = heroActual.closest('.page-hero');

    fetch(url.href, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    }).then(function (html) {
      if (miGeneracion !== generacion) return; // otra navegación llegó primero

      var doc = new DOMParser().parseFromString(html, 'text/html');
      var nuevoHero = doc.querySelector(HERO_SEL);
      var nuevoMain = doc.querySelector(MAIN_SEL);
      if (!nuevoHero || !nuevoMain) { irReal(url.href); return; }

      if (conHistoria) history.pushState({ spa: true }, '', url.href);
      document.title = doc.title;
      window.scrollTo(0, 0);

      heroActual.classList.remove('spa-hero-entra');
      heroActual.classList.add('spa-hero-sale');

      setTimeout(function () {
        if (miGeneracion !== generacion) return;

        /* El <video> de fondo vive en la sección .page-hero de afuera,
           que nunca se toca ni se destruye — solo se le agrega o quita
           el modificador de portada, y eso es lo que anima su altura
           ("sube"/"baja"). Se hace justo AQUÍ, recién con el texto
           viejo ya invisible (terminó .spa-hero-sale), no al hacer
           clic: .page-hero--portada también centra y angosta
           .page-hero-inner, así que cambiarlo antes hacía que el
           título todavía visible saltara al centro y se quedara ahí
           un instante antes de desvanecerse — se veía mal. */
        if (heroSeccion) {
          heroSeccion.classList.toggle('page-hero--portada', esPortada);
          if (esPortada) {
            /* Al ENTRAR a la portada, .page-hero--fijo (position:fixed
               para el video/velo, ver theme.css) se agrega recién
               cuando la transición de altura (230px -> 100vh) termina
               de verdad, no junto con --portada: si se agregara de
               una, el video saltaría de golpe a pantalla completa
               mientras la caja recién arranca a crecer, en vez de
               verse crecer con ella. transitionend es lo normal; el
               setTimeout es solo una red de seguridad por si no
               llegara a disparar (pestaña en segundo plano, etc). Al
               SALIR no hace falta ninguno de los dos: ahí la caja
               arranca ya en 100vh (recién se achica después), así que
               sacar --fijo junto con --portada no da ningún salto. */
            var miGen = miGeneracion;
            var fijado = false;
            var fijar = function () {
              if (fijado || miGen !== generacion) return;
              fijado = true;
              heroSeccion.classList.add('page-hero--fijo');
            };
            heroSeccion.addEventListener('transitionend', function alFinCrecer(e) {
              if (e.target !== heroSeccion || e.propertyName !== 'height') return;
              heroSeccion.removeEventListener('transitionend', alFinCrecer);
              fijar();
            });
            setTimeout(fijar, 700);
          } else {
            heroSeccion.classList.remove('page-hero--fijo');
          }
        }
        if (window.__sincronizarConstelacion) window.__sincronizarConstelacion();

        heroActual.innerHTML = nuevoHero.innerHTML;
        mainActual.innerHTML = nuevoMain.innerHTML;
        ejecutarScripts(heroActual);
        ejecutarScripts(mainActual);
        actualizarNav(archivo);
        moverFoco(heroActual);

        heroActual.classList.remove('spa-hero-sale');
        reiniciarAnimacion(heroActual, 'spa-hero-entra');
        reiniciarAnimacion(mainActual, 'spa-main-entra');
      }, DURACION_SALIDA);
    }).catch(function () {
      irReal(url.href);
    });
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    if (a.target && a.target !== '_self') return;
    if (a.hasAttribute('download')) return;

    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin) return;

    var archivo = archivoDe(url);
    if (!esElegible(archivo)) return; // p.ej. visor.html: navegación real

    var actual = archivoDe(new URL(location.href));
    if (archivo === actual && url.hash === location.hash) return; // ya estamos aquí

    e.preventDefault();
    navegar(url, true);
  });

  window.addEventListener('popstate', function () {
    var url = new URL(location.href);
    if (!esElegible(archivoDe(url))) return;
    navegar(url, false);
  });

  /* El nav flotante se desvanece con el scroll SOLO mientras la franja
     de arriba está en modo portada (pantalla completa) — en las demás
     páginas, angostas, se queda siempre visible. Esto vive acá (y no
     en un <script> propio de index.html) porque la sección .page-hero
     es persistente entre navegaciones SPA: si el usuario entra al
     sitio por cualquier página que no sea index.html y luego navega a
     "Inicio", ese <script> de index.html nunca se volvería a ejecutar
     (queda fuera de .page-hero-inner y #spaMain, las únicas zonas que
     se reemplazan) — así que el desvanecido tiene que quedar
     conectado una sola vez, acá, de forma global. */
  var heroNavGlobal = document.getElementById('heroNavFlotante');
  var heroSeccionGlobal = document.querySelector('.page-hero');
  if (heroNavGlobal && heroSeccionGlobal) {
    var desvaneciendo = false;
    function actualizarDesvanecido() {
      desvaneciendo = false;
      if (!heroSeccionGlobal.classList.contains('page-hero--portada')) {
        heroNavGlobal.style.opacity = '';
        heroNavGlobal.style.pointerEvents = '';
        heroSeccionGlobal.style.removeProperty('--progreso-salida');
        heroSeccionGlobal.style.removeProperty('--blur-fondo');
        return;
      }
      /* En escritorio el título queda fijo (position:fixed, ver
         theme.css min-width:901px) mientras dura el recorrido de sobra
         de #tituloDwell — el desvanecido tiene que llegar a 1 justo al
         completar ESE recorrido (alto propio de .page-hero, 100vh, más
         el de #tituloDwell), no antes ni después. .page-hero se queda
         siempre en 100vh (ver el porqué en theme.css) — no restarle acá
         el alto de ventana como si estuviera agrandado. En mobile no
         existe #tituloDwell (el título nunca queda fijo ahí) así que
         se sigue usando el alto entero de la propia caja. */
      var esEscritorio = window.innerWidth >= 901;
      var tituloDwellEl = document.getElementById('tituloDwell');
      var alto = esEscritorio
        ? Math.max(1, heroSeccionGlobal.offsetHeight + (tituloDwellEl ? tituloDwellEl.offsetHeight : 0))
        : (heroSeccionGlobal.offsetHeight || 1);
      var progreso = Math.min(1, Math.max(0, window.scrollY / alto));
      heroNavGlobal.style.opacity = String(1 - progreso);
      heroNavGlobal.style.pointerEvents = progreso > 0.85 ? 'none' : 'auto';
      /* Mismo progreso (0 a 1, ya medido para desvanecer el nav) para que
         el título de la portada se vaya desvaneciendo/desenfocando a
         medida que se hace scroll, con un ligero zoom del vídeo de
         fondo — todo por CSS (ver .page-hero--portada en theme.css), acá
         solo se pone el número. */
      heroSeccionGlobal.style.setProperty('--progreso-salida', String(progreso));
      /* El desenfoque se queda cerca de 0 mientras se está todavía
         dentro del propio alto del título (sea 100vh en mobile o los
         240vh de recorrido que tiene en escritorio como "diapositiva")
         y recién ahí empieza a crecer, alcanzando el máximo (16px) 1.2
         pantallas después — así el título se ve nítido durante todo su
         propio tramo, y el fondo se termina de desenfocar rápido apenas
         se entra al contenido, sin importar cuánto dure el tramo del
         título. Nunca llega a bloque plano: el video siempre se tiene
         que seguir reconociendo. */
      var progresoBlur = Math.min(1, Math.max(0, (window.scrollY - alto) / (window.innerHeight * 1.2)));
      heroSeccionGlobal.style.setProperty('--blur-fondo', (progresoBlur * 16).toFixed(2) + 'px');
      sincronizarDiapositivas();
    }
    /* Cada .slide-wrap (y el propio título) es más alto que la pantalla
       a propósito: mientras se scrollea por ese "recorrido" extra,
       queda fijo en pantalla (position:sticky, ver theme.css) y esto
       mide cuánto de ese recorrido ya se hizo, 0 a 1 — con eso, cada
       elemento [data-reveal] de adentro arma su propia entrada por CSS
       (ver .slide-pin [data-reveal] en theme.css). Solo aplica en
       escritorio: en mobile se pidió dejar el flujo normal de siempre,
       sin diapositivas ni fijado (min-width:901px, igual que en el
       CSS). Se vuelve a consultar el DOM en cada llamada en vez de
       guardar una lista una sola vez porque #spaMain se reemplaza
       entero en cada navegación por SPA. */
    function sincronizarDiapositivas() {
      if (window.innerWidth < 901) return;
      var wraps = document.querySelectorAll('.slide-wrap');
      for (var i = 0; i < wraps.length; i++) {
        var wrap = wraps[i];
        var alto = wrap.offsetHeight - window.innerHeight;
        var progreso = alto > 0 ? Math.min(1, Math.max(0, -wrap.getBoundingClientRect().top / alto)) : 1;
        wrap.style.setProperty('--slide-progreso', String(progreso));
      }
    }
    function pedirDesvanecido() {
      if (desvaneciendo) return;
      desvaneciendo = true;
      requestAnimationFrame(actualizarDesvanecido);
    }
    actualizarDesvanecido();
    window.addEventListener('scroll', pedirDesvanecido, { passive: true });
    window.addEventListener('resize', pedirDesvanecido);
  }

  /* Red de puntos tipo constelación, de fondo detrás del título de la
     portada (ver .hero-constelacion en theme.css): nodos en grilla que
     se apartan del mouse con un resorte (Hooke) y vuelven solos a su
     sitio, con líneas finas entre los que quedan cerca. Solo corre
     mientras la portada esté activa — se arranca/para desde navegar()
     al entrar o salir de ella, y una sola vez acá para la primera
     carga real si esta ya es la portada. */
  var canvasConstelacion = document.getElementById('heroConstelacion');
  if (canvasConstelacion && heroSeccionGlobal) {
    var ctxConstelacion = canvasConstelacion.getContext('2d', { alpha: true });
    var nodosConstelacion = [];
    var anchoConstelacion = 0;
    var altoConstelacion = 0;
    var rafConstelacion = null;
    var ultimoTiempo = 0;
    var mouseConstelacion = { x: -1000, y: -1000 };
    var reducidoConstelacion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function medirConstelacion() {
      /* Se mide el propio <canvas> (clientWidth/Height, su tamaño real
         ya renderizado), no heroSeccionGlobal ni el viewport: .page-hero
         anima su alto con transition (0.6s) al entrar/salir de la
         portada, y el tamaño en pantalla del canvas (height:100% de esa
         sección) va cambiando cuadro a cuadro mientras dura. Leer una
         sola vez, al togglear la clase, agarraba un valor a medio
         camino de esa animación — el buffer quedaba fijo con ese alto
         viejo mientras CSS seguía estirando el elemento hasta el alto
         final: los puntos salían ovalados, y con los nodos apretados en
         esa franja chica pero el mouse medido en coordenadas ya
         completas, la distancia contra ellos daba cualquier cosa,
         marcando de más como "cerca" (dorado) en vez de azules. Por eso
         esta función se vuelve a llamar en cada tick de
         ResizeObserverConstelacion (ver más abajo), no solo una vez: así
         el buffer nunca queda desincronizado del tamaño real en pantalla,
         ni siquiera a mitad de la transición. */
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      anchoConstelacion = canvasConstelacion.clientWidth;
      altoConstelacion = canvasConstelacion.clientHeight;
      if (!anchoConstelacion || !altoConstelacion) return; // todavía oculto (display:none), nada que medir
      canvasConstelacion.width = anchoConstelacion * dpr;
      canvasConstelacion.height = altoConstelacion * dpr;
      ctxConstelacion.setTransform(dpr, 0, 0, dpr, 0, 0);
      armarNodos();
    }
    var resizeObserverConstelacion = typeof ResizeObserver !== 'undefined'
      ? new ResizeObserver(function () { medirConstelacion(); })
      : null;

    var ESPACIADO = 64;
    function armarNodos() {
      nodosConstelacion = [];
      var cols = Math.ceil(anchoConstelacion / ESPACIADO) + 1;
      var filas = Math.ceil(altoConstelacion / ESPACIADO) + 1;
      for (var i = 0; i < cols; i++) {
        for (var j = 0; j < filas; j++) {
          var x = i * ESPACIADO;
          var y = j * ESPACIADO;
          nodosConstelacion.push({
            x: x, y: y, vx: 0, vy: 0, baseX: x, baseY: y,
            radio: Math.random() * 1.1 + 1.1,
            pulso: Math.random() * Math.PI * 2
          });
        }
      }
    }

    function onMouseMoveConstelacion(e) {
      /* Contra el propio <canvas> (fixed, inset:0 — su rect es siempre
         el viewport), no contra heroSeccionGlobal: esa sección mide
         240vh en escritorio (el "pase de diapositivas") y va
         desplazándose con el scroll, así que su rect.top se vuelve muy
         negativo apenas se baja un poco. Medir contra ella desincroniza
         la posición del mouse que ve la física de los nodos frente a
         dónde está el cursor de verdad en pantalla — y como esto solo
         se recalcula cuando SÍ hay un mousemove, un solo movimiento de
         mouse mientras se está bajando o subiendo deja ese desfase
         "congelado" hasta el siguiente mousemove, con los nodos
         empujados hacia un punto fantasma en vez de volver a su sitio. */
      var rc = canvasConstelacion.getBoundingClientRect();
      mouseConstelacion.x = e.clientX - rc.left;
      mouseConstelacion.y = e.clientY - rc.top;
    }
    function onMouseLeaveConstelacion() {
      mouseConstelacion.x = -1000;
      mouseConstelacion.y = -1000;
    }

    var RADIO_MOUSE = 200;
    var DIST_MAX_CONEXION = ESPACIADO * 1.35;
    var RESORTE = 18;
    var AMORTIGUACION = 0.82;
    var AZUL = '35, 48, 68'; // casi el mismo azul que el video/overlay de fondo (var(--blue): 20,35,61) — la malla en reposo casi no debe notarse
    var ACENTO = '85, 100, 125'; // gris azulado apagado para el efecto cerca del mouse — nada vivo ni cálido

    function dibujarFrame(ahora) {
      var dt = Math.min((ahora - ultimoTiempo) / 1000, 0.05) || 0.016;
      ultimoTiempo = ahora;

      ctxConstelacion.clearRect(0, 0, anchoConstelacion, altoConstelacion);

      for (var n = 0; n < nodosConstelacion.length; n++) {
        var nodo = nodosConstelacion[n];
        nodo.pulso += dt * 3;

        var dx = mouseConstelacion.x - nodo.x;
        var dy = mouseConstelacion.y - nodo.y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < RADIO_MOUSE && dist > 0) {
          var potencia = 1 - dist / RADIO_MOUSE;
          var fuerza = potencia * 900;
          var angulo = Math.atan2(dy, dx);
          nodo.vx -= Math.cos(angulo) * fuerza * dt;
          nodo.vy -= Math.sin(angulo) * fuerza * dt;
        }

        nodo.vx += (nodo.baseX - nodo.x) * RESORTE * dt;
        nodo.vy += (nodo.baseY - nodo.y) * RESORTE * dt;
        nodo.vx *= AMORTIGUACION;
        nodo.vy *= AMORTIGUACION;
        nodo.x += nodo.vx * dt * 60;
        nodo.y += nodo.vy * dt * 60;
      }

      var distMaxCuad = DIST_MAX_CONEXION * DIST_MAX_CONEXION;
      for (var a = 0; a < nodosConstelacion.length; a++) {
        var na = nodosConstelacion[a];
        for (var b = a + 1; b < nodosConstelacion.length; b++) {
          var nb = nodosConstelacion[b];
          var ndx = na.x - nb.x;
          var ndy = na.y - nb.y;
          var distCuad = ndx * ndx + ndy * ndy;
          if (distCuad < distMaxCuad) {
            var distReal = Math.sqrt(distCuad);
            var alpha = (1 - distReal / DIST_MAX_CONEXION) * 0.1;
            ctxConstelacion.strokeStyle = 'rgba(' + AZUL + ', ' + alpha + ')';
            ctxConstelacion.lineWidth = 0.7;
            ctxConstelacion.beginPath();
            ctxConstelacion.moveTo(na.x, na.y);
            ctxConstelacion.lineTo(nb.x, nb.y);
            ctxConstelacion.stroke();
          }
        }
      }

      for (var m = 0; m < nodosConstelacion.length; m++) {
        var pt = nodosConstelacion[m];
        var pdx = mouseConstelacion.x - pt.x;
        var pdy = mouseConstelacion.y - pt.y;
        var cerca = Math.sqrt(pdx * pdx + pdy * pdy) < RADIO_MOUSE;
        var alphaBase = cerca ? 0.6 : 0.14 + Math.sin(pt.pulso) * 0.05;
        var radioActual = cerca ? pt.radio * 2 : pt.radio + Math.sin(pt.pulso) * 0.25;
        ctxConstelacion.fillStyle = 'rgba(' + (cerca ? ACENTO : AZUL) + ', ' + alphaBase + ')';
        ctxConstelacion.beginPath();
        ctxConstelacion.arc(pt.x, pt.y, Math.max(0.5, radioActual), 0, Math.PI * 2);
        ctxConstelacion.fill();
      }

      rafConstelacion = requestAnimationFrame(dibujarFrame);
    }

    function iniciarConstelacion() {
      if (rafConstelacion !== null || reducidoConstelacion) return;
      medirConstelacion();
      window.addEventListener('mousemove', onMouseMoveConstelacion);
      window.addEventListener('mouseleave', onMouseLeaveConstelacion);
      if (resizeObserverConstelacion) resizeObserverConstelacion.observe(canvasConstelacion);
      ultimoTiempo = performance.now();
      rafConstelacion = requestAnimationFrame(dibujarFrame);
    }
    function detenerConstelacion() {
      if (rafConstelacion !== null) cancelAnimationFrame(rafConstelacion);
      rafConstelacion = null;
      window.removeEventListener('mousemove', onMouseMoveConstelacion);
      window.removeEventListener('mouseleave', onMouseLeaveConstelacion);
      if (resizeObserverConstelacion) resizeObserverConstelacion.disconnect();
      if (ctxConstelacion) ctxConstelacion.clearRect(0, 0, anchoConstelacion, altoConstelacion);
    }
    function sincronizarConstelacion() {
      if (heroSeccionGlobal.classList.contains('page-hero--portada')) iniciarConstelacion();
      else detenerConstelacion();
    }

    window.__sincronizarConstelacion = sincronizarConstelacion;
    sincronizarConstelacion();
  }
})();
