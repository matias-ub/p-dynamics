"""Test scenarios and questions for the couples assessment."""
from typing import Optional, List, Dict
import copy
import logging

from .supabase_client import get_supabase_client

logger = logging.getLogger(__name__)
# DEPRECATED: Hardcoded scenarios kept as fallback only
# Este data hardcoded será reemplazado por consultas dinámicas a Supabase
# usando la función get_scenarios_from_db()
SCENARIOS = [
    {
        "id": 1,
        "title": "Tiempo Libre",
        "description": "¿Cómo prefieren pasar el tiempo libre juntos?",
        "questions": [
            {
                "id": "q1_1",
                "text": "¿Qué prefiero hacer en mi tiempo libre?",
                "options": [
                    {
                        "text": "Actividades al aire libre",
                        "tags": {"sociabilidad": 7, "energia": 9, "aventura": 8, "intimidad": 6, "autonomia": 5}
                    },
                    {
                        "text": "Ver películas/series en casa",
                        "tags": {"sociabilidad": 4, "energia": 3, "aventura": 2, "intimidad": 9, "autonomia": 6}
                    },
                    {
                        "text": "Salir con amigos",
                        "tags": {"sociabilidad": 10, "energia": 8, "aventura": 7, "intimidad": 3, "autonomia": 4}
                    },
                    {
                        "text": "Leer o actividades tranquilas",
                        "tags": {"sociabilidad": 2, "energia": 2, "aventura": 1, "intimidad": 7, "autonomia": 9}
                    }
                ]
            },
            {
                "id": "q1_2",
                "text": "¿Qué creo que mi pareja prefiere hacer?",
                "options": [
                    {
                        "text": "Actividades al aire libre",
                        "tags": {"sociabilidad": 7, "energia": 9, "aventura": 8, "intimidad": 6, "autonomia": 5}
                    },
                    {
                        "text": "Ver películas/series en casa",
                        "tags": {"sociabilidad": 4, "energia": 3, "aventura": 2, "intimidad": 9, "autonomia": 6}
                    },
                    {
                        "text": "Salir con amigos",
                        "tags": {"sociabilidad": 10, "energia": 8, "aventura": 7, "intimidad": 3, "autonomia": 4}
                    },
                    {
                        "text": "Leer o actividades tranquilas",
                        "tags": {"sociabilidad": 2, "energia": 2, "aventura": 1, "intimidad": 7, "autonomia": 9}
                    }
                ]
            },
            {
                "id": "q1_3",
                "text": "¿Qué es lo más justo para ambos?",
                "options": [
                    {
                        "text": "Actividades al aire libre",
                        "tags": {"sociabilidad": 7, "energia": 9, "aventura": 8, "intimidad": 6, "autonomia": 5}
                    },
                    {
                        "text": "Ver películas/series en casa",
                        "tags": {"sociabilidad": 4, "energia": 3, "aventura": 2, "intimidad": 9, "autonomia": 6}
                    },
                    {
                        "text": "Salir con amigos",
                        "tags": {"sociabilidad": 10, "energia": 8, "aventura": 7, "intimidad": 3, "autonomia": 4}
                    },
                    {
                        "text": "Leer o actividades tranquilas",
                        "tags": {"sociabilidad": 2, "energia": 2, "aventura": 1, "intimidad": 7, "autonomia": 9}
                    }
                ]
            },
            {
                "id": "q1_4",
                "text": "¿Qué creo que mi pareja considera lo mejor para la relación?",
                "options": [
                    {
                        "text": "Actividades al aire libre",
                        "tags": {"sociabilidad": 7, "energia": 9, "aventura": 8, "intimidad": 6, "autonomia": 5}
                    },
                    {
                        "text": "Ver películas/series en casa",
                        "tags": {"sociabilidad": 4, "energia": 3, "aventura": 2, "intimidad": 9, "autonomia": 6}
                    },
                    {
                        "text": "Salir con amigos",
                        "tags": {"sociabilidad": 10, "energia": 8, "aventura": 7, "intimidad": 3, "autonomia": 4}
                    },
                    {
                        "text": "Leer o actividades tranquilas",
                        "tags": {"sociabilidad": 2, "energia": 2, "aventura": 1, "intimidad": 7, "autonomia": 9}
                    }
                ]
            }
        ]
    },
    {
        "id": 2,
        "title": "Finanzas",
        "description": "¿Cómo manejar el dinero en la relación?",
        "questions": [
            {
                "id": "q2_1",
                "text": "¿Cómo prefiero manejar las finanzas?",
                "options": [
                    {
                        "text": "Cuentas completamente separadas",
                        "tags": {"independencia": 10, "confianza": 4, "autonomia": 9, "colaboracion": 2, "transparencia": 5}
                    },
                    {
                        "text": "Cuenta conjunta para gastos comunes",
                        "tags": {"independencia": 6, "confianza": 7, "autonomia": 6, "colaboracion": 7, "transparencia": 8}
                    },
                    {
                        "text": "Todo en cuentas conjuntas",
                        "tags": {"independencia": 2, "confianza": 10, "autonomia": 3, "colaboracion": 10, "transparencia": 10}
                    },
                    {
                        "text": "Sistema proporcional según ingresos",
                        "tags": {"independencia": 5, "confianza": 8, "autonomia": 5, "colaboracion": 9, "transparencia": 9, "equidad": 10}
                    }
                ]
            },
            {
                "id": "q2_2",
                "text": "¿Qué creo que mi pareja prefiere?",
                "options": [
                    {
                        "text": "Cuentas completamente separadas",
                        "tags": {"independencia": 10, "confianza": 4, "autonomia": 9, "colaboracion": 2, "transparencia": 5}
                    },
                    {
                        "text": "Cuenta conjunta para gastos comunes",
                        "tags": {"independencia": 6, "confianza": 7, "autonomia": 6, "colaboracion": 7, "transparencia": 8}
                    },
                    {
                        "text": "Todo en cuentas conjuntas",
                        "tags": {"independencia": 2, "confianza": 10, "autonomia": 3, "colaboracion": 10, "transparencia": 10}
                    },
                    {
                        "text": "Sistema proporcional según ingresos",
                        "tags": {"independencia": 5, "confianza": 8, "autonomia": 5, "colaboracion": 9, "transparencia": 9, "equidad": 10}
                    }
                ]
            },
            {
                "id": "q2_3",
                "text": "¿Qué es lo más justo para ambos?",
                "options": [
                    {
                        "text": "Cuentas completamente separadas",
                        "tags": {"independencia": 10, "confianza": 4, "autonomia": 9, "colaboracion": 2, "transparencia": 5}
                    },
                    {
                        "text": "Cuenta conjunta para gastos comunes",
                        "tags": {"independencia": 6, "confianza": 7, "autonomia": 6, "colaboracion": 7, "transparencia": 8}
                    },
                    {
                        "text": "Todo en cuentas conjuntas",
                        "tags": {"independencia": 2, "confianza": 10, "autonomia": 3, "colaboracion": 10, "transparencia": 10}
                    },
                    {
                        "text": "Sistema proporcional según ingresos",
                        "tags": {"independencia": 5, "confianza": 8, "autonomia": 5, "colaboracion": 9, "transparencia": 9, "equidad": 10}
                    }
                ]
            },
            {
                "id": "q2_4",
                "text": "¿Qué creo que mi pareja considera lo mejor para la relación?",
                "options": [
                    {
                        "text": "Cuentas completamente separadas",
                        "tags": {"independencia": 10, "confianza": 4, "autonomia": 9, "colaboracion": 2, "transparencia": 5}
                    },
                    {
                        "text": "Cuenta conjunta para gastos comunes",
                        "tags": {"independencia": 6, "confianza": 7, "autonomia": 6, "colaboracion": 7, "transparencia": 8}
                    },
                    {
                        "text": "Todo en cuentas conjuntas",
                        "tags": {"independencia": 2, "confianza": 10, "autonomia": 3, "colaboracion": 10, "transparencia": 10}
                    },
                    {
                        "text": "Sistema proporcional según ingresos",
                        "tags": {"independencia": 5, "confianza": 8, "autonomia": 5, "colaboracion": 9, "transparencia": 9, "equidad": 10}
                    }
                ]
            }
        ]
    },
    {
        "id": 3,
        "title": "Comunicación",
        "description": "¿Cómo resolver conflictos?",
        "questions": [
            {
                "id": "q3_1",
                "text": "¿Cómo prefiero resolver conflictos?",
                "options": [
                    {
                        "text": "Hablarlo inmediatamente",
                        "tags": {"confrontacion": 9, "urgencia": 10, "apertura": 9, "reflexion": 3, "resolucion": 8}
                    },
                    {
                        "text": "Tomar tiempo para pensar",
                        "tags": {"confrontacion": 4, "urgencia": 2, "apertura": 6, "reflexion": 10, "resolucion": 6}
                    },
                    {
                        "text": "Buscar compromiso rápido",
                        "tags": {"confrontacion": 6, "urgencia": 7, "apertura": 7, "reflexion": 5, "resolucion": 10}
                    },
                    {
                        "text": "Evitar el conflicto",
                        "tags": {"confrontacion": 1, "urgencia": 1, "apertura": 2, "reflexion": 4, "resolucion": 2}
                    }
                ]
            },
            {
                "id": "q3_2",
                "text": "¿Qué creo que mi pareja prefiere?",
                "options": [
                    {
                        "text": "Hablarlo inmediatamente",
                        "tags": {"confrontacion": 9, "urgencia": 10, "apertura": 9, "reflexion": 3, "resolucion": 8}
                    },
                    {
                        "text": "Tomar tiempo para pensar",
                        "tags": {"confrontacion": 4, "urgencia": 2, "apertura": 6, "reflexion": 10, "resolucion": 6}
                    },
                    {
                        "text": "Buscar compromiso rápido",
                        "tags": {"confrontacion": 6, "urgencia": 7, "apertura": 7, "reflexion": 5, "resolucion": 10}
                    },
                    {
                        "text": "Evitar el conflicto",
                        "tags": {"confrontacion": 1, "urgencia": 1, "apertura": 2, "reflexion": 4, "resolucion": 2}
                    }
                ]
            },
            {
                "id": "q3_3",
                "text": "¿Qué es lo más justo para ambos?",
                "options": [
                    {
                        "text": "Hablarlo inmediatamente",
                        "tags": {"confrontacion": 9, "urgencia": 10, "apertura": 9, "reflexion": 3, "resolucion": 8}
                    },
                    {
                        "text": "Tomar tiempo para pensar",
                        "tags": {"confrontacion": 4, "urgencia": 2, "apertura": 6, "reflexion": 10, "resolucion": 6}
                    },
                    {
                        "text": "Buscar compromiso rápido",
                        "tags": {"confrontacion": 6, "urgencia": 7, "apertura": 7, "reflexion": 5, "resolucion": 10}
                    },
                    {
                        "text": "Evitar el conflicto",
                        "tags": {"confrontacion": 1, "urgencia": 1, "apertura": 2, "reflexion": 4, "resolucion": 2}
                    }
                ]
            },
            {
                "id": "q3_4",
                "text": "¿Qué creo que mi pareja considera lo mejor para la relación?",
                "options": [
                    {
                        "text": "Hablarlo inmediatamente",
                        "tags": {"confrontacion": 9, "urgencia": 10, "apertura": 9, "reflexion": 3, "resolucion": 8}
                    },
                    {
                        "text": "Tomar tiempo para pensar",
                        "tags": {"confrontacion": 4, "urgencia": 2, "apertura": 6, "reflexion": 10, "resolucion": 6}
                    },
                    {
                        "text": "Buscar compromiso rápido",
                        "tags": {"confrontacion": 6, "urgencia": 7, "apertura": 7, "reflexion": 5, "resolucion": 10}
                    },
                    {
                        "text": "Evitar el conflicto",
                        "tags": {"confrontacion": 1, "urgencia": 1, "apertura": 2, "reflexion": 4, "resolucion": 2}
                    }
                ]
            }
        ]
    }
]

