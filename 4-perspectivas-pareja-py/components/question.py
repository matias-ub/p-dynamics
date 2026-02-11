"""Question component for test display."""
import reflex as rx
from state.test_state import TestState


def create_option_button(option: str, question_id: str, option_index: int) -> rx.Component:
    """Create a single option button for a question."""
    return rx.button(
        option,
        on_click=TestState.answer_question(question_id, option_index),
        width="100%",
        variant="outline",
        size="3",
        margin_bottom="0.5rem"
    )


def question_component(question: dict) -> rx.Component:
    """Display a question with multiple choice options."""
    question_id = question.get("id", "")
    options = question.get("options", [])
    
    return rx.vstack(
        rx.heading(
            question.get("text", ""),
            size="5",
            margin_bottom="1rem"
        ),
        rx.vstack(
            *[
                create_option_button(option, question_id, i)
                for i, option in enumerate(options)
            ],
            spacing="2",
            width="100%"
        ),
        spacing="4",
        align="start",
        width="100%",
        padding="1rem"
    )
