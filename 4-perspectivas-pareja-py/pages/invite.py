"""Invite page for sharing with partner."""
import reflex as rx
from state.auth_state import AuthState
from components.couple_invite import couple_invite


def invite() -> rx.Component:
    """Invite page for partner."""
    invite_link = f"https://yourapp.com/join/{AuthState.couple_id}"
    
    return rx.container(
        rx.vstack(
            rx.heading(
                "Comparte el Test",
                size="8",
                margin_bottom="2rem",
                text_align="center"
            ),
            couple_invite(invite_link),
            rx.text(
                "¿Ya completaste tu parte?",
                size="3",
                margin_top="2rem",
                text_align="center"
            ),
            rx.button(
                "Ver mi progreso",
                on_click=rx.redirect("/test"),
                size="3"
            ),
            spacing="4",
            align="center",
            padding_y="4rem",
            min_height="100vh"
        ),
        max_width="800px",
        padding="2rem"
    )