async def get_scenarios(pack_name: str = "cotidiano-v1") -> List[Dict]:
    """
    Devuelve lista de escenarios para el pack indicado desde Supabase.
    
    Nota: Esta función es async para compatibilidad con código asíncrono,
    aunque internamente usa el cliente sincrónico de Supabase.
    
    Args:
        pack_name: Nombre del pack de escenarios (default: "cotidiano-v1")
    
    Returns:
        Lista de escenarios, cada uno con estructura:
        {
            'key': str,               # ej: 'platos-sucios'
            'title': str,             # Título del escenario
            'description': str,       # Descripción del escenario
            'order_num': int,         # Orden de presentación
            'options': list[dict]     # Lista de opciones disponibles
        }
        
        Cada opción tiene estructura:
        {
            'key': str,           # ej: 'A', 'B', 'C'
            'text': str,          # Texto de la opción
            'tags': dict,         # Tags/dimensiones para scoring
            'order_num': int,     # Orden de presentación
            'is_positive': bool   # Si es una opción positiva
        }
    
    Raises:
        ValueError: Si el pack no existe en la base de datos
        Exception: Si hay errores en las consultas a Supabase
    
    Example:
        scenarios = await get_scenarios("cotidiano-v1")
        for scenario in scenarios:
            print(f"{scenario['title']}: {len(scenario['options'])} options")
    """
    try:
        # Obtener cliente de Supabase (sincrónico)
        supabase = get_supabase_client()
        
        # 1. Obtener el pack_id
        logger.info(f"Buscando pack: {pack_name}")
        pack_response = supabase.table("scenario_packs")\
            .select("id")\
            .eq("name", pack_name)\
            .single()\
            .execute()
        
        # Verificar que se encontró el pack
        if not pack_response.data:
            error_msg = f"Pack '{pack_name}' no encontrado en la base de datos"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        pack_id = pack_response.data["id"]
        logger.info(f"Pack encontrado con ID: {pack_id}")
        
        # 2. Obtener escenarios del pack ordenados
        logger.info(f"Obteniendo escenarios para pack_id: {pack_id}")
        scenarios_response = supabase.table("scenarios")\
            .select("id, key, title, description, order_num")\
            .eq("pack_id", pack_id)\
            .order("order_num")\
            .execute()
        
        if not scenarios_response.data:
            logger.warning(f"No se encontraron escenarios para el pack {pack_name}")
            return []
        
        scenarios_data = scenarios_response.data
        logger.info(f"Encontrados {len(scenarios_data)} escenarios")
        
        # 3. Obtener todas las opciones de todos los escenarios en una sola consulta
        scenario_ids = [scenario["id"] for scenario in scenarios_data]
        logger.info(f"Obteniendo opciones para {len(scenario_ids)} escenarios en una sola consulta")

        options_response = supabase.table("scenario_options")\
            .select("scenario_id, key, text, tags, order_num, is_positive")\
            .in_("scenario_id", scenario_ids)\
            .order("scenario_id")\
            .order("order_num")\
            .execute()

        options_data = options_response.data or []
        logger.info(f"Encontradas {len(options_data)} opciones en total")

        # Agrupar opciones por escenario_id
        options_by_scenario_id: Dict[int, List[dict]] = {}
        for option in options_data:
            sid = option["scenario_id"]
            if sid not in options_by_scenario_id:
                options_by_scenario_id[sid] = []
            options_by_scenario_id[sid].append({
                "key": option["key"],
                "text": option["text"],
                "tags": option.get("tags"),
                "order_num": option["order_num"],
                "is_positive": option.get("is_positive"),
            })

        # Asignar opciones agrupadas a cada escenario
        for scenario in scenarios_data:
            sid = scenario["id"]
            scenario_options = options_by_scenario_id.get(sid, [])
            scenario["options"] = scenario_options
            logger.debug(f"Escenario '{scenario['key']}': {len(scenario_options)} opciones cargadas")
        
        logger.info(f"✓ Carga completa: {len(scenarios_data)} escenarios con sus opciones")
        return scenarios_data
        
    except ValueError:
        # Re-raise ValueError (pack no encontrado)
        raise
    except Exception as e:
        error_msg = f"Error al cargar escenarios desde Supabase: {str(e)}"
        logger.exception(error_msg)
        raise


# DEPRECATED FUNCTIONS - Mantenidas para compatibilidad temporal
def get_scenarios_legacy() -> List[Dict]:
    """Return all test scenarios (DEPRECATED - usar get_scenarios() asíncrona).
    
    Returns a deep copy to prevent modifications to the original data.
    """
    logger.warning("get_scenarios_legacy() está deprecada, usa get_scenarios() asíncrona")
    return copy.deepcopy(SCENARIOS)

def get_scenario_by_id(scenario_id: int) -> Optional[Dict]:
    """Get a specific scenario by its ID (DEPRECATED).
    
    Returns a deep copy to prevent modifications to the original data.
    """
    logger.warning("get_scenario_by_id() está deprecada")
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return copy.deepcopy(scenario)
    return None
