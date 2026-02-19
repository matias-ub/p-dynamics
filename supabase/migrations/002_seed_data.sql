-- ================================================
-- SEED INICIAL - 3 Preguntas + 3 opciones cada una
-- Fechas: ayer, hoy, mañana (dinámicas con CURRENT_DATE)
-- ================================================

-- Pregunta 1 - Ayer
WITH q1 AS (
  INSERT INTO public.questions (text, intensity_level) 
  VALUES ('¿Cómo preferís pasar un viernes a la noche en pareja?', 2)
  RETURNING id
)
INSERT INTO public.daily_questions (question_id, date)
SELECT id, CURRENT_DATE - INTERVAL '1 day' FROM q1
ON CONFLICT (date) DO NOTHING;

INSERT INTO public.options (question_id, text, position)
SELECT q.id, opt.text, opt.pos
FROM public.questions q, (VALUES 
  (1, 'Cena romántica en casa con velas y buena música'),
  (2, 'Salir a un restaurante lindo y caminar después'),
  (3, 'Quedarnos en casa pidiendo delivery y viendo una serie abrazados')
) AS opt(pos, text)
WHERE q.text = '¿Cómo preferís pasar un viernes a la noche en pareja?';

-- Pregunta 2 - Hoy
WITH q2 AS (
  INSERT INTO public.questions (text, intensity_level) 
  VALUES ('¿Qué harías si tuvieras un día completamente libre sorpresa mañana?', 3)
  RETURNING id
)
INSERT INTO public.daily_questions (question_id, date)
SELECT id, CURRENT_DATE FROM q2
ON CONFLICT (date) DO NOTHING;

INSERT INTO public.options (question_id, text, position)
SELECT q.id, opt.text, opt.pos
FROM public.questions q, (VALUES 
  (1, 'Quedarnos todo el día en pijama descansando y cocinando juntos'),
  (2, 'Salir a explorar un barrio nuevo o un lugar que no conocemos'),
  (3, 'Hacer una escapada corta a un pueblo o playa cerca')
) AS opt(pos, text)
WHERE q.text = '¿Qué harías si tuvieras un día completamente libre sorpresa mañana?';

-- Pregunta 3 - Mañana
WITH q3 AS (
  INSERT INTO public.questions (text, intensity_level) 
  VALUES ('Si ganáramos un viaje gratis para dos personas, ¿qué tipo de viaje elegirías?', 4)
  RETURNING id
)
INSERT INTO public.daily_questions (question_id, date)
SELECT id, CURRENT_DATE + INTERVAL '1 day' FROM q3
ON CONFLICT (date) DO NOTHING;

INSERT INTO public.options (question_id, text, position)
SELECT q.id, opt.text, opt.pos
FROM public.questions q, (VALUES 
  (1, 'Playa paradisíaca para relajarnos completamente'),
  (2, 'Ciudad europea con buena comida, cultura y paseos'),
  (3, 'Aventura en la naturaleza (montañas, bosque o trekking)')
) AS opt(pos, text)
WHERE q.text = 'Si ganáramos un viaje gratis para dos personas, ¿qué tipo de viaje elegirías?';

-- ================================================
-- VERIFICACIÓN FINAL (esto te muestra todo bonito)
-- ================================================
SELECT 
  dq.date as "Fecha",
  q.text as "Pregunta",
  string_agg(o.text, ' | ') as "Opciones"
FROM public.daily_questions dq
JOIN public.questions q ON q.id = dq.question_id
JOIN public.options o ON o.question_id = q.id
GROUP BY dq.date, q.text
ORDER BY dq.date;