"""Index/home page."""
import reflex as rx
from state.auth_state import AuthState


def index() -> rx.Component:
    """Home page with introduction to the test."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "4 Perspectivas para Parejas",
                size="9",
                margin_bottom="1rem",
                text_align="center"
            ),
            rx.text(
                "Test interactivo para parejas: compara deseos personales, percepción del otro, "
                "equidad objetiva y percepción mutua de lo 'mejor para la relación'.",
                size="4",
                text_align="center",
                margin_bottom="2rem",
                color="gray"
            ),
            rx.card(
                rx.vstack(
                    rx.heading("¿Cómo funciona?", size="6", margin_bottom="1rem"),
                    rx.unordered_list(
                        rx.list_item("Cada persona responde 4 preguntas por escenario"),
                        rx.list_item("Perspectiva 1: ¿Qué prefiero yo?"),
                        rx.list_item("Perspectiva 2: ¿Qué creo que prefiere mi pareja?"),
                        rx.list_item("Perspectiva 3: ¿Qué es lo más justo?"),
                        rx.list_item("Perspectiva 4: ¿Qué creo que mi pareja considera mejor para la relación?"),
                        spacing="2",
                        margin_left="1rem"
                    ),
                    rx.text(
                        "Después calculamos:",
                        font_weight="bold",
                        margin_top="1rem"
                    ),
                    rx.unordered_list(
                        rx.list_item("Score de Alineación: ¿Qué tan similares son sus preferencias?"),
                        rx.list_item("Score de Empatía: ¿Qué tan bien se conocen?"),
                        rx.list_item("Score de Salud Relacional: ¿Están de acuerdo en lo que es justo y mejor?"),
                        spacing="2",
                        margin_left="1rem"
                    ),
                    spacing="3",
                    align="start"
                ),
                width="100%",
                max_width="700px",
                padding="2rem",
                margin_bottom="2rem"
            ),
            rx.button(
                "Comenzar Test",
                on_click=rx.redirect("/login"),
                size="4",
                color_scheme="blue"
            ),
            spacing="4",
            align="center",
            padding_y="4rem",
            min_height="100vh"
        ),
        max_width="900px",
        padding="2rem"
    )
