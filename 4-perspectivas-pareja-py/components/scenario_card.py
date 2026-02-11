"""Scenario card component."""
import reflex as rx


def scenario_card(scenario: dict) -> rx.Component:
    """Display a scenario card with title and description."""
    return rx.card(
        rx.vstack(
            rx.heading(
                scenario.get("title", ""),
                size="6",
                margin_bottom="0.5rem"
            ),
            rx.text(
                scenario.get("description", ""),
                color="gray",
                size="3"
            ),
            spacing="2",
            align="start",
            width="100%"
        ),
        width="100%",
        padding="1.5rem",
        margin_bottom="1rem"
    )
