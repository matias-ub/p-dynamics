# 💑 Parejas - Daily Question Game

Una pregunta diaria para parejas que quieren conectar, entenderse mejor y mantener una rutina de comunicación a través de preguntas interesantes.

## 🎯 Concepto

Cada día, ambas personas responden dos preguntas:
1. **¿Qué harías tú?** - Tu respuesta personal
2. **¿Qué haría tu pareja?** - Predice qué elegiría tu pareja

La app rastrea:
- ✅ Si las predicciones coinciden (qué tan bien conoces a tu pareja)
- 🔥 Racha de días consecutivos donde ambos respondieron
- 💡 Conexión a través de respuestas compartidas

## ✨ Flujo Simplificado

### Usuario 1 (Crea)
1. Entra a la página principal → Ve la pregunta del día
2. Click en "Responder" → Se crea automáticamente:
   - Usuario anónimo
   - Room privado
3. Responde ambas preguntas
4. Recibe código para compartir con su pareja

### Usuario 2 (Se Une)
1. Recibe código/enlace
2. Entra con el código
3. Se crea usuario anónimo automáticamente
4. Responde ambas preguntas

**Sin registro, sin complicaciones, sin pasos extras.**

## ✨ Características

- 🎲 **Pregunta Diaria**: Una nueva pregunta cada día con opciones múltiples
- ⚡ **Auto-Creación**: Room y usuario se crean automáticamente al responder
- 👤 **100% Anónimo**: Sin email, sin password, sin datos personales
- 🔄 **Auto-Refresh de Sesión**: Supabase JS maneja tokens automáticamente (nunca expiran)
- 📈 **Racha Automática**: Tracking de días consecutivos
- 🎨 **UI Minimalista**: Flujo directo sin distracciones
- 🔗 **Compartir Fácil**: Código o enlace directo para invitar

## 🗂️ Arquitectura

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
â”‚   â”‚   â”œâ”€â”€ index.html       # Landing con pregunta del día
â”‚   â”‚   â”œâ”€â”€ join_room.html   # Unirse con código
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
// En base.html - Inicialización global
window.appSupabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// Función helper - crea anónimo si no hay sesión
async function ensureSession() {
  const { data: { session } } = await appSupabase.auth.getSession()
  if (!session) {
    const { data } = await appSupabase.auth.signInAnonymously()
    return data.session
  }
  return session
}

// En cualquier página
const session = await ensureSession()
const token = session.access_token
// Supabase auto-refresca el token antes de que expire
```

## 🗄️ Database Schema

### Tablas Principales
- **auth.users** - Usuarios de Supabase (anónimos)
- **profiles** - Perfiles extendidos (auto-creados via trigger)
- **questions** - Pool de preguntas (intensity_level 1-5)
- **options** - Opciones de respuesta por pregunta (position)
- **daily_questions** - Maps question_id → date (una por día)
- **rooms** - Rooms privados (token único, max_participants=2)
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
-- Un usuario responde solo 1 vez por día por room
CREATE UNIQUE INDEX uniq_response_per_user_day 
  ON responses(room_id, daily_question_id, user_id);

-- Parejas siempre tienen max 2 participantes
ALTER TABLE rooms ADD CONSTRAINT chk_couple_max_participants 
  CHECK (room_type != 'couple' OR max_participants = 2);
```

## 🚀 Quick Start

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
   - Settings → Authentication → Enable Anonymous Sign-ins

c) **Obtén las credenciales**:
   - Settings → API → Project URL y anon/public key

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

Abre `http://localhost:8000` 🎉

## 📖 Cómo Funciona

### 1. Usuario inicia respuesta
```
GET / 
→ Ve pregunta del día
→ Click "Responder"
→ JS: ensureSession() crea usuario anónimo
→ POST /api/rooms crea room
→ Redirect a /question/{room_id}
```

### 2. Usuario responde
```
GET /question/{room_id}
→ Muestra formulario con opciones
→ Usuario elige "Qué haría yo" y "Qué haría mi pareja"
→ POST /api/responses con {self_option_id, partner_prediction_option_id}
→ Guarda en DB con user_id del JWT
```

### 3. Usuario invita
```
Si es el primer participante del room:
→ Muestra botón "Invitar"
→ Código: ABCD1234EFGH5678
→ Link: /join-room?token=ABCD...
```

