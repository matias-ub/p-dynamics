# ðŸ’‘ Parejas - Daily Question Game

Una pregunta diaria para parejas que quieren conectar, entenderse mejor y mantener una rutina de comunicaciÃ³n a travÃ©s de preguntas interesantes.

## ðŸŽ¯ Concepto

Cada dÃ­a, ambas personas responden dos preguntas:
1. **Â¿QuÃ© harÃ­as tÃº?** - Tu respuesta personal
2. **Â¿QuÃ© harÃ­a tu pareja?** - Predice quÃ© elegirÃ­a tu pareja

La app rastrea:
- âœ… Si las predicciones coinciden (quÃ© tan bien conoces a tu pareja)
- ðŸ”¥ Racha de dÃ­as consecutivos donde ambos respondieron
- ðŸ’‘ ConexiÃ³n a travÃ©s de respuestas compartidas

## âœ¨ Flujo Simplificado

### Usuario 1 (Crea)
1. Entra a la pÃ¡gina principal â†’ Ve la pregunta del dÃ­a
2. Click en "Responder" â†’ Se crea automÃ¡ticamente:
   - Usuario anÃ³nimo
   - Room privado
3. Responde ambas preguntas
4. Recibe cÃ³digo para compartir con su pareja

### Usuario 2 (Se Une)
1. Recibe cÃ³digo/enlace
2. Entra con el cÃ³digo
3. Se crea usuario anÃ³nimo automÃ¡ticamente
4. Responde ambas preguntas

**Sin registro, sin complicaciones, sin pasos extras.**

## âœ¨ CaracterÃ­sticas

- ðŸŽ² **Pregunta Diaria**: Una nueva pregunta cada dÃ­a con opciones mÃºltiples
- âš¡ **Auto-CreaciÃ³n**: Room y usuario se crean automÃ¡ticamente al responder
- ðŸ‘¤ **100% AnÃ³nimo**: Sin email, sin password, sin datos personales
- ðŸ”„ **Auto-Refresh de SesiÃ³n**: Supabase JS maneja tokens automÃ¡ticamente (nunca expiran)
- ðŸ“ˆ **Racha AutomÃ¡tica**: Tracking de dÃ­as consecutivos
- ðŸŽ¨ **UI Minimalista**: Flujo directo sin distracciones
- ðŸ”— **Compartir FÃ¡cil**: CÃ³digo o enlace directo para invitar

## ðŸ—ï¸ Arquitectura

### Tech Stack
- **Backend**: FastAPI (Python) - API REST + SSR
- **Database**: Supabase (Postgres + Auth + RLS)
- **Frontend**: Jinja2 Templates + Bootstrap 5
- **Auth Client**: Supabase JS (auto-refresh, session management)
- **No estatal**: Sessions manejadas por Supabase (localStorage + cookies)

### Project Structure
```
p-dynamics/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ main.py              # FastAPI app + endpoint /api/start-session
â”‚   â”œâ”€â”€ config.py            # Environment configuration
â”‚   â”œâ”€â”€ dependencies.py      # Auth dependencies (JWT validation)
â”‚   â”œâ”€â”€ models.py            # Pydantic models
â”‚   â”‚
â”‚   â”œâ”€â”€ routes/              # Route handlers
â”‚   â”‚   â”œâ”€â”€ pages.py         # SSR: /, /join-room, /question/{id}
â”‚   â”‚   â”œâ”€â”€ auth.py          # API: /refresh (no usado ahora)
â”‚   â”‚   â”œâ”€â”€ rooms.py         # API: POST/GET rooms
â”‚   â”‚   â”œâ”€â”€ questions.py     # API: GET today's question
â”‚   â”‚   â””â”€â”€ responses.py     # API: POST/GET responses, streaks
â”‚   â”‚
â”‚   â”œâ”€â”€ services/            # Business logic
â”‚   â”‚   â”œâ”€â”€ room_service.py  # Create rooms, get by token/id
â”‚   â”‚   â”œâ”€â”€ question_service.py  # Get daily questions
â”‚   â”‚   â””â”€â”€ response_service.py  # Submit, calculate streaks
â”‚   â”‚
â”‚   â”œâ”€â”€ utils/
â”‚   â”‚   â””â”€â”€ supabase.py      # Supabase backend client
â”‚   â”‚
â”‚   â”œâ”€â”€ templates/           # Jinja2 templates (SOLO 3 PÃGINAS)
â”‚   â”‚   â”œâ”€â”€ base.html        # Template base + Supabase JS init
â”‚   â”‚   â”œâ”€â”€ index.html       # Landing con pregunta del dÃ­a
â”‚   â”‚   â”œâ”€â”€ join_room.html   # Unirse con cÃ³digo
â”‚   â”‚   â””â”€â”€ question.html    # Formulario de respuesta + invitar
â”‚   â”‚
â”‚   â””â”€â”€ static/
â”‚       â””â”€â”€ css/
â”‚           â””â”€â”€ style.css    # Estilos personalizados
â”‚
â”œâ”€â”€ supabase/
â”‚   â””â”€â”€ migrations/
â”‚       â”œâ”€â”€ 001_initial_schema.sql  # Schema completo
â”‚       â””â”€â”€ 002_seed_data.sql       # Preguntas de ejemplo
â”‚
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .env
â””â”€â”€ README.md
```

