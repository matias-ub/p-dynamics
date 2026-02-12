"""Question component for test display."""
import reflex as rx
from ..state.test_state import TestState


def question_component(question) -> rx.Component:
    """Display a question with multiple choice options."""
    return rx.vstack(
        rx.heading(
            question["text"],
            size="5",
            margin_bottom="1rem"
        ),
        rx.vstack(
            rx.foreach(
                question["options"],
                lambda option, index: rx.button(
                    option,
                    on_click=TestState.answer_question(question["id"], index),
                    width="100%",
                    variant="outline",
                    size="3",
                    margin_bottom="0.5rem"
                )
            ),
            spacing="2",
            width="100%"
        ),
        spacing="4",
        align="start",
        width="100%",
        padding="1rem"
    )
