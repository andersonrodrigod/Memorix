import customtkinter as ctk
from views.search_view import SearchView
from views.add_view import AddView


class RecallApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Recall — Memória Técnica")
        self.root.geometry("1000x700")

        self.add_view = None

        self._create_menu()
        self._open_search_view()

    def _create_menu(self):
        menu_bar = ctk.CTkFrame(self.root, height=40)
        menu_bar.pack(fill="x")

        btn_search = ctk.CTkButton(
            menu_bar,
            text="Pesquisar",
            command=self._open_search_view,
            width=120
        )
        btn_search.pack(side="left", padx=10, pady=5)

        btn_add = ctk.CTkButton(
            menu_bar,
            text="Adicionar",
            command=self._open_add_view,
            width=120
        )
        btn_add.pack(side="left", padx=5, pady=5)

    def _clear_view(self):
        if hasattr(self, "current_view"):
            self.current_view.destroy()

    def _open_search_view(self):
        self._clear_view()
        self.current_view = SearchView(self.root)
        self.current_view.pack(fill="both", expand=True)

    def _open_add_view(self):
        self.root.iconify()

        if self.add_view is None or not self.add_view.winfo_exists():
            self.add_view = AddView(self.root)
        else:
            self.add_view.deiconify()
            self.add_view.focus_force()

    def run(self):
        self.root.mainloop()