### Frontend Auth Flow (Supabase JS)
```javascript
// En base.html - InicializaciÃ³n global
window.appSupabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// FunciÃ³n helper - crea anÃ³nimo si no hay sesiÃ³n
async function ensureSession() {
  const { data: { session } } = await appSupabase.auth.getSession()
  if (!session) {
    const { data } = await appSupabase.auth.signInAnonymously()
    return data.session
  }
  return session
}

// En cualquier pÃ¡gina
const session = await ensureSession()
const token = session.access_token
// Supabase auto-refresca el token antes de que expire
```

## ðŸ—„ï¸ Database Schema

### Tablas Principales
- **auth.users** - Usuarios de Supabase (anÃ³nimos)
- **profiles** - Perfiles extendidos (auto-creados via trigger)
- **questions** - Pool de preguntas (intensity_level 1-5)
- **options** - Opciones de respuesta por pregunta (position)
- **daily_questions** - Maps question_id â†’ date (una por dÃ­a)
- **rooms** - Rooms privados (token Ãºnico, max_participants=2)
- **responses** - Respuestas: self_option_id + partner_prediction_option_id

### Row Level Security (RLS)
```sql
-- Usuarios pueden ver/editar solo su perfil
CREATE POLICY "Users can read own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

-- Solo los participantes del room ven sus respuestas
CREATE POLICY "Room participants can read responses" ON responses
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM responses r2 
      WHERE r2.room_id = responses.room_id 
        AND r2.user_id = auth.uid()
    )
  );

-- Usuarios solo insertan sus propias respuestas
CREATE POLICY "Users insert own response" ON responses
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### Constraints Importantes
```sql
-- Un usuario responde solo 1 vez por dÃ­a por room
CREATE UNIQUE INDEX uniq_response_per_user_day 
  ON responses(room_id, daily_question_id, user_id);

-- Parejas siempre tienen max 2 participantes
ALTER TABLE rooms ADD CONSTRAINT chk_couple_max_participants 
  CHECK (room_type != 'couple' OR max_participants = 2);
```

## ðŸš€ Quick Start

### Prerequisites
- Python 3.8+
- Supabase account (free tier)

### Installation

1. **Clone y setup**
```bash
git clone https://github.com/matias-ub/p-dynamics.git
cd p-dynamics
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

2. **Configurar Supabase**

Crea un proyecto en [supabase.com](https://supabase.com) y:

a) **Ejecuta las migraciones** (SQL Editor):
   - `supabase/migrations/001_initial_schema.sql`
   - `supabase/migrations/002_seed_data.sql`

b) **Habilita Anonymous Auth**:
   - Settings â†’ Authentication â†’ Enable Anonymous Sign-ins

c) **ObtÃ©n las credenciales**:
   - Settings â†’ API â†’ Project URL y anon/public key

3. **Crear `.env`**
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=eyJhbG...  # La puedes exponer en frontend
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...  # Secreta, solo backend
```

4. **Ejecutar**
```bash
uvicorn app.main:app --reload
```

Abre `http://localhost:8000` ðŸŽ‰

