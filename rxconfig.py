import reflex as rx

config = rx.Config(
    app_name="p_dynamics",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)