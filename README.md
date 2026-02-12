# P Dynamics - 4 Perspectivas para Parejas

Test interactivo para parejas que compara deseos personales, percepción del otro, equidad objetiva y percepción mutua de lo "mejor para la relación". Calcula scores de alineación, empatía y salud relacional.

## Descripción

Aplicación web construida con **FastAPI**, **Jinja2** y **HTMX** que ayuda a las parejas a entender mejor su relación a través de un test de 4 perspectivas:

1. **Perspectiva Personal**: ¿Qué prefiero yo?
2. **Perspectiva Empática**: ¿Qué creo que prefiere mi pareja?
3. **Perspectiva de Equidad**: ¿Qué es lo más justo para ambos?
4. **Perspectiva Relacional**: ¿Qué creo que mi pareja considera mejor para la relación?

## Características

- 🔐 Autenticación de usuarios con Supabase
- 📝 Test interactivo con múltiples escenarios
- 👥 Sistema de invitación para parejas
- 📊 Cálculo automático de scores:
  - Score de Alineación
  - Score de Empatía
  - Score de Salud Relacional
- 📈 Visualización de resultados con dimensiones
- 📱 Interfaz responsive con Bootstrap
- ⚡ HTMX para interactividad sin JavaScript complejo

## Estructura del Proyecto

```
p-dynamics/
├── app/                     # Aplicación FastAPI
│   ├── main.py             # Punto de entrada de la aplicación
│   ├── routes/             # Rutas de la API
│   │   ├── auth.py         # Login/registro
│   │   ├── test.py         # Test interactivo
│   │   └── results.py      # Resultados
│   ├── templates/          # Templates Jinja2
│   │   ├── base.html       # Template base
│   │   ├── login.html      # Página de login
│   │   ├── test.html       # Página del test
│   │   └── results.html    # Página de resultados
│   └── static/             # Archivos estáticos
│       └── css/
│           └── style.css   # Estilos personalizados
├── p_dynamics/             # Lógica de negocio
│   └── lib/                # Utilidades
│       ├── supabase_client.py  # Cliente de Supabase
│       └── scenarios.py    # Escenarios del test
├── supabase/               # Configuración de Supabase
│   └── migrations/         # Migraciones SQL
│       └── 001_initial_schema.sql
├── requirements-fastapi.txt # Dependencias FastAPI
├── .env.example            # Variables de entorno de ejemplo
└── README.md               # Este archivo
```

## Requisitos

- Python 3.8 o superior
- pip o [uv](https://github.com/astral-sh/uv) (recomendado)
- Cuenta de Supabase (para autenticación y base de datos)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/matias-ub/p-dynamics.git
cd p-dynamics
```

2. Crea un entorno virtual con uv (recomendado):
```bash
uv venv
```

3. Instala las dependencias:
```bash
# Con uv (recomendado)
uv pip install -r requirements-fastapi.txt

# O con pip tradicional
pip install -r requirements-fastapi.txt
```

4. Configura las variables de entorno:
- Copia el archivo `.env.example` a `.env` y completa con tus credenciales de Supabase:
```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_de_supabase
```

## Uso

1. Inicia el servidor de desarrollo:
```bash
# Con uv
uv run uvicorn app.main:app --reload

# O directamente con uvicorn
uvicorn app.main:app --reload
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