## ðŸ“– CÃ³mo Funciona

### 1. Usuario inicia respuesta
```
GET / 
â†’ Ve pregunta del dÃ­a
â†’ Click "Responder"
â†’ JS: ensureSession() crea usuario anÃ³nimo
â†’ POST /api/rooms crea room
â†’ Redirect a /question/{room_id}
```

### 2. Usuario responde
```
GET /question/{room_id}
â†’ Muestra formulario con opciones
â†’ Usuario elige "QuÃ© harÃ­a yo" y "QuÃ© harÃ­a mi pareja"
â†’ POST /api/responses con {self_option_id, partner_prediction_option_id}
â†’ Guarda en DB con user_id del JWT
```

### 3. Usuario invita
```
Si es el primer participante del room:
â†’ Muestra botÃ³n "Invitar"
â†’ CÃ³digo: ABCD1234EFGH5678
â†’ Link: /join-room?token=ABCD...
```

### 4. Pareja se une
```
GET /join-room?token=ABCD...
â†’ Verifica room existe: GET /api/rooms/{token}
â†’ ensureSession() crea usuario anÃ³nimo 2
â†’ Redirect a /question/{room_id}
â†’ Responde las mismas preguntas
```

### 5. Ver si coincidieron
```
Cuando ambos respondieron:
â†’ Compara self_option_id del usuario 1 con partner_prediction_option_id del usuario 2
â†’ Compara self_option_id del usuario 2 con partner_prediction_option_id del usuario 1
â†’ Â¿Acertaron? âœ… o âŒ
```

## ðŸŒŸ API Endpoints

### PÃ¡ginas (Server-Side Rendered)
| Ruta | DescripciÃ³n |
|------|-------------|
| `GET /` | Landing page con pregunta del dÃ­a |
| `GET /join-room?token=XXX` | Unirse a un room existente |
| `GET /question/{room_id}` | Formulario para responder (requiere auth) |

### API REST (JSON)
| MÃ©todo | Ruta | DescripciÃ³n | Auth |
|--------|------|-------------|------|
| `POST` | `/api/rooms` | Crear nuevo room | SÃ­ |
| `GET` | `/api/rooms/{token}` | Obtener room por token | No |
| `GET` | `/api/rooms/id/{room_id}` | Obtener room por ID | SÃ­ |
| `GET` | `/api/questions/today` | Pregunta del dÃ­a | No |
| `POST` | `/api/responses` | Enviar respuesta | SÃ­ |
| `GET` | `/api/responses/room/{room_id}` | Todas las respuestas del room | SÃ­ |
| `GET` | `/api/responses/room/{room_id}/streak` | Racha actual | SÃ­ |
| `GET` | `/api/responses/room/{room_id}/status/{question_id}` | Â¿Ambos respondieron? | SÃ­ |

### Modelos Request/Response

**POST /api/responses**
```json
{
  "room_id": "uuid",
  "daily_question_id": "uuid",
  "self_option_id": "uuid",
  "partner_prediction_option_id": "uuid"
}
```

**GET /api/questions/today**
```json
{
  "id": "uuid",
  "text": "Â¿PreferirÃ­as...?",
  "intensity_level": 3,
  "options": [
    {"id": "uuid", "text": "OpciÃ³n A", "position": 1},
    {"id": "uuid", "text": "OpciÃ³n B", "position": 2}
  ]
}
```

## ðŸŽ¨ Agregar Preguntas

Edita `supabase/migrations/002_seed_data.sql`:

```sql
-- 1. Insertar pregunta
WITH q AS (
  INSERT INTO questions (text, intensity_level) 
  VALUES ('Â¿PreferirÃ­as vivir en la playa o en la montaÃ±a?', 2)
  RETURNING id
)
-- 2. Asignarla a una fecha
INSERT INTO daily_questions (question_id, date)
SELECT id, '2026-02-20' FROM q;

-- 3. Agregar opciones
INSERT INTO options (question_id, text, position)
SELECT q.id, opt.text, opt.pos
FROM questions q, (VALUES 
  (1, 'ðŸ–ï¸ Playa - sol, mar y arena'),
  (2, 'â›°ï¸ MontaÃ±a - paz, naturaleza y aire puro'),
  (3, 'ðŸ™ï¸ Ciudad - prefiero la vida urbana')
) AS opt(pos, text)
WHERE q.text = 'Â¿PreferirÃ­as vivir en la playa o en la montaÃ±a?';
```

