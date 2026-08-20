// Contador de descargas por apunte. Mismo mecanismo que api/views.js
// (almacén KV de Vercel), pero con su propia clave para no mezclar
// vistas con descargas.
//
// Variables de entorno esperadas (las crea Vercel solas al conectar el KV
// desde el panel del proyecto): KV_REST_API_URL, KV_REST_API_TOKEN.

export default async function handler(req, res) {
  const doc = (req.query.doc || '').toString();

  if (!doc || doc.includes('..')) {
    res.status(400).json({ error: 'Falta el parámetro doc.' });
    return;
  }

  const base = process.env.KV_REST_API_URL;
  const token = process.env.KV_REST_API_TOKEN;
  if (!base || !token) {
    res.status(500).json({ error: 'El almacén de descargas no está configurado.' });
    return;
  }

  const key = encodeURIComponent('descargas:' + doc);
  const accion = req.method === 'POST' ? 'incr' : 'get';

  try {
    const r = await fetch(base + '/' + accion + '/' + key, {
      headers: { Authorization: 'Bearer ' + token },
    });
    const datos = await r.json();
    const descargas = typeof datos.result === 'number' ? datos.result : Number(datos.result) || 0;

    res.setHeader('Cache-Control', 'no-store');
    res.status(200).json({ doc: doc, descargas: descargas });
  } catch (err) {
    res.status(502).json({ error: 'No se pudo leer el contador.' });
  }
}