### 4. Pareja se une
```
GET /join-room?token=ABCD...
→ Verifica room existe: GET /api/rooms/{token}
→ ensureSession() crea usuario anónimo 2
→ Redirect a /question/{room_id}
→ Responde las mismas preguntas
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
| `GET /` | Landing page con pregunta del día |
| `GET /join-room?token=XXX` | Unirse a un room existente |
| `GET /question/{room_id}` | Formulario para responder (requiere auth) |

### API REST (JSON)
| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/api/rooms` | Crear nuevo room | Sí |
| `GET` | `/api/rooms/{token}` | Obtener room por token | No |
| `GET` | `/api/rooms/id/{room_id}` | Obtener room por ID | Sí |
| `GET` | `/api/questions/today` | Pregunta del día | No |
| `POST` | `/api/responses` | Enviar respuesta | Sí |
| `GET` | `/api/responses/room/{room_id}` | Todas las respuestas del room | Sí |
| `GET` | `/api/responses/room/{room_id}/streak` | Racha actual | Sí |
| `GET` | `/api/responses/room/{room_id}/status/{question_id}` | ¿Ambos respondieron? | Sí |

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
- 1: Ligera (comida favorita, películas)
- 2: Casual (preferencias de estilo de vida)
- 3: Moderada (valores, prioridades)
- 4: Profunda (miedos, sueños)
- 5: Íntima (vulnerabilidad, futuro juntos)

## 🚢 Deployment

### Railway
```bash
# Conecta tu repo GitHub
# Railway detecta FastAPI automáticamente
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

## 🛣️ Roadmap

### MVP Actual ✅
- [x] Flujo simplificado (1 click para responder)
- [x] Auto-creación de usuario y room
- [x] Supabase JS con auto-refresh
- [x] Sistema de invitación con código
- [x] RLS completo para privacidad

### Próximos Pasos
- [ ] Página de resultados/comparación
- [ ] Dashboard con histórico de respuestas
- [ ] Ver racha actual en UI
- [ ] Notificaciones cuando ambos respondieron
- [ ] Convertir usuario anónimo a permanente (email/password)
- [ ] PWA (installable en móvil)
- [ ] Temas de color personalizados
- [ ] Packs de preguntas temáticas

### Futuro
- [ ] Grupos (más de 2 personas)
- [ ] Estadísticas y gráficos
- [ ] Compartir en redes sociales
- [ ] API pública para integrar en otras apps
- [ ] Multi-idioma

## 🔧 Troubleshooting

### Error: "Token validation failed: token is expired"
**Solución:** Ya no debería pasar con Supabase JS, que auto-refresca. Si pasa:
- Verifica que Supabase JS está cargado: `console.log(window.appSupabase)`
- Borra cookies: DevTools → Application → Cookies → Clear All

### Error: "Room capacity exceeded"
**Causa:** El room ya tiene 2 participantes.
**Solución:** Crear un nuevo room (cada pareja necesita su propio room).

### No aparece la pregunta del día
**Causa:** No hay pregunta asignada para la fecha actual.
**Solución:** Ejecuta en SQL Editor:
```sql
-- Ver qué fechas tienen preguntas
SELECT * FROM daily_questions ORDER BY date DESC;

-- Asignar pregunta a hoy
INSERT INTO daily_questions (question_id, date)
SELECT id, CURRENT_DATE FROM questions LIMIT 1;
```

### Anonymous auth no funciona
**Solución:** 
1. Supabase Dashboard → Authentication → Providers
2. Encuentra "Anonymous Sign-ins"
3. Toggle ON
4. Save

## 📝 License

MIT License - Ver [LICENSE](LICENSE)

## 👥 Contributing

Pull requests son bienvenidos. Para cambios grandes, abre un issue primero.

1. Fork
2. Crea tu rama (`git checkout -b feature/CosaIncreible`)
3. Commit (`git commit -m 'Add: cosa increíble'`)
4. Push (`git push origin feature/CosaIncreible`)
5. Pull Request

## 📧 Contact

**Matias** - [@matias-ub](https://github.com/matias-ub)

Proyecto: [https://github.com/matias-ub/p-dynamics](https://github.com/matias-ub/p-dynamics)

---

💑 Hecho con amor para parejas que quieren conectar mejor