**Intensity levels:**
- 1: Ligera (comida favorita, pelÃ­culas)
- 2: Casual (preferencias de estilo de vida)
- 3: Moderada (valores, prioridades)
- 4: Profunda (miedos, sueÃ±os)
- 5: Ãntima (vulnerabilidad, futuro juntos)

## ðŸš¢ Deployment

### Railway
```bash
# Conecta tu repo GitHub
# Railway detecta FastAPI automÃ¡ticamente
# Variables de entorno en Settings:
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

### Render
```bash
# Build Command
pip install -r requirements.txt
# Start Command
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Fly.io
```toml
# fly.toml
app = "p-dynamics"

[env]
  PORT = "8000"

[[services]]
  http_checks = []
  internal_port = 8000
  protocol = "tcp"
```

## ðŸ›£ï¸ Roadmap

### MVP Actual âœ…
- [x] Flujo simplificado (1 click para responder)
- [x] Auto-creaciÃ³n de usuario y room
- [x] Supabase JS con auto-refresh
- [x] Sistema de invitaciÃ³n con cÃ³digo
- [x] RLS completo para privacidad

### PrÃ³ximos Pasos
- [ ] PÃ¡gina de resultados/comparaciÃ³n
- [ ] Dashboard con histÃ³rico de respuestas
- [ ] Ver racha actual en UI
- [ ] Notificaciones cuando ambos respondieron
- [ ] Convertir usuario anÃ³nimo a permanente (email/password)
- [ ] PWA (installable en mÃ³vil)
- [ ] Temas de color personalizados
- [ ] Packs de preguntas temÃ¡ticas

### Futuro
- [ ] Grupos (mÃ¡s de 2 personas)
- [ ] EstadÃ­sticas y grÃ¡ficos
- [ ] Compartir en redes sociales
- [ ] API pÃºblica para integrar en otras apps
- [ ] Multi-idioma

## ðŸ”§ Troubleshooting

### Error: "Token validation failed: token is expired"
**SoluciÃ³n:** Ya no deberÃ­a pasar con Supabase JS, que auto-refresca. Si pasa:
- Verifica que Supabase JS estÃ¡ cargado: `console.log(window.appSupabase)`
- Borra cookies: DevTools â†’ Application â†’ Cookies â†’ Clear All

### Error: "Room capacity exceeded"
**Causa:** El room ya tiene 2 participantes.
**SoluciÃ³n:** Crear un nuevo room (cada pareja necesita su propio room).

### No aparece la pregunta del dÃ­a
**Causa:** No hay pregunta asignada para la fecha actual.
**SoluciÃ³n:** Ejecuta en SQL Editor:
```sql
-- Ver quÃ© fechas tienen preguntas
SELECT * FROM daily_questions ORDER BY date DESC;

-- Asignar pregunta a hoy
INSERT INTO daily_questions (question_id, date)
SELECT id, CURRENT_DATE FROM questions LIMIT 1;
```

### Anonymous auth no funciona
**SoluciÃ³n:** 
1. Supabase Dashboard â†’ Authentication â†’ Providers
2. Encuentra "Anonymous Sign-ins"
3. Toggle ON
4. Save

## ðŸ“ License

MIT License - Ver [LICENSE](LICENSE)

## ðŸ‘¥ Contributing

Pull requests son bienvenidos. Para cambios grandes, abre un issue primero.

1. Fork
2. Crea tu rama (`git checkout -b feature/CosaIncreible`)
3. Commit (`git commit -m 'Add: cosa increÃ­ble'`)
4. Push (`git push origin feature/CosaIncreible`)
5. Pull Request

## ðŸ“§ Contact

**Matias** - [@matias-ub](https://github.com/matias-ub)

Proyecto: [https://github.com/matias-ub/p-dynamics](https://github.com/matias-ub/p-dynamics)

---

ðŸ’‘ Hecho con amor para parejas que quieren conectar mejor
