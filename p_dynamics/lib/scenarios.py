"""Test scenarios and questions for the couples assessment."""
from typing import Optional, List, Dict
import copy
import logging

from .supabase_client import get_supabase_client

# Configure logging
logging.basicConfig(level=logging.INFO)
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
                    "Actividades al aire libre",
                    "Ver películas/series en casa",
                    "Salir con amigos",
                    "Leer o actividades tranquilas"
                ]
            },
            {
                "id": "q1_2",
                "text": "¿Qué creo que mi pareja prefiere hacer?",
                "options": [
                    "Actividades al aire libre",
                    "Ver películas/series en casa",
                    "Salir con amigos",
                    "Leer o actividades tranquilas"
                ]
            },
            {
                "id": "q1_3",
                "text": "¿Qué es lo más justo para ambos?",
                "options": [
                    "Actividades al aire libre",
                    "Ver películas/series en casa",
                    "Salir con amigos",
                    "Leer o actividades tranquilas"
                ]
            },
            {
                "id": "q1_4",
                "text": "¿Qué creo que mi pareja considera lo mejor para la relación?",
                "options": [
                    "Actividades al aire libre",
                    "Ver películas/series en casa",
                    "Salir con amigos",
                    "Leer o actividades tranquilas"
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
                    "Cuentas completamente separadas",
                    "Cuenta conjunta para gastos comunes",
                    "Todo en cuentas conjuntas",
                    "Sistema proporcional según ingresos"
                ]
            },
            {
                "id": "q2_2",
                "text": "¿Qué creo que mi pareja prefiere?",
                "options": [
                    "Cuentas completamente separadas",
                    "Cuenta conjunta para gastos comunes",
                    "Todo en cuentas conjuntas",
                    "Sistema proporcional según ingresos"
                ]
            },
            {
                "id": "q2_3",
                "text": "¿Qué es lo más justo para ambos?",
                "options": [
                    "Cuentas completamente separadas",
                    "Cuenta conjunta para gastos comunes",
                    "Todo en cuentas conjuntas",
                    "Sistema proporcional según ingresos"
                ]
            },
            {
                "id": "q2_4",
                "text": "¿Qué creo que mi pareja considera lo mejor para la relación?",
                "options": [
                    "Cuentas completamente separadas",
                    "Cuenta conjunta para gastos comunes",
                    "Todo en cuentas conjuntas",
                    "Sistema proporcional según ingresos"
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
                    "Hablarlo inmediatamente",
                    "Tomar tiempo para pensar",
                    "Buscar compromiso rápido",
                    "Evitar el conflicto"
                ]
            },
            {
                "id": "q3_2",
                "text": "¿Qué creo que mi pareja prefiere?",
                "options": [
                    "Hablarlo inmediatamente",
                    "Tomar tiempo para pensar",
                    "Buscar compromiso rápido",
                    "Evitar el conflicto"
                ]
            },
            {
                "id": "q3_3",
                "text": "¿Qué es lo más justo para ambos?",
                "options": [
                    "Hablarlo inmediatamente",
                    "Tomar tiempo para pensar",
                    "Buscar compromiso rápido",
                    "Evitar el conflicto"
                ]
            },
            {
                "id": "q3_4",
                "text": "¿Qué creo que mi pareja considera lo mejor para la relación?",
                "options": [
                    "Hablarlo inmediatamente",
                    "Tomar tiempo para pensar",
                    "Buscar compromiso rápido",
                    "Evitar el conflicto"
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
        
        # 3. Para cada escenario, obtener sus opciones ordenadas
        for scenario in scenarios_data:
            scenario_id = scenario["id"]
            
            logger.debug(f"Obteniendo opciones para escenario: {scenario['key']}")
            options_response = supabase.table("scenario_options")\
                .select("key, text, tags, order_num, is_positive")\
                .eq("scenario_id", scenario_id)\
                .order("order_num")\
                .execute()
            
            # Agregar las opciones al escenario
            scenario["options"] = options_response.data if options_response.data else []
            logger.debug(f"Escenario '{scenario['key']}': {len(scenario['options'])} opciones cargadas")
        
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
