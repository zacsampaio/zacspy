import tkinter as tk
from tkinter import filedialog, messagebox, font
from pathlib import Path

from zacspy.pdf.convert_to_300_DPI import convert_pdf_to_300dpi

def centralizar_janela(janela, largura=600, altura=300):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = int((largura_tela - largura) / 2)
    y = int((altura_tela - altura) / 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def selecionar_arquivo():
    filepath = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if filepath:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, filepath)

def selecionar_saida():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Salvar arquivo como"
    )
    if filepath:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, filepath)

def converter():
    input_path = entry_input.get()
    output_path = entry_output.get()

    if not input_path:
        messagebox.showwarning("Aviso", "Selecione o arquivo de entrada.")
        return

    # Se saída estiver vazia ou for o placeholder, salva ao lado do arquivo original com sufixo
    if not output_path or output_path == "<opcional, salva no mesmo local do arquivo>":
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.with_name(input_path_obj.stem + "_300DPI.pdf"))

    try:
        convert_pdf_to_300dpi(input_path, output_path)
        messagebox.showinfo("Sucesso", f"Arquivo convertido e salvo em:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

def on_entry_output_focus_in(event):
    if entry_output.get() == "<opcional, salva no mesmo local do arquivo>":
        entry_output.delete(0, tk.END)
        entry_output.config(fg="black")

def on_entry_output_focus_out(event):
    if not entry_output.get():
        entry_output.insert(0, "<opcional, salva no mesmo local do arquivo>")
        entry_output.config(fg="gray")

root = tk.Tk()
root.title("Conversor PDF para 300 DPI")
centralizar_janela(root, largura=650, altura=320)
root.configure(bg="#f0f0f0")  # fundo cinza claro

# Coloque o arquivo icon.ico na mesma pasta do script
try:
    root.iconbitmap("icon.ico")
except Exception as e:
    print(f"Erro ao carregar ícone: {e}")

# Fonte customizada
fonte_label = font.Font(family="Segoe UI", size=10)
fonte_entry = font.Font(family="Segoe UI", size=10)
fonte_btn = font.Font(family="Segoe UI", size=10, weight="bold")
fonte_versao = font.Font(family="Segoe UI", size=8, slant="italic")

# Label da versão no topo
label_versao = tk.Label(root, text="Versão 1.0", font=fonte_versao, bg="#f0f0f0", fg="#666666")
label_versao.pack(pady=(8, 0))  # pequeno padding superior e 0 abaixo

# Frame centralizado para o resto da UI
frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=15)
frame.pack(expand=True)  # Expande e centraliza verticalmente

# Labels e entradas
tk.Label(frame, text="Arquivo PDF:", bg="#f0f0f0", font=fonte_label).grid(row=0, column=0, sticky="e", pady=5)
entry_input = tk.Entry(frame, width=50, font=fonte_entry)
entry_input.grid(row=0, column=1, padx=10, pady=5)
btn_input = tk.Button(frame, text="Selecionar", command=selecionar_arquivo, font=fonte_btn, bg="#4CAF50", fg="white", activebackground="#45a049")
btn_input.grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame, text="Salvar como:", bg="#f0f0f0", font=fonte_label).grid(row=1, column=0, sticky="e", pady=5)
entry_output = tk.Entry(frame, width=50, font=fonte_entry)
entry_output.insert(0, "Opcional. Caso não escolha, salvará no mesmo local do arquivo importado.")
entry_output.config(fg="gray")
entry_output.bind("<FocusIn>", on_entry_output_focus_in)
entry_output.bind("<FocusOut>", on_entry_output_focus_out)
entry_output.grid(row=1, column=1, padx=10, pady=5)

btn_output = tk.Button(frame, text="Selecionar", command=selecionar_saida, font=fonte_btn, bg="#2196F3", fg="white", activebackground="#0b7dda")
btn_output.grid(row=1, column=2, padx=5, pady=5)

btn_convert = tk.Button(frame, text="Converter", command=converter, width=20, font=fonte_btn, bg="#f44336", fg="white", activebackground="#da190b")
btn_convert.grid(row=2, column=1, pady=15)

# Ajuste colunas para expansão proporcional
frame.grid_columnconfigure(1, weight=1)

root.mainloop()
