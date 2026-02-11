# 4 Perspectivas para Parejas

Test interactivo para parejas que compara deseos personales, percepción del otro, equidad objetiva y percepción mutua de lo "mejor para la relación". Calcula scores de alineación, empatía y salud relacional.

## Descripción

Este proyecto es una aplicación web construida con [Reflex](https://reflex.dev/) que ayuda a las parejas a entender mejor su relación a través de un test de 4 perspectivas:

1. **Perspectiva Personal**: ¿Qué prefiero yo?
2. **Perspectiva Empática**: ¿Qué creo que prefiere mi pareja?
3. **Perspectiva de Equidad**: ¿Qué es lo más justo para ambos?
4. **Perspectiva Relacional**: ¿Qué creo que mi pareja considera mejor para la relación?

## Características

- ✅ Autenticación de usuarios con Supabase
- ✅ Test interactivo con múltiples escenarios
- ✅ Sistema de invitación para parejas
- ✅ Cálculo automático de scores:
  - Score de Alineación
  - Score de Empatía
  - Score de Salud Relacional
- ✅ Visualización de resultados con gráficos radar
- ✅ Interfaz responsive y moderna

## Estructura del Proyecto

```
4-perspectivas-pareja-py/
├── rxconfig.py              # Configuración de Reflex
├── .reflex/                 # Directorio de Reflex (generado)
├── assets/                  # Archivos estáticos
├── pages/                   # Páginas de la aplicación
│   ├── __init__.py
│   ├── index.py            # Página de inicio
│   ├── login.py            # Login/registro
│   ├── test.py             # Test interactivo
│   ├── results.py          # Resultados
│   └── invite.py           # Invitación a pareja
├── components/              # Componentes reutilizables
│   ├── __init__.py
│   ├── scenario_card.py    # Tarjeta de escenario
│   ├── question.py         # Componente de pregunta
│   ├── radar_chart.py      # Gráfico radar
│   └── couple_invite.py    # Componente de invitación
├── state/                   # Gestión de estado
│   ├── __init__.py
│   ├── auth_state.py       # Estado de autenticación
│   ├── test_state.py       # Estado del test
│   └── scoring.py          # Cálculos de scores
├── lib/                     # Utilidades
│   ├── supabase_client.py  # Cliente de Supabase
│   └── scenarios.py        # Escenarios del test
├── requirements.txt         # Dependencias Python
├── .env                     # Variables de entorno
└── README.md               # Este archivo
```

## Requisitos

- Python 3.8 o superior
- pip
- Cuenta de Supabase (para autenticación y base de datos)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/matias-ub/p-dynamics.git
cd p-dynamics/4-perspectivas-pareja-py
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
- Copia el archivo `.env` y completa con tus credenciales de Supabase:
```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_de_supabase
```

4. Inicializa Reflex:
```bash
reflex init
```

## Uso

1. Inicia el servidor de desarrollo:
```bash
reflex run
```

2. Abre tu navegador en `http://localhost:3000`

3. Crea una cuenta o inicia sesión

4. Completa el test y comparte el enlace con tu pareja

5. Una vez que ambos hayan completado el test, visualiza los resultados

## Desarrollo

### Agregar nuevos escenarios

Edita el archivo `lib/scenarios.py` y agrega nuevos escenarios siguiendo la estructura existente:

```python
{
    "id": 4,
    "title": "Nuevo Escenario",
    "description": "Descripción del escenario",
    "questions": [
        # 4 preguntas por escenario
    ]
}
```

### Modificar componentes

Los componentes se encuentran en el directorio `components/`. Cada componente es una función que retorna un `rx.Component`.

### Configuración de Supabase

Asegúrate de crear las siguientes tablas en tu base de datos de Supabase:
- `users` - Para almacenar información de usuarios
- `couples` - Para relacionar parejas
- `test_responses` - Para guardar respuestas del test

## Tecnologías

- [Reflex](https://reflex.dev/) - Framework web de Python
- [Supabase](https://supabase.com/) - Backend as a Service
- [Plotly](https://plotly.com/) - Visualización de datos
- Python 3.8+

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
