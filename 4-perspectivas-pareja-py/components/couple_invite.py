"""Couple invite component for inviting partner."""
import reflex as rx


def couple_invite(invite_link: str) -> rx.Component:
    """Display invite link for partner to join test."""
    return rx.card(
        rx.vstack(
            rx.heading(
                "Invita a tu pareja",
                size="5",
                margin_bottom="1rem"
            ),
            rx.text(
                "Comparte este enlace con tu pareja para que complete su parte del test:",
                margin_bottom="1rem"
            ),
            rx.hstack(
                rx.input(
                    value=invite_link,
                    is_read_only=True,
                    width="100%",
                    size="3"
                ),
                rx.button(
                    "Copiar",
                    on_click=rx.set_clipboard(invite_link),
                    size="3"
                ),
                spacing="2",
                width="100%"
            ),
            rx.text(
                "Una vez que ambos hayan completado el test, podrán ver los resultados.",
                size="2",
                color="gray",
                margin_top="1rem"
            ),
            spacing="3",
            align="start",
            width="100%"
        ),
        width="100%",
        max_width="600px",
        padding="2rem",
        margin="0 auto"
    )
