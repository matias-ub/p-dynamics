# 💑 Parejas - Daily Question Game

A daily question game for couples to connect, understand each other better, and maintain consistency in their relationship through engaging daily prompts.

## 🎯 Concept

Every day, both partners answer a simple question and predict what their partner will choose. The app tracks:
- ✅ Whether predictions match reality (how well you know your partner)
- 🔥 Streak of consecutive days both have answered
- 📊 History of all responses

## ✨ Features

- 🎲 **Daily Questions**: One new question per day with multiple-choice answers
- 🤝 **Room System**: Create a private room and share a code with your partner
- 👤 **Anonymous Auth**: No registration required - just create and join
- 📈 **Streak Tracking**: Maintain your couple's daily answering streak
- 🎨 **Beautiful UI**: Responsive design with Bootstrap 5 and gradient themes
- ⚡ **HTMX Integration**: Smooth interactions without page reloads

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: Supabase (Postgres + Auth)
- **Frontend**: Jinja2 Templates + Bootstrap 5 + HTMX
- **Auth**: Supabase Anonymous Authentication

### Project Structure
```
p-dynamics/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Environment configuration
│   ├── dependencies.py      # Auth dependencies
│   ├── models.py            # Pydantic models
│   │
│   ├── routes/              # Route handlers
│   │   ├── pages.py         # SSR page routes
│   │   ├── auth.py          # Auth API endpoints
│   │   ├── rooms.py         # Room management
│   │   ├── questions.py     # Daily questions
│   │   └── responses.py     # User responses
│   │
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py
│   │   ├── room_service.py
│   │   ├── question_service.py
│   │   └── response_service.py
│   │
│   ├── utils/               # Utilities
│   │   └── supabase.py      # Supabase client
│   │
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── create_room.html
│   │   ├── join_room.html
│   │   ├── dashboard.html
│   │   ├── question.html
│   │   └── results.html
│   │
│   └── static/              # Static assets
│       └── css/
│           └── style.css
│
├── supabase/
│   └── migrations/
│       ├── 001_initial_schema.sql
│       └── 002_seed_data.sql
│
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Supabase account (free tier works)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/matias-ub/p-dynamics.git
cd p-dynamics
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
DEBUG=false
```

5. **Set up Supabase**

- Create a new Supabase project
- Run the migrations in order:
  1. Execute `supabase/migrations/001_initial_schema.sql` in SQL Editor
  2. Execute `supabase/migrations/002_seed_data.sql` in SQL Editor
- Enable anonymous auth in Authentication settings

6. **Run the application**
```bash
uvicorn app.main:app --reload
```

The app will be available at `http://localhost:8000`

## 📖 How to Use

### For the First Partner (Room Creator)
1. Go to the home page
2. Click "Crear Room"
3. Share the generated code with your partner

### For the Second Partner (Joining)
1. Go to the home page
2. Click "Unirse con Código"
3. Enter the code shared by your partner
4. You're in!

### Daily Flow
1. Visit your room's dashboard
2. Click "Responder Ahora" when today's question is available
3. Answer what YOU would choose
4. Predict what YOUR PARTNER will choose
5. Check back later to see if your predictions matched!

## 🗄️ Database Schema

### Tables
- **profiles**: User profiles (auto-created from auth.users)
- **questions**: Pool of questions with intensity levels
- **options**: Multiple-choice options for each question
- **daily_questions**: Maps questions to specific dates
- **rooms**: Private rooms for couples (with unique tokens)
- **responses**: User answers and partner predictions

### Key Features
- **Row Level Security (RLS)**: Enforces data privacy
- **Anonymous Auth**: Users don't need email/password
- **Streak Calculation**: On-the-fly calculation from responses
- **Unique Constraints**: One response per user per day per room

## 🔐 Authentication Flow

1. User creates or joins a room
2. Anonymous Supabase user is created automatically
3. JWT token is stored in cookie
4. All API calls include token for RLS enforcement
5. Users can optionally convert to permanent accounts (future feature)

## 🌟 API Endpoints

### Pages (SSR)
- `GET /` - Landing page
- `GET /create-room` - Create room page
- `GET /join-room` - Join room page
- `GET /dashboard/{room_id}` - Room dashboard
- `GET /question/{room_id}` - Answer today's question
- `GET /results/{room_id}` - View results and history

