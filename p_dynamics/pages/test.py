"""Test page for taking the assessment."""
import reflex as rx
from ..state.test_state import TestState
from ..components.scenario_card import scenario_card


def test() -> rx.Component:
    """Test page with questions."""
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "Test de Pareja",
                    size="7"
                ),
                rx.text(
                    f"Progreso: {TestState.get_progress}%",
                    size="3",
                    color="gray"
                ),
                justify="between",
                width="100%",
                margin_bottom="2rem"
            ),
            # Progress bar
            rx.progress(
                value=TestState.get_progress,
                width="100%",
                margin_bottom="2rem"
            ),
            # Current scenario card
            rx.cond(
                TestState.current_scenario,
                scenario_card(TestState.current_scenario)
            ),
            # Current question
            rx.cond(
                TestState.current_question,
                rx.vstack(
                    rx.heading(
                        TestState.current_question["text"],
                        size="5",
                        margin_bottom="1rem"
                    ),
                    rx.vstack(
                        rx.foreach(
                            TestState.question_options,
                            lambda option, index: rx.button(
                                option,
                                on_click=TestState.answer_question(TestState.current_question["id"], index),
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
            ),
            # Navigation buttons
            rx.hstack(
                rx.button(
                    "Anterior",
                    on_click=TestState.previous_question,
                    variant="outline",
                    size="3",
                    disabled=TestState.current_scenario_index == 0 and TestState.current_question_index == 0
                ),
                rx.button(
                    "Siguiente",
                    on_click=TestState.next_question,
                    size="3"
                ),
                spacing="2",
                justify="end",
                width="100%",
                margin_top="2rem"
            ),
            spacing="4",
            width="100%",
            padding_y="2rem"
        ),
        max_width="800px",
        padding="2rem"
    )
