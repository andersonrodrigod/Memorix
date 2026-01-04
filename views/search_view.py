import customtkinter as ctk
import json
import os


class SearchView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.all_entries = []
        self.filtered_entries = []

        self._build_ui()
        self._load_entries()
        self._apply_filters()

    # ================= UI =================

    def _build_ui(self):
        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(1, weight=1)

        # -------- FILTROS --------
        filters_frame = ctk.CTkFrame(self)
        filters_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        filters_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.category_filter = ctk.CTkEntry(
            filters_frame, placeholder_text="Categoria"
        )
        self.category_filter.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.category_filter.bind("<KeyRelease>", lambda e: self._apply_filters())

        self.area_filter = ctk.CTkEntry(
            filters_frame, placeholder_text="Área / Domínio"
        )
        self.area_filter.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.area_filter.bind("<KeyRelease>", lambda e: self._apply_filters())

        self.tags_filter = ctk.CTkEntry(
            filters_frame, placeholder_text="Tags (separadas por vírgula)"
        )
        self.tags_filter.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.tags_filter.bind("<KeyRelease>", lambda e: self._apply_filters())

        # -------- TÍTULOS --------
        titles_frame = ctk.CTkScrollableFrame(self)
        titles_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)

        ctk.CTkLabel(
            titles_frame, text="Títulos", font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.titles_container = ctk.CTkFrame(titles_frame)
        self.titles_container.pack(fill="both", expand=True, padx=10)

        # -------- LOUSA --------
        self.lousa_frame = ctk.CTkScrollableFrame(self)
        self.lousa_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)

        self.lousa_title = ctk.CTkLabel(
            self.lousa_frame, text="🧠 Lousa", font=("Arial", 18, "bold")
        )
        self.lousa_title.pack(anchor="w", padx=10, pady=(10, 5))

        self.lousa_meta = ctk.CTkLabel(
            self.lousa_frame, text="", text_color="#aaaaaa"
        )
        self.lousa_meta.pack(anchor="w", padx=10, pady=(0, 10))

        self.lousa_tags = ctk.CTkLabel(
            self.lousa_frame,
            text="",
            text_color="#888888",
            wraplength=700
        )
        self.lousa_tags.pack(anchor="w", padx=10, pady=(0, 15))

        self.lousa_description = self._section("Descrição")
        self.lousa_example_a = self._section("Exemplo A", code=True,)
        self.lousa_example_b = self._section("Exemplo B", code=True)
        self.lousa_notes = self._section("Explicação do meu jeito")

    def _section(self, title, code=False):
        ctk.CTkLabel(
            self.lousa_frame,
            text=title,
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10)

        box = ctk.CTkTextbox(
            self.lousa_frame,
            height=100 if not code else 300,
            font=("Consolas", 12) if code else None
        )

        if code:
            # Exemplos → crescem
            box.pack(fill="both", expand=True, padx=10, pady=(5, 15))
        else:
            # Texto normal → tamanho controlado
            box.pack(fill="x", padx=10, pady=(5, 15))

        return box

    # ================= DADOS =================

    def _load_entries(self):
        path = os.path.join("data", "memoria.json")

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            self.all_entries = [self._normalize(e) for e in raw]

        except Exception:
            self.all_entries = self._mock_entries()

    def _normalize(self, e):
        return {
            "titulo": e.get("titulo", ""),
            "categoria": e.get("categoria", "").lower(),
            "area": e.get("area", "").lower(),
            "tags": [t.lower() for t in e.get("tags", [])],
            "dificuldade": e.get("nivel_dificuldade", ""),
            "descricao": e.get("descricao", ""),
            "exemplo_a": e.get("exemplos", {}).get("exemplo_a", ""),
            "exemplo_b": e.get("exemplos", {}).get("exemplo_b", ""),
            "explicacao": e.get("explicacao_pessoal", "")
        }

    def _mock_entries(self):
        return [
            {
                "titulo": "set_index (pandas)",
                "categoria": "python",
                "area": "pandas",
                "tags": ["set index", "indice"],
                "dificuldade": "Intermediário",
                "descricao": "Define uma coluna como índice.",
                "exemplo_a": "df.set_index('coluna')",
                "exemplo_b": "df.set_index('coluna', inplace=True)",
                "explicacao": "Uso quando quero acessar pelo índice."
            },
            {
                "titulo": "groupby",
                "categoria": "python",
                "area": "pandas",
                "tags": ["groupby", "agregacao"],
                "dificuldade": "Intermediário",
                "descricao": "Agrupa dados para agregação.",
                "exemplo_a": "df.groupby('coluna').sum()",
                "exemplo_b": "df.groupby(['a','b']).mean()",
                "explicacao": "Base da análise de dados."
            }
        ]

    # ================= FILTROS =================

    def _apply_filters(self):
        cat = self.category_filter.get().strip().lower()
        area = self.area_filter.get().strip().lower()
        tags = [
            t.strip().lower()
            for t in self.tags_filter.get().split(",")
            if t.strip()
        ]

        def match(e):
            if cat and cat not in e["categoria"]:
                return False
            if area and area not in e["area"]:
                return False
            if tags and not all(t in e["tags"] for t in tags):
                return False
            return True

        self.filtered_entries = [e for e in self.all_entries if match(e)]
        self._render_titles()

    # ================= RENDER =================

    def _render_titles(self):
        for w in self.titles_container.winfo_children():
            w.destroy()

        for entry in self.filtered_entries:
            btn = ctk.CTkButton(
                self.titles_container,
                text=entry["titulo"],
                anchor="w",
                fg_color="#2b2b2b",
                hover_color="#3a3a3a",
                command=lambda e=entry: self._render_lousa(e)
            )
            btn.pack(fill="x", pady=4)

    def _render_lousa(self, e):
        self.lousa_title.configure(text=e["titulo"])
        self.lousa_meta.configure(
            text=f"{e['categoria']} • {e['area']} • {e['dificuldade']}"
        )

        tags_text = ", ".join(e["tags"]) if e["tags"] else "—"
        self.lousa_tags.configure(
            text=f"tags: {tags_text}"
        )

        self._fill(self.lousa_description, e["descricao"])
        self._fill(self.lousa_example_a, e["exemplo_a"])
        self._fill(self.lousa_example_b, e["exemplo_b"])
        self._fill(self.lousa_notes, e["explicacao"])

    def _fill(self, box, text):
        box.delete("1.0", "end")
        box.insert("1.0", text)
