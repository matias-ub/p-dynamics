"""Results page displaying test scores."""
import reflex as rx
from ..state.scoring import ScoringState
from ..components.radar_chart import radar_chart


def results() -> rx.Component:
    """Results page with scores visualization."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "Resultados del Test",
                size="8",
                margin_bottom="2rem",
                text_align="center"
            ),
            # Radar chart
            rx.cond(
                ScoringState.scores_calculated,
                rx.vstack(
                    radar_chart(
                        ScoringState.alignment_score,
                        ScoringState.empathy_score,
                        ScoringState.relationship_health_score
                    ),
                    # Score details
                    rx.card(
                        rx.vstack(
                            rx.heading("Detalles de los Scores", size="6", margin_bottom="1rem"),
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Alineación", font_weight="bold"),
                                    rx.text(
                                        f"{ScoringState.alignment_score:.1f}%",
                                        size="6",
                                        color="blue"
                                    ),
                                    rx.text(
                                        "Similitud en preferencias personales",
                                        size="2",
                                        color="gray"
                                    ),
                                    align="center",
                                    spacing="1"
                                ),
                                rx.vstack(
                                    rx.text("Empatía", font_weight="bold"),
                                    rx.text(
                                        f"{ScoringState.empathy_score:.1f}%",
                                        size="6",
                                        color="green"
                                    ),
                                    rx.text(
                                        "Precisión al entender al otro",
                                        size="2",
                                        color="gray"
                                    ),
                                    align="center",
                                    spacing="1"
                                ),
                                rx.vstack(
                                    rx.text("Salud Relacional", font_weight="bold"),
                                    rx.text(
                                        f"{ScoringState.relationship_health_score:.1f}%",
                                        size="6",
                                        color="purple"
                                    ),
                                    rx.text(
                                        "Acuerdo en justicia y bienestar",
                                        size="2",
                                        color="gray"
                                    ),
                                    align="center",
                                    spacing="1"
                                ),
                                spacing="6",
                                justify="around",
                                width="100%"
                            ),
                            spacing="4",
                            align="start"
                        ),
                        width="100%",
                        max_width="700px",
                        padding="2rem",
                        margin_top="2rem"
                    ),
                    spacing="4",
                    width="100%"
                ),
                rx.text(
                    "Esperando a que ambos completen el test...",
                    size="4",
                    color="gray",
                    text_align="center"
                )
            ),
            # Action buttons
            rx.hstack(
                rx.button(
                    "Volver al inicio",
                    on_click=rx.redirect("/"),
                    variant="outline",
                    size="3"
                ),
                rx.button(
                    "Reintentar test",
                    on_click=rx.redirect("/test"),
                    size="3"
                ),
                spacing="2",
                justify="center",
                margin_top="2rem"
            ),
            spacing="4",
            align="center",
            padding_y="4rem",
            min_height="100vh"
        ),
        max_width="900px",
        padding="2rem"
    )
