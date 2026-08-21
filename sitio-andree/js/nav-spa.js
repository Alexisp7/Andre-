/* Navegación SPA entre las páginas con franja de video: intercepta los
   clics en enlaces internos, trae la página siguiente por fetch() y
   reemplaza solo el texto de la franja (.page-hero-inner) y el
   contenido de abajo (#spaMain) — el menú y el propio <video> de
   fondo nunca se tocan, así que jamás se recargan ni reinician: el
   video sigue reproduciéndose sin cortes de una "página" a la
   siguiente.

   La portada (index.html) queda fuera a propósito: su franja
   (.library-hero) es una sección con clases y proporciones propias,
   distinta de .page-hero de las demás — no es el mismo elemento que
   se pueda "seguir mostrando" al cambiar de página, así que intentarlo
   solo cambiaría el texto de adentro dejando el marco de afuera
   equivocado. Los enlaces hacia o desde la portada navegan normal,
   de verdad; lo mismo visor.html, que no tiene franja de video y cuya
   propia lógica (pdf.js) es demasiado particular como para
   revalidarla dentro de este esquema.

   Si algo no cuadra (fetch falla, la página no tiene la estructura
   esperada, JS deshabilitado), todo cae de vuelta a una navegación
   real — nunca deja al sitio en un estado roto. */
(function () {
  'use strict';

  var PAGINAS = [
    'materiales.html', 'investigacion.html', 'noticias.html',
    'apuntes.html', 'contacto.html', 'biopsicologia.html', 'neuroanatomia.html',
    'neuropsicologia.html', 'psicofarmacologia.html'
  ];

  // Qué pestaña(s) del menú marcar como activa para cada página.
  var ACTIVOS = {
    'materiales.html': { cursos: true },
    'psicofarmacologia.html': { subActiva: true },
    'investigacion.html': { investigacion: true },
    'noticias.html': { noticias: true },
    'biopsicologia.html': { cursos: true },
    'neuroanatomia.html': { cursos: true },
    'neuropsicologia.html': { cursos: true }
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
      var sub = nav.querySelector('.nav-submenu a[href="psicofarmacologia.html"]');
      if (sub) sub.classList.add('sub-activa');
    }
  }

  /* Los <script> insertados vía innerHTML no se ejecutan solos — hay
     que reemplazar cada uno por un elemento <script> recién creado
     para que el navegador sí los corra (misma técnica que usan pjax y
     turbo). */
  function ejecutarScripts(contenedor) {
    var scripts = contenedor.querySelectorAll('script');
    scripts.forEach(function (viejo) {
      var nuevo = document.createElement('script');
      for (var i = 0; i < viejo.attributes.length; i++) {
        nuevo.setAttribute(viejo.attributes[i].name, viejo.attributes[i].value);
      }
      nuevo.textContent = viejo.textContent;
      viejo.parentNode.replaceChild(nuevo, viejo);
    });
  }

  function moverFoco(heroActual) {
    var titulo = heroActual.querySelector('.page-hero-title');
    if (!titulo) return;
    if (!titulo.hasAttribute('tabindex')) titulo.setAttribute('tabindex', '-1');
    titulo.focus({ preventScroll: true });
  }

  var generacion = 0;

  function navegar(url, conHistoria) {
    var miGeneracion = ++generacion;
    var archivo = archivoDe(url);

    var heroActual = document.querySelector(HERO_SEL);
    var mainActual = document.querySelector(MAIN_SEL);
    if (!heroActual || !mainActual) { irReal(url.href); return; }

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

        heroActual.innerHTML = nuevoHero.innerHTML;
        mainActual.innerHTML = nuevoMain.innerHTML;
        ejecutarScripts(heroActual);
        ejecutarScripts(mainActual);
        actualizarNav(archivo);
        moverFoco(heroActual);

        heroActual.classList.remove('spa-hero-sale');
        void heroActual.offsetWidth; // fuerza reflow para reiniciar la animación
        heroActual.classList.add('spa-hero-entra');

        mainActual.classList.remove('spa-main-entra');
        void mainActual.offsetWidth;
        mainActual.classList.add('spa-main-entra');
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
})();
