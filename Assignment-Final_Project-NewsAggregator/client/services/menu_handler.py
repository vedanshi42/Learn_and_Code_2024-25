class MenuHandler:
    def __init__(self, auth_ui, user_ui, admin_ui):
        self.auth_ui = auth_ui
        self.user_ui = user_ui
        self.admin_ui = admin_ui

    def display_main_menu(self):
        user = self.auth_ui.login_or_signup()
        if user.role == 'admin':
            self.admin_ui.admin_menu(user)
        else:
            self.user_ui.user_menu(user)
