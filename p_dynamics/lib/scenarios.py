"""Test scenarios and questions for the couples assessment."""
from typing import Optional, List, Dict
import copy

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

def get_scenarios() -> List[Dict]:
    """Return all test scenarios.
    
    Returns a deep copy to prevent modifications to the original data.
    """
    return copy.deepcopy(SCENARIOS)

def get_scenario_by_id(scenario_id: int) -> Optional[Dict]:
    """Get a specific scenario by its ID.
    
    Returns a deep copy to prevent modifications to the original data.
    """
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return copy.deepcopy(scenario)
    return None
