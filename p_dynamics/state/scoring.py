"""Scoring calculations for test results."""
import math
import reflex as rx
from typing import Dict, List, Any, Tuple


def calculate_similarity(tags1: Dict[str, float], tags2: Dict[str, float]) -> float:
    """
    Calcula la similitud entre dos conjuntos de tags usando distancia euclidiana normalizada.
    
    Args:
        tags1: Diccionario de tags con valores numéricos (ej: {"generosidad": 8, "equidad": 6})
        tags2: Diccionario de tags con valores numéricos
        
    Returns:
        float: Score de similitud de 0 a 100 (100 = idénticos, 0 = máxima diferencia)
        
    La fórmula usa distancia euclidiana normalizada:
    - Calcula la distancia euclidiana entre los vectores de tags
    - Normaliza por la máxima distancia posible (asumiendo rango 0-10)
    - Convierte a porcentaje de similitud (100 - distancia_normalizada)
    """
    if not tags1 or not tags2:
        return 0.0
    
    # Obtener todas las keys únicas de ambos dicts
    all_keys = set(tags1.keys()) | set(tags2.keys())
    
    if not all_keys:
        return 0.0
    
    # Calcular distancia euclidiana
    sum_squared_diff = 0.0
    for key in all_keys:
        val1 = tags1.get(key, 0)
        val2 = tags2.get(key, 0)
        sum_squared_diff += (val1 - val2) ** 2
    
    euclidean_distance = math.sqrt(sum_squared_diff)
    
    # Normalizar: la máxima distancia posible asumiendo valores 0-10
    # Para n dimensiones, max_distance = sqrt(n * 10^2) = sqrt(n) * 10
    max_possible_distance = math.sqrt(len(all_keys)) * 10
    
    # Evitar división por cero
    if max_possible_distance == 0:
        return 100.0
    
    # Convertir distancia a similitud (0-100)
    normalized_distance = (euclidean_distance / max_possible_distance) * 100
    similarity = 100 - normalized_distance
    
    # Asegurar que esté en el rango [0, 100]
    return max(0.0, min(100.0, similarity))


