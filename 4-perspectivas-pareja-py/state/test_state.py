"""Test state management for quiz flow."""
import reflex as rx
from typing import Dict, List
from lib.scenarios import get_scenarios, get_scenario_by_id


class TestState(rx.State):
    """State management for test flow."""
    
    current_scenario_index: int = 0
    current_question_index: int = 0
    answers: Dict[str, int] = {}
    test_completed: bool = False
    
    def get_current_scenario(self):
        """Get the current scenario."""
        scenarios = get_scenarios()
        if self.current_scenario_index < len(scenarios):
            return scenarios[self.current_scenario_index]
        return None
    
    def get_current_question(self):
        """Get the current question."""
        scenario = self.get_current_scenario()
        if scenario and self.current_question_index < len(scenario["questions"]):
            return scenario["questions"][self.current_question_index]
        return None
    
    def answer_question(self, question_id: str, answer_index: int):
        """Record an answer for a question."""
        self.answers[question_id] = answer_index
    
    def next_question(self):
        """Move to the next question."""
        scenario = self.get_current_scenario()
        if not scenario:
            return
        
        if self.current_question_index < len(scenario["questions"]) - 1:
            self.current_question_index += 1
        else:
            # Move to next scenario
            scenarios = get_scenarios()
            if self.current_scenario_index < len(scenarios) - 1:
                self.current_scenario_index += 1
                self.current_question_index = 0
            else:
                self.test_completed = True
                return rx.redirect("/results")
    
    def previous_question(self):
        """Move to the previous question."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
        else:
            # Move to previous scenario
            if self.current_scenario_index > 0:
                self.current_scenario_index -= 1
                scenario = self.get_current_scenario()
                if scenario:
                    self.current_question_index = len(scenario["questions"]) - 1
    
    def get_progress(self) -> float:
        """Calculate test progress percentage."""
        scenarios = get_scenarios()
        total_questions = sum(len(s["questions"]) for s in scenarios)
        answered_questions = len(self.answers)
        return (answered_questions / total_questions * 100) if total_questions > 0 else 0
    
    def reset_test(self):
        """Reset test to initial state."""
        self.current_scenario_index = 0
        self.current_question_index = 0
        self.answers = {}
        self.test_completed = False
