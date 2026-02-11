"""Authentication state management."""
import reflex as rx
from lib.supabase_client import get_supabase_client


class AuthState(rx.State):
    """Authentication state for user management."""
    
    user_id: str = ""
    user_email: str = ""
    is_authenticated: bool = False
    couple_id: str = ""
    partner_id: str = ""
    error_message: str = ""
    
    def login(self, email: str, password: str):
        """Login user with email and password."""
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                self.user_id = response.user.id
                self.user_email = response.user.email
                self.is_authenticated = True
                self.error_message = ""
                return rx.redirect("/test")
            else:
                self.error_message = "Login failed. Please check your credentials."
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
    
    def signup(self, email: str, password: str):
        """Sign up new user."""
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                self.user_id = response.user.id
                self.user_email = response.user.email
                self.is_authenticated = True
                self.error_message = ""
                return rx.redirect("/test")
            else:
                self.error_message = "Sign up failed. Please try again."
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
    
    def logout(self):
        """Logout current user."""
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            self.user_id = ""
            self.user_email = ""
            self.is_authenticated = False
            self.couple_id = ""
            self.partner_id = ""
            self.error_message = ""
            return rx.redirect("/login")
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
    
    def set_couple_id(self, couple_id: str):
        """Set the couple ID for the current user."""
        self.couple_id = couple_id
    
    def set_partner_id(self, partner_id: str):
        """Set the partner ID."""
        self.partner_id = partner_id