def calculate_scores(responses_a: Dict[str, int], responses_b: Dict[str, int]) -> Dict[str, Any]:
    """
    Calcula los scores completos de la pareja basados en sus respuestas.
    
    Args:
        responses_a: Respuestas del participante A. 
                     Formato: {"q1_1": 0, "q1_2": 1, "q1_3": 2, "q1_4": 1, "q2_1": 3, ...}
                     Donde el key es "q{scenario}_{question}" y el valor es el índice de la opción elegida.
        responses_b: Respuestas del participante B (mismo formato)
        
    Returns:
        Dict con estructura:
        {
            "empatia": 85.5,                    # Dimensión 1: Precisión de percepción mutua
            "consenso_equidad": 72.0,            # Dimensión 2: Consenso sobre lo justo
            "alineacion_deseos": 68.0,           # Dimensión 3: Similitud de deseos reales
            "balance_personal": 81.0,            # Dimensión 4: Balance personal vs relacional
            "score_global": 77.3,                # Promedio de las 4 dimensiones
            "detalles_por_escenario": [...]      # Breakdown por cada escenario
        }
        
    Las 4 dimensiones son:
    1. Empatía: Promedio de cuán bien cada persona adivinó lo que la otra realmente quiere
       (A adivina B en Q2 vs Q1_B real + B adivina A en Q2 vs Q1_A real)
    2. Consenso en equidad: Similitud entre lo que cada uno considera "mejor para la pareja"
       (Q3_A vs Q3_B)
    3. Alineación de deseos: Similitud entre lo que realmente quieren
       (Q1_A vs Q1_B)
    4. Balance personal vs relacional: Promedio de cuánto difiere el deseo propio de lo que
       considera "mejor para la pareja" (Q1_A vs Q3_A + Q1_B vs Q3_B)
    """
    # Importar scenarios dentro de la función para evitar imports circulares
    from p_dynamics.lib.scenarios import get_scenarios
    
    scenarios = get_scenarios()
    
    # Validar que tenemos respuestas
    if not responses_a or not responses_b:
        return {
            "empatia": 0.0,
            "consenso_equidad": 0.0,
            "alineacion_deseos": 0.0,
            "balance_personal": 0.0,
            "score_global": 0.0,
            "detalles_por_escenario": []
        }
    
    # Listas para acumular scores por escenario
    empatia_scores = []
    consenso_scores = []
    alineacion_scores = []
    balance_scores = []
    detalles_por_escenario = []
    
    # Procesar cada escenario
    for scenario in scenarios:
        scenario_id = scenario["id"]
        scenario_title = scenario["title"]
        
        # Obtener las 4 preguntas del escenario
        questions = scenario["questions"]
        if len(questions) != 4:
            continue  # Skip si no tiene las 4 preguntas esperadas
        
        q1 = questions[0]  # "¿Qué prefiero?" (deseo real)
        q2 = questions[1]  # "¿Qué creo que mi pareja prefiere?" (percepción del otro)
        q3 = questions[2]  # "¿Qué es lo más justo?" (visión de equidad)
        q4 = questions[3]  # "¿Qué creo que mi pareja considera mejor?" (meta-percepción)
        
        # Obtener los índices de respuesta para este escenario
        q_key_base = f"q{scenario_id}"
        
        # Obtener índices seleccionados
        idx_a_q1 = responses_a.get(f"{q_key_base}_1")  # Deseo real de A
        idx_a_q2 = responses_a.get(f"{q_key_base}_2")  # A adivina deseo de B
        idx_a_q3 = responses_a.get(f"{q_key_base}_3")  # A: lo más justo
        
        idx_b_q1 = responses_b.get(f"{q_key_base}_1")  # Deseo real de B
        idx_b_q2 = responses_b.get(f"{q_key_base}_2")  # B adivina deseo de A
        idx_b_q3 = responses_b.get(f"{q_key_base}_3")  # B: lo más justo
        
        # Verificar que todas las respuestas necesarias existan
        if any(idx is None for idx in [idx_a_q1, idx_a_q2, idx_a_q3, idx_b_q1, idx_b_q2, idx_b_q3]):
            continue
        
        # Obtener los tags de cada respuesta
        try:
            tags_a_q1 = q1["options"][idx_a_q1]["tags"]  # Deseo real de A
            tags_a_q2 = q2["options"][idx_a_q2]["tags"]  # A adivina B
            tags_a_q3 = q3["options"][idx_a_q3]["tags"]  # A: equidad
            
            tags_b_q1 = q1["options"][idx_b_q1]["tags"]  # Deseo real de B
            tags_b_q2 = q2["options"][idx_b_q2]["tags"]  # B adivina A
            tags_b_q3 = q3["options"][idx_b_q3]["tags"]  # B: equidad
        except (IndexError, KeyError, TypeError):
            continue  # Skip si los tags no existen
        
        # --- DIMENSIÓN 1: EMPATÍA / PRECISIÓN DE PERCEPCIÓN ---
        # ¿Qué tan bien A adivinó lo que B realmente quiere?
        empatia_a = calculate_similarity(tags_a_q2, tags_b_q1)
        # ¿Qué tan bien B adivinó lo que A realmente quiere?
        empatia_b = calculate_similarity(tags_b_q2, tags_a_q1)
        # Promedio de ambas direcciones
        empatia_escenario = (empatia_a + empatia_b) / 2
        empatia_scores.append(empatia_escenario)
        
        # --- DIMENSIÓN 2: CONSENSO EN EQUIDAD ---
        # ¿Qué tan similar es la visión de lo "justo" entre A y B?
        consenso_escenario = calculate_similarity(tags_a_q3, tags_b_q3)
        consenso_scores.append(consenso_escenario)
        
        # --- DIMENSIÓN 3: ALINEACIÓN DE DESEOS REALES ---
        # ¿Qué tan similares son los deseos reales de A y B?
        alineacion_escenario = calculate_similarity(tags_a_q1, tags_b_q1)
        alineacion_scores.append(alineacion_escenario)
        
        # --- DIMENSIÓN 4: BALANCE PERSONAL VS RELACIONAL ---
        # ¿Qué tan alineado está el deseo propio con lo que considera "mejor para la pareja"?
        # Para A: similitud entre su deseo (Q1) y su visión de equidad (Q3)
        balance_a = calculate_similarity(tags_a_q1, tags_a_q3)
        # Para B: similitud entre su deseo (Q1) y su visión de equidad (Q3)
        balance_b = calculate_similarity(tags_b_q1, tags_b_q3)
        # Promedio: alto score = ambos alinean bien su deseo con lo que ven justo
        balance_escenario = (balance_a + balance_b) / 2
        balance_scores.append(balance_escenario)
        
        # Guardar detalles del escenario
        detalles_por_escenario.append({
            "escenario_id": scenario_id,
            "escenario_titulo": scenario_title,
            "empatia": round(empatia_escenario, 1),
            "consenso_equidad": round(consenso_escenario, 1),
            "alineacion_deseos": round(alineacion_escenario, 1),
            "balance_personal": round(balance_escenario, 1),
            "detalles": {
                "empatia_a_hacia_b": round(empatia_a, 1),
                "empatia_b_hacia_a": round(empatia_b, 1),
                "balance_a": round(balance_a, 1),
                "balance_b": round(balance_b, 1)
            }
        })
    
    # Calcular promedios finales
    empatia_final = sum(empatia_scores) / len(empatia_scores) if empatia_scores else 0.0
    consenso_final = sum(consenso_scores) / len(consenso_scores) if consenso_scores else 0.0
    alineacion_final = sum(alineacion_scores) / len(alineacion_scores) if alineacion_scores else 0.0
    balance_final = sum(balance_scores) / len(balance_scores) if balance_scores else 0.0
    
    # Score global: promedio de las 4 dimensiones
    score_global = (empatia_final + consenso_final + alineacion_final + balance_final) / 4
    
    return {
        "empatia": round(empatia_final, 1),
        "consenso_equidad": round(consenso_final, 1),
        "alineacion_deseos": round(alineacion_final, 1),
        "balance_personal": round(balance_final, 1),
        "score_global": round(score_global, 1),
        "detalles_por_escenario": detalles_por_escenario
    }


