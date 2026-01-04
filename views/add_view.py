import customtkinter as ctk
from models.memory_model import add_entry, parse_tags
from tkinter import messagebox




class AddView(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Adicionar Conhecimento")
        self.geometry("1200x850")
        self.minsize(1100, 750)

        self._build_ui()

        # 🔥 CONTROLE DE FOCO (AJUSTADO)
        self.transient(master)
        self.focus_force()


        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _on_close(self):
        self.withdraw()  # esconde a janela, NÃO destrói
        self.master.deiconify()


    def _build_ui(self):
        # ===== CONTAINER GERAL =====
        container = ctk.CTkScrollableFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= METADADOS =================
        meta_frame = ctk.CTkFrame(container)
        meta_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(meta_frame, text="Metadados", font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=10)

        grid = ctk.CTkFrame(meta_frame)
        grid.pack(fill="x", padx=20, pady=(0, 15))
        grid.grid_columnconfigure((0, 1), weight=1)

        # Categoria
        ctk.CTkLabel(grid, text="Categoria *").grid(row=0, column=0, sticky="w")
        self.category_entry = ctk.CTkEntry(grid)
        self.category_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 10))

        # Área
        ctk.CTkLabel(grid, text="Área / Domínio").grid(row=0, column=1, sticky="w")
        self.domain_entry = ctk.CTkEntry(grid)
        self.domain_entry.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        # Contexto
        ctk.CTkLabel(grid, text="Projeto / Contexto").grid(row=2, column=0, sticky="w")
        self.context_entry = ctk.CTkEntry(grid)
        self.context_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 10))

        # Referência
        ctk.CTkLabel(grid, text="Referência / Fonte").grid(row=2, column=1, sticky="w")
        self.reference_entry = ctk.CTkEntry(grid)
        self.reference_entry.grid(row=3, column=1, sticky="ew", pady=(0, 10))

        # ===== DIFICULDADE =====
        diff_frame = ctk.CTkFrame(meta_frame)
        diff_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(diff_frame, text="Nível de Dificuldade").pack(anchor="w", pady=(10, 5))

        self.difficulty = ctk.StringVar(value="Intermediário")

        radio_container = ctk.CTkFrame(diff_frame)
        radio_container.pack(anchor="w", pady=(0, 10))

        for level in ["Básico", "Intermediário", "Avançado"]:
            ctk.CTkRadioButton(
                radio_container,
                text=level,
                variable=self.difficulty,
                value=level
            ).pack(side="left", padx=10)

        # ================= CONTEÚDO =================
        content_frame = ctk.CTkFrame(container)
        content_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(content_frame, text="Conteúdo", font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=10)

        ctk.CTkLabel(content_frame, text="Título").pack(anchor="w", padx=20)
        self.title_entry = ctk.CTkEntry(content_frame)
        self.title_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(content_frame, text="Tags (separadas por vírgula)").pack(anchor="w", padx=20)
        self.tags_entry = ctk.CTkEntry(content_frame)
        self.tags_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(content_frame, text="Descrição").pack(anchor="w", padx=20)
        self.description_box = ctk.CTkTextbox(content_frame, height=90)
        self.description_box.pack(fill="x", padx=20, pady=(0, 15))

        # ================= EXEMPLOS =================
        examples_frame = ctk.CTkFrame(container)
        examples_frame.pack(fill="both", expand=True, pady=(0, 20))

        ctk.CTkLabel(examples_frame, text="Exemplos", font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=10)

        examples_grid = ctk.CTkFrame(examples_frame)
        examples_grid.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        examples_grid.grid_columnconfigure((0, 1), weight=1)
        examples_grid.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(examples_grid, text="Exemplo A").grid(row=0, column=0, sticky="w")
        self.example_a = ctk.CTkTextbox(examples_grid, font=("Consolas", 12))
        self.example_a.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(examples_grid, text="Exemplo B").grid(row=0, column=1, sticky="w")
        self.example_b = ctk.CTkTextbox(examples_grid, font=("Consolas", 12))
        self.example_b.grid(row=1, column=1, sticky="nsew")

        # ================= OBSERVAÇÕES =================
        notes_frame = ctk.CTkFrame(container)
        notes_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(notes_frame, text="Explicação do meu jeito", font=("Arial", 16, "bold")).pack(anchor="w", padx=20, pady=10)
        self.notes_box = ctk.CTkTextbox(notes_frame, height=120)
        self.notes_box.pack(fill="x", padx=20, pady=(0, 10))

        # ================= BOTÃO =================
        buttons_frame = ctk.CTkFrame(container)
        buttons_frame.pack(pady=20)

        btn_clear = ctk.CTkButton(
            buttons_frame,
            text="Limpar campos",
            fg_color="#444444",
            hover_color="#555555",
            command=self._clear_fields
        )
        btn_clear.pack(side="left", padx=10)

        btn_save = ctk.CTkButton(
            buttons_frame,
            text="Salvar",
            height=40,
            command=self._save_entry
        )
        btn_save.pack(side="left", padx=10)


    def _save_entry(self):
        entry = {
            "categoria": self.category_entry.get().strip(),
            "area": self.domain_entry.get().strip(),
            "contexto": self.context_entry.get().strip(),
            "referencia": self.reference_entry.get().strip(),
            "nivel_dificuldade": self.difficulty.get(),
            "titulo": self.title_entry.get().strip(),
            "tags": parse_tags(self.tags_entry.get()),
            "descricao": self.description_box.get("1.0", "end").strip(),
            "exemplos": {
                "exemplo_a": self.example_a.get("1.0", "end").strip(),
                "exemplo_b": self.example_b.get("1.0", "end").strip(),
            },
            "explicacao_pessoal": self.notes_box.get("1.0", "end").strip(),
            "status": "estudo"
        }

        # Validação mínima
        if not entry["categoria"]:
            ctk.CTkMessagebox(title="Erro", message="Categoria é obrigatória.")
            return

        add_entry(entry)
        self.withdraw()

    def _clear_fields(self):
        resposta = messagebox.askyesno(
            "Confirmar limpeza",
            "Tem certeza que deseja limpar todos os campos?\n\n"
            "Essa ação NÃO pode ser desfeita."
        )

        if not resposta:
            return

        self.category_entry.delete(0, "end")
        self.domain_entry.delete(0, "end")
        self.context_entry.delete(0, "end")
        self.reference_entry.delete(0, "end")

        self.title_entry.delete(0, "end")
        self.tags_entry.delete(0, "end")

        self.description_box.delete("1.0", "end")
        self.example_a.delete("1.0", "end")
        self.example_b.delete("1.0", "end")
        self.notes_box.delete("1.0", "end")

        self.difficulty.set("Intermediário")


