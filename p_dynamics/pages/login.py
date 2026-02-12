"""Login and signup page."""
import reflex as rx
from ..state.auth_state import AuthState


def login() -> rx.Component:
    """Login/signup page."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "Iniciar Sesión",
                size="8",
                margin_bottom="2rem",
                text_align="center"
            ),
            rx.card(
                rx.vstack(
                    rx.cond(
                        AuthState.error_message != "",
                        rx.callout(
                            AuthState.error_message,
                            color_scheme="red",
                            size="2",
                            margin_bottom="1rem"
                        )
                    ),
                    rx.input(
                        placeholder="Email",
                        type="email",
                        size="3",
                        width="100%",
                        value=AuthState.email,
                        on_change=AuthState.set_email
                    ),
                    rx.input(
                        placeholder="Contraseña",
                        type="password",
                        size="3",
                        width="100%",
                        value=AuthState.password,
                        on_change=AuthState.set_password
                    ),
                    rx.hstack(
                        rx.button(
                            "Iniciar Sesión",
                            on_click=AuthState.login,
                            size="3",
                            width="100%"
                        ),
                        rx.button(
                            "Registrarse",
                            on_click=AuthState.signup,
                            size="3",
                            width="100%",
                            variant="outline"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    spacing="4",
                    width="100%"
                ),
                width="100%",
                max_width="400px",
                padding="2rem"
            ),
            rx.button(
                "Volver al inicio",
                on_click=rx.redirect("/"),
                variant="ghost",
                margin_top="1rem"
            ),
            spacing="4",
            align="center",
            padding_y="4rem",
            min_height="100vh"
        ),
        max_width="600px",
        padding="2rem"
    )
