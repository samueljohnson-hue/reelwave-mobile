import express from 'express';
import cors from 'cors';
import multer from 'multer';
import OpenAI, { toFile } from 'openai';

const app = express();
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 25 * 1024 * 1024 } });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
app.use(cors());
app.get('/health', (_req,res)=>res.json({ok:true}));

app.post('/api/analyze', upload.single('audio'), async (req,res)=>{
  try {
    if (!req.file) return res.status(400).send('Missing audio file');
    const audio = await toFile(req.file.buffer, req.file.originalname || 'song.mp3', { type: req.file.mimetype || 'audio/mpeg' });
    const tx = await openai.audio.transcriptions.create({
      file: audio,
      model: 'gpt-4o-transcribe',
      response_format: 'verbose_json',
      timestamp_granularities: ['word','segment']
    });
    const words = (tx.words || []).map(w=>({word:w.word,start:Number(w.start),end:Number(w.end)}));
    const segments = tx.segments || [];
    const style = String(req.body.style || 'dream');
    const sceneInput = segments.slice(0,12).map(s=>({start:s.start,end:s.end,text:s.text}));
    const plan = await openai.responses.create({
      model: 'gpt-5.6-luna',
      input: `Create a concise visual scene plan for a vertical music visualizer. Style: ${style}. Only surreal/original skies, clouds, stars, moons, sunsets, lightning, aurora, abstract celestial light. Never depict copyrighted characters or logos. Return JSON with a scenes array. Each scene: {start,end,prompt,mood}. Segments: ${JSON.stringify(sceneInput)}`,
      text: { format: { type: 'json_schema', name: 'scene_plan', schema: { type:'object', properties:{ scenes:{type:'array',items:{type:'object',properties:{start:{type:'number'},end:{type:'number'},prompt:{type:'string'},mood:{type:'string'}},required:['start','end','prompt','mood'],additionalProperties:false}}},required:['scenes'],additionalProperties:false } } }
    });
    let scenes=[];
    try { scenes=JSON.parse(plan.output_text).scenes || []; } catch {}
    res.json({ text: tx.text, words, scenes });
  } catch (err) {
    console.error(err);
    res.status(500).send(err?.message || 'AI analysis failed');
  }
});

app.listen(process.env.PORT || 8787, ()=>console.log('Reelwave AI backend listening'));