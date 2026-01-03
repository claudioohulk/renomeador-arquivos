import os
import tkinter as tk
from tkinter import filedialog, messagebox

def selecionar_pasta():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta_selecionada)

def gerar_nome_unico(caminho, nome_arquivo):
    base, ext = os.path.splitext(nome_arquivo)
    contador = 2
    novo_nome = nome_arquivo

    while os.path.exists(os.path.join(caminho, novo_nome)):
        novo_nome = f"{base} ({contador}){ext}"
        contador += 1

    return novo_nome

def renomear_arquivos():
    pasta = entry_pasta.get()
    texto_antigo = entry_antigo.get()
    texto_novo = entry_novo.get()
    incluir_subpastas = var_subpastas.get()

    if not pasta or not texto_antigo:
        messagebox.showerror("Erro", "Por favor, preencha a pasta e o texto a substituir.")
        return

    arquivos_para_renomear = []

    if incluir_subpastas:
        for raiz, _, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                novo_nome = arquivo.replace(texto_antigo, texto_novo)
                if novo_nome != arquivo:
                    arquivos_para_renomear.append((raiz, arquivo, novo_nome))
    else:
        for arquivo in os.listdir(pasta):
            caminho = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho):
                novo_nome = arquivo.replace(texto_antigo, texto_novo)
                if novo_nome != arquivo:
                    arquivos_para_renomear.append((pasta, arquivo, novo_nome))

    if not arquivos_para_renomear:
        messagebox.showinfo("Info", "Nenhum arquivo para renomear.")
        return

    abrir_previsualizacao(arquivos_para_renomear)

def abrir_previsualizacao(lista_arquivos):
    preview = tk.Toplevel(janela)
    preview.title("Pré-visualização da seleção de arquivos")
    preview.geometry("650x400")

    canvas = tk.Canvas(preview)
    scrollbar = tk.Scrollbar(preview, orient="vertical", command=canvas.yview)
    frame_lista = tk.Frame(canvas)

    frame_lista.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_lista, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    vars_check = []

    for raiz, antigo, novo in lista_arquivos:
        var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(
            frame_lista,
            text=antigo,
            variable=var,
            anchor="w",
            justify="left"
        )
        chk.pack(fill="x", anchor="w")
        vars_check.append((var, raiz, antigo, novo))

    def confirmar():
        count = 0
        for var, raiz, antigo, novo in vars_check:
            if var.get():
                destino = novo
                if var_conflitos.get():
                    destino = gerar_nome_unico(raiz, novo)

                try:
                    os.rename(
                        os.path.join(raiz, antigo),
                        os.path.join(raiz, destino)
                    )
                    count += 1
                except Exception as e:
                    messagebox.showerror("Erro", str(e))

        preview.destroy()
        messagebox.showinfo("Sucesso", f"{count} arquivos renomeados com sucesso!")

    frame_opcoes = tk.Frame(preview)
    frame_opcoes.pack(pady=5)

    tk.Checkbutton(
        frame_opcoes,
        text="Detectar conflitos de nomes e numerar automaticamente",
        variable=var_conflitos
    ).pack()

    frame_botoes = tk.Frame(preview)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Confirmar Renomeação", command=confirmar).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Cancelar", command=preview.destroy).pack(side="left", padx=5)

# Janela principal
janela = tk.Tk()
janela.title("Renomeador de Arquivos")
janela.geometry("400x300")

tk.Label(janela, text="Pasta dos arquivos:").pack(pady=5)
entry_pasta = tk.Entry(janela, width=50)
entry_pasta.pack()
tk.Button(janela, text="Selecionar Pasta", command=selecionar_pasta).pack()

tk.Label(janela, text="Texto a substituir:").pack(pady=5)
entry_antigo = tk.Entry(janela, width=50)
entry_antigo.pack()

tk.Label(janela, text="Texto novo:").pack(pady=5)
entry_novo = tk.Entry(janela, width=50)
entry_novo.pack()

var_subpastas = tk.BooleanVar()
tk.Checkbutton(
    janela,
    text="Renomear arquivos das subpastas",
    variable=var_subpastas
).pack(pady=5)

var_conflitos = tk.BooleanVar(value=True)

tk.Button(janela, text="Renomear Arquivos", command=renomear_arquivos).pack(pady=10)

janela.mainloop()
