// Contador de vistas por apunte, respaldado por un almacén KV de Vercel
// (integración Vercel KV / Upstash Redis). No usa paquetes externos: llama
// directo a la REST API del KV con fetch, así no hace falta build ni
// package.json para esta función.
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
    res.status(500).json({ error: 'El almacén de vistas no está configurado.' });
    return;
  }

  const key = encodeURIComponent('vistas:' + doc);
  const accion = req.method === 'POST' ? 'incr' : 'get';

  try {
    const r = await fetch(base + '/' + accion + '/' + key, {
      headers: { Authorization: 'Bearer ' + token },
    });
    const datos = await r.json();
    const vistas = typeof datos.result === 'number' ? datos.result : Number(datos.result) || 0;

    res.setHeader('Cache-Control', 'no-store');
    res.status(200).json({ doc: doc, vistas: vistas });
  } catch (err) {
    res.status(502).json({ error: 'No se pudo leer el contador.' });
  }
}
