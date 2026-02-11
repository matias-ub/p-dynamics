"""Test scenarios and questions for the couples assessment."""
from typing import Optional, List, Dict

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

def get_scenarios() -> List[Dict]:
    """Return all test scenarios.
    
    Note: Returns a reference to the module-level SCENARIOS list.
    Callers should not modify the returned list directly.
    """
    return SCENARIOS

def get_scenario_by_id(scenario_id: int) -> Optional[Dict]:
    """Get a specific scenario by its ID.
    
    Note: Returns a reference to a scenario dict from SCENARIOS.
    Callers should not modify the returned dict directly.
    """
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    return None