# ============================================================================
# REFLEX STATE CLASS (para integración con la UI)
# ============================================================================

class ScoringState(rx.State):
    """State for calculating and managing test scores."""
    
    alignment_score: float = 0.0
    empathy_score: float = 0.0
    relationship_health_score: float = 0.0
    scores_calculated: bool = False
    
    def calculate_alignment_score(self, answers_a: Dict[str, int], answers_b: Dict[str, int]) -> float:
        """
        Calculate alignment score between personal desires (Q1 responses).
        Measures how similar partners' personal preferences are.
        """
        q1_answers_a = {k: v for k, v in answers_a.items() if k.endswith("_1")}
        q1_answers_b = {k: v for k, v in answers_b.items() if k.endswith("_1")}
        
        if not q1_answers_a or not q1_answers_b:
            return 0.0
        
        matching_count = sum(
            1 for k in q1_answers_a.keys() 
            if k in q1_answers_b and q1_answers_a[k] == q1_answers_b[k]
        )
        
        total_questions = len(q1_answers_a)
        return (matching_count / total_questions * 100) if total_questions > 0 else 0.0
    
    def calculate_empathy_score(self, answers_a: Dict[str, int], answers_b: Dict[str, int]) -> float:
        """
        Calculate empathy score (Q2 accuracy).
        Measures how well each partner understands the other's preferences.
        """
        # Partner A's guess about B vs B's actual answer
        q1_answers_a = {k: v for k, v in answers_a.items() if k.endswith("_1")}
        q2_answers_a = {k: v for k, v in answers_a.items() if k.endswith("_2")}
        
        q1_answers_b = {k: v for k, v in answers_b.items() if k.endswith("_1")}
        q2_answers_b = {k: v for k, v in answers_b.items() if k.endswith("_2")}
        
        if not q1_answers_a or not q2_answers_a:
            return 0.0
        
        # A's empathy: how well A guesses B's preferences
        a_correct = sum(
            1 for k in q2_answers_a.keys()
            if k.replace("_2", "_1") in q1_answers_b 
            and q2_answers_a[k] == q1_answers_b[k.replace("_2", "_1")]
        )
        
        # B's empathy: how well B guesses A's preferences
        b_correct = sum(
            1 for k in q2_answers_b.keys()
            if k.replace("_2", "_1") in q1_answers_a 
            and q2_answers_b[k] == q1_answers_a[k.replace("_2", "_1")]
        )
        
        total_questions = len(q2_answers_a)
        total_correct = a_correct + b_correct
        max_possible = total_questions * 2
        
        return (total_correct / max_possible * 100) if max_possible > 0 else 0.0
    
    def calculate_relationship_health_score(
        self, answers_a: Dict[str, int], answers_b: Dict[str, int]
    ) -> float:
        """
        Calculate relationship health score.
        Measures alignment on fairness (Q3) and mutual best interest (Q4).
        """
        q3_answers_a = {k: v for k, v in answers_a.items() if k.endswith("_3")}
        q3_answers_b = {k: v for k, v in answers_b.items() if k.endswith("_3")}
        
        q4_answers_a = {k: v for k, v in answers_a.items() if k.endswith("_4")}
        q4_answers_b = {k: v for k, v in answers_b.items() if k.endswith("_4")}
        
        if not q3_answers_a or not q4_answers_a:
            return 0.0
        
        # Q3 alignment: both agree on what's fair
        q3_matching = sum(
            1 for k in q3_answers_a.keys()
            if k in q3_answers_b and q3_answers_a[k] == q3_answers_b[k]
        )
        
        # Q4 alignment: both agree on what's best for relationship
        q4_matching = sum(
            1 for k in q4_answers_a.keys()
            if k in q4_answers_b and q4_answers_a[k] == q4_answers_b[k]
        )
        
        total_questions = len(q3_answers_a)
        total_matching = q3_matching + q4_matching
        max_possible = total_questions * 2
        
        return (total_matching / max_possible * 100) if max_possible > 0 else 0.0
    
    def calculate_all_scores(self, answers_a: Dict[str, int], answers_b: Dict[str, int]):
        """Calculate all scores for a couple."""
        self.alignment_score = self.calculate_alignment_score(answers_a, answers_b)
        self.empathy_score = self.calculate_empathy_score(answers_a, answers_b)
        self.relationship_health_score = self.calculate_relationship_health_score(
            answers_a, answers_b
        )
        self.scores_calculated = True
    
    def get_scores(self) -> Tuple[float, float, float]:
        """Return all scores as a tuple."""
        return (
            self.alignment_score,
            self.empathy_score,
            self.relationship_health_score
        )
    
    def reset_scores(self):
        """Reset all scores."""
        self.alignment_score = 0.0
        self.empathy_score = 0.0
        self.relationship_health_score = 0.0
        self.scores_calculated = False