### API (JSON)
- `POST /api/auth/anonymous` - Create anonymous user
- `POST /api/rooms` - Create new room
- `GET /api/rooms/{token}` - Get room by token
- `GET /api/questions/today` - Get today's daily question
- `POST /api/responses` - Submit answer
- `GET /api/responses/room/{room_id}` - Get room responses
- `GET /api/responses/room/{room_id}/streak` - Get streak

## 🎨 Customization

### Adding New Questions
Edit `supabase/migrations/002_seed_data.sql` and add:
```sql
WITH q AS (
  INSERT INTO public.questions (text, intensity_level) 
  VALUES ('Your question here?', 3)
  RETURNING id
)
INSERT INTO public.daily_questions (question_id, date)
SELECT id, 'YYYY-MM-DD' FROM q;

INSERT INTO public.options (question_id, text, position)
SELECT q.id, opt.text, opt.pos
FROM public.questions q, (VALUES 
  (1, 'Option 1'),
  (2, 'Option 2'),
  (3, 'Option 3')
) AS opt(pos, text)
WHERE q.text = 'Your question here?';
```

### Styling
Edit `app/static/css/style.css` to customize colors, gradients, and animations.

## 🚢 Deployment

### Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### Environment Variables
Remember to set these in your deployment platform:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

## 🛣️ Roadmap

- [ ] Email/password authentication option
- [ ] Convert anonymous users to permanent accounts
- [ ] Share results on social media
- [ ] Weekly/monthly reports
- [ ] Custom question packs
- [ ] Couple statistics and insights
- [ ] Multi-language support
- [ ] Mobile app (React Native)

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

**Matias** - [@matias-ub](https://github.com/matias-ub)

Project Link: [https://github.com/matias-ub/p-dynamics](https://github.com/matias-ub/p-dynamics)

---

Made with ❤️ for couples who want to connect better
```

2. Abre tu navegador en `http://localhost:8000`

3. Accede a la documentación interactiva en `http://localhost:8000/docs`

4. Crea una cuenta o inicia sesión

5. Completa el test

6. Visualiza tus resultados

## Desarrollo

### Agregar nuevos escenarios

Edita el archivo `p_dynamics/lib/scenarios.py` y agrega nuevos escenarios siguiendo la estructura existente:

```python
{
    "id": 4,
    "title": "Nuevo Escenario",
    "description": "Descripción del escenario",
    "questions": [
        {
            "id": "q4_1",
            "text": "¿Pregunta del escenario?",
            "options": [
                {
                    "text": "Opción 1",
                    "tags": {"dimension1": 8, "dimension2": 5}
                },
                # ... más opciones
            ]
        }
        # 4 preguntas por escenario
    ]
}
```

### Modificar templates

Los templates Jinja2 están en `app/templates/`. Cada template extiende de `base.html`.

### Agregar nuevas rutas

Crea nuevos archivos en `app/routes/` y regístralos en `app/main.py`:

```python
from .routes import nueva_ruta

app.include_router(nueva_ruta.router, prefix="/ruta", tags=["tag"])
```

### Configuración de Supabase

El schema de la base de datos está en `supabase/migrations/001_initial_schema.sql`. Puedes ejecutarlo directamente en el SQL Editor de Supabase.

**Nota:** Para el MVP actual, las sesiones de test se almacenan en memoria. Para producción, se recomienda usar Redis o guardar en base de datos.

**Tablas principales:**
- `profiles` - Extensión de auth.users con datos del perfil
- `couples` - Relación de parejas con invite_code
- `scenario_packs` - Paquetes de escenarios versionados
- `scenarios` - Escenarios individuales
- `scenario_options` - Opciones de respuesta por escenario
- `tests` - Instancias de tests realizados
- `responses` - Respuestas de usuarios (4 perspectivas por escenario)

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido
- [Jinja2](https://jinja.palletsprojects.com/) - Motor de templates
- [HTMX](https://htmx.org/) - Interactividad HTML moderna
- [Bootstrap 5](https://getbootstrap.com/) - Framework CSS
- [Supabase](https://supabase.com/) - Backend as a Service
- [Plotly](https://plotly.com/) - Visualización de datos (futuro)
- Python 3.8+

## Próximos Pasos

- [ ] Persistencia de sesiones en Redis/Base de datos
- [ ] Sistema de parejas funcional (invitaciones)
- [ ] Comparación de resultados entre parejas
- [ ] Gráficos radar con Plotly
- [ ] Verificación de email
- [ ] Despliegue a producción

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Matias - [@matias-ub](https://github.com/matias-ub)

Proyecto: [https://github.com/matias-ub/p-dynamics](https://github.com/matias-ub/p-dynamics)
