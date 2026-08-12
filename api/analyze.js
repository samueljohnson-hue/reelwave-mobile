import OpenAI, { toFile } from 'openai';

export const config = { api: { bodyParser: false } };

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks);
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST required' });
  if (!process.env.OPENAI_API_KEY) return res.status(500).json({ error: 'OPENAI_API_KEY is not configured' });
  try {
    const contentType = req.headers['content-type'] || '';
    const match = contentType.match(/boundary=(?:"([^"]+)"|([^;]+))/i);
    if (!match) return res.status(400).json({ error: 'multipart/form-data required' });
    const boundary = Buffer.from(`--${match[1] || match[2]}`);
    const body = await readBody(req);
    const parts = [];
    let start = body.indexOf(boundary) + boundary.length + 2;
    while (start > boundary.length + 1) {
      const end = body.indexOf(boundary, start);
      if (end < 0) break;
      parts.push(body.subarray(start, Math.max(start, end - 2)));
      start = end + boundary.length + 2;
    }
    let audioPart = null;
    let style = 'dream';
    for (const part of parts) {
      const split = part.indexOf(Buffer.from('\r\n\r\n'));
      if (split < 0) continue;
      const headers = part.subarray(0, split).toString('utf8');
      const data = part.subarray(split + 4);
      const name = headers.match(/name="([^"]+)"/i)?.[1];
      if (name === 'style') style = data.toString('utf8').trim();
      if (name === 'audio') {
        audioPart = {
          data,
          filename: headers.match(/filename="([^"]+)"/i)?.[1] || 'song.wav',
          type: headers.match(/content-type:\s*([^\r\n]+)/i)?.[1] || 'audio/wav'
        };
      }
    }
    if (!audioPart) return res.status(400).json({ error: 'Missing audio file' });

    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const audio = await toFile(audioPart.data, audioPart.filename, { type: audioPart.type });
    const tx = await openai.audio.transcriptions.create({
      file: audio,
      model: 'whisper-1',
      response_format: 'verbose_json',
      timestamp_granularities: ['word', 'segment']
    });
    const words = (tx.words || []).map(w => ({ word: w.word, start: Number(w.start), end: Number(w.end) }));
    const segments = (tx.segments || []).slice(0, 16);

    let scenes = [];
    try {
      const response = await openai.responses.create({
        model: 'gpt-5-mini',
        input: `Plan surreal original animated sky scenes for a vertical music visualizer. Style: ${style}. Use clouds, stars, moons, sunsets, lightning, aurora and abstract celestial light. No logos or copyrighted characters. Return JSON only: {"scenes":[{"start":0,"end":5,"prompt":"...","mood":"..."}]}. Lyrics: ${JSON.stringify(segments.map(s => ({start:s.start,end:s.end,text:s.text})))}`
      });
      const cleaned = response.output_text.replace(/^```json\s*|\s*```$/g, '');
      scenes = JSON.parse(cleaned).scenes || [];
    } catch (sceneErr) {
      console.warn('Scene planning skipped:', sceneErr?.message || sceneErr);
    }

    return res.status(200).json({ text: tx.text || '', words, scenes });
  } catch (err) {
    console.error(err);
    if (err?.code === 'credit_balance_exhausted' || err?.status === 429) {
      return res.status(402).json({
        error: 'OpenAI API credits are empty. Add API credits in your OpenAI Platform billing account, then try again.',
        code: 'API_CREDITS_REQUIRED'
      });
    }
    return res.status(500).json({ error: err?.message || 'AI analysis failed' });
  }
}
