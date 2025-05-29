import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from zacspy.pdf.convert_to_300_DPI import convert_pdf_to_dpi

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Janela arredondada e barra personalizada
        self.geometry("650x350")
        self.resizable(True, True)
        self.overrideredirect(True)  # Remove barra padrão do sistema

        self._make_custom_title_bar()

        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(padx=30, pady=(10, 30), fill="both", expand=True)

        self.entry_input = ctk.CTkEntry(frame, placeholder_text="Caminho do PDF")
        self.entry_input.pack(pady=10, fill="x")

        btn_input = ctk.CTkButton(frame, text="Selecionar PDF", command=self.selecionar_arquivo, corner_radius=4)
        btn_input.pack(pady=5)

        self.entry_output = ctk.CTkEntry(frame, placeholder_text="Salvar como (opcional)")
        self.entry_output.pack(pady=10, fill="x")

        btn_output = ctk.CTkButton(frame, text="Selecionar saída", command=self.selecionar_saida, corner_radius=4)
        btn_output.pack(pady=5)

        self.entry_dpi = ctk.CTkEntry(frame, placeholder_text="DPI (padrão 300)")
        self.entry_dpi.insert(0, "300")
        self.entry_dpi.pack(pady=10)

        btn_convert = ctk.CTkButton(frame, text="Converter PDF", command=self.converter, corner_radius=4, fg_color="#e53935")
        btn_convert.pack(pady=15)

    def _make_custom_title_bar(self):
        """Cria uma barra de título customizada com botão de fechar."""
        title_bar = ctk.CTkFrame(self, height=30, fg_color="black", corner_radius=0)
        title_bar.pack(fill="x", side="top")
        title_bar.bind("<B1-Motion>", self._mover_janela)
        title_bar.bind("<Button-1>", self._pegar_posicao)

        label_title = ctk.CTkLabel(title_bar, text=" Conversor PDF para DPI Personalizado", text_color="white", fg_color="transparent")
        label_title.pack(side="left", padx=10)

        btn_fechar = ctk.CTkButton(title_bar, text="X", width=30, height=25, fg_color="red",
                                   hover_color="#990000", command=self.destroy, corner_radius=4)
        btn_fechar.pack(side="right", padx=5, pady=2)

    def _pegar_posicao(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def _mover_janela(self, event):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if caminho:
            self.entry_input.delete(0, "end")
            self.entry_input.insert(0, caminho)

    def selecionar_saida(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if caminho:
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, caminho)

    def converter(self):
        input_path = self.entry_input.get()
        output_path = self.entry_output.get()
        try:
            dpi = int(self.entry_dpi.get())
            if dpi <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Aviso", "Digite um valor de DPI válido.")
            return

        if not input_path:
            messagebox.showwarning("Aviso", "Selecione o arquivo de entrada.")
            return

        if not output_path:
            output_path = str(Path(input_path).with_name(Path(input_path).stem + f"_{dpi}DPI.pdf"))

        try:
            convert_pdf_to_dpi(input_path, output_path, dpi=dpi)
            messagebox.showinfo("Sucesso", f"PDF convertido para {dpi} DPI e salvo em:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
