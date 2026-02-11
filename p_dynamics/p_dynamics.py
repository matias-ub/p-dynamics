"""Main application file for 4 Perspectivas para Parejas."""
import reflex as rx
from .pages import index, login, test, results, invite

# Create the application
app = rx.App()

# Add pages
app.add_page(index, route="/")
app.add_page(login, route="/login")
app.add_page(test, route="/test")
app.add_page(results, route="/results")
app.add_page(invite, route="/invite")
