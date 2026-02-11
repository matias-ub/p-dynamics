"""Scoring calculations for test results."""
import reflex as rx
from typing import Dict, List, Tuple


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
