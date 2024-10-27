import flet as ft
from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class ThemeColors:
    """Color scheme for the application"""
    primary: str = ft.colors.BLUE
    background: str = "#1a1a1a"
    card_background: str = "#2d2d2d"
    text: str = ft.colors.WHITE
    text_secondary: str = ft.colors.BLUE_GREY_200
    error: str = ft.colors.RED_400

class CustomTextField(ft.TextField):
    """Custom styled text field for the form"""
    def __init__(self, label: str, password: bool = False, visible: bool = True):
        super().__init__(
            label=label,
            password=password,
            can_reveal_password=password,
            border_color=ThemeColors.primary,
            color=ThemeColors.text,
            bgcolor=ThemeColors.card_background,
            width=300,
            text_size=14,
            visible=visible,
            border_radius=8,
            focused_border_color=ThemeColors.primary,
            label_style=ft.TextStyle(color=ThemeColors.text_secondary)
        )

class AuthForm(ft.UserControl):
    """Main authentication form component"""
    def __init__(self):
        super().__init__()
        self.is_login = True
        self.colors = ThemeColors()
        self.initialize_fields()
        
    def initialize_fields(self):
        """Initialize all form fields"""
        self.name_field = CustomTextField("Username")
        self.email_field = CustomTextField("Email", visible=False)
        self.pass_field = CustomTextField("Password", password=True)
        self.confirm_pass_field = CustomTextField("Confirm Password", password=True, visible=False)
        
        self.submit_button = ft.ElevatedButton(
            text="Login",
            style=ft.ButtonStyle(
                color=self.colors.text,
                bgcolor=self.colors.primary,
                padding=20,
            ),
            width=300,
            on_click=self.validate_and_submit
        )
        
        self.toggle_text = ft.Text(
            "New here? Sign Up!",
            color=self.colors.primary,
            size=14,
            weight=ft.FontWeight.W_500,
            selectable=True
        )
        
        self.form_container = ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text(
                        "Welcome!", 
                        size=32, 
                        weight=ft.FontWeight.BOLD, 
                        color=self.colors.primary
                    ),
                    self.name_field,
                    self.email_field,
                    self.pass_field,
                    self.confirm_pass_field,
                    self.submit_button,
                    ft.Container(
                        content=self.toggle_text,
                        on_click=self.toggle_mode,
                        padding=10,
                        border_radius=8,
                        ink=True,
                    )
                ]
            ),
            padding=40,
            bgcolor=self.colors.card_background,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLACK38,
            )
        )

    def validate_and_submit(self, e):
        """Validate form fields and handle submission"""
        if not self.name_field.value:
            self.show_error("Please enter username")
            return
        if not self.pass_field.value:
            self.show_error("Please enter password")
            return
            
        if not self.is_login:
            if not self.email_field.value:
                self.show_error("Please enter email")
                return
            if self.pass_field.value != self.confirm_pass_field.value:
                self.show_error("Passwords don't match!")
                return
                
        action = "Login" if self.is_login else "Signup"
        self.show_success(f"{action} successful!")
        
    def show_error(self, message: str):
        """Show error message in snackbar"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, color=self.colors.error),
                bgcolor=self.colors.card_background
            )
        )
        
    def show_success(self, message: str):
        """Show success message in snackbar"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message, color=self.colors.text),
                bgcolor=self.colors.primary
            )
        )

    def toggle_mode(self, e):
        """Toggle between login and signup modes"""
        self.is_login = not self.is_login
        
        # Update visibility of fields
        self.confirm_pass_field.visible = not self.is_login
        self.email_field.visible = not self.is_login
        
        # Update button and text
        self.submit_button.text = "Login" if self.is_login else "Sign Up"
        self.toggle_text.value = "New here? Sign Up!" if self.is_login else "Already have an account? Login!"
        
        self.update()

    def build(self):
        return self.form_container

class AuthApp:
    """Main application class"""
    def __init__(self):
        self.colors = ThemeColors()
        
    def main(self, page: ft.Page):
        # Configure page
        page.title = "Mukund"
        page.window_width = 390
        page.window_height = 884
        page.window_resizable = False
        page.bgcolor = self.colors.background
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        
        # Add auth form
        auth_form = AuthForm()
        page.add(auth_form)

if __name__ == "__main__":
    app = AuthApp()
    ft.app(target=app.main)