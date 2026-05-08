import customtkinter as ctk
import random
import string

# Configuração de Tema
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.geometry("1150x1000") 
app.title("Bunny Guard VIP ⋆𐙚₊˚⊹♡")
app.configure(fg_color="#FFE4E6")


historico_senhas = []

# --- ARTES (Com margens ajustadas para não cortar) ---
LACO_BRAILLE = r"""
       ⢠⡏⠉⠑⢄⠀ ⠀ ⡠⠋⠉⢱⡀
       ⡇⠙⠒⠒⠬⡗⢒⢮⠄⠒⠒⠁⢣
       ⠇⠀⠈⠁⢁⡷⠤⢮⠈⠁⠀⠀⡌
       ⠘⢄⣀⡰⢻⠁⠀⠘⡕⢄⣀⡰⠁
       ⠀⡎⠘⢀⠇⠀⠀⠀⢱⠈⠂⠡⠀
       ⠀⠑⢄⡜⠢⡀⠀⢀⠔⠇⡴⠃⠀
       ⠀⠀⠀⠑⠠⠚⠀⠓⠔⠋⠀⠀
"""

COELHO_BRAILLE = r"""
     ⢀⣤⠤⣄⠀⠀⠀⠀⣠⠤⣄⠀⠀⠀
     ⢠⠞⠀⠀⠈⢷⠀⠀⡜⠃⠀⠈⢳⠀⠀
     ⣾⠀⠀⠀⠀⠘⡇⢰⠅⠀⠀⠀⠸⡇⠀
     ⣿⠀⠀⠀⠀⠀⡇⣾⠀⠀⠀⠀⢸⠃⠀
     ⢹⡀⠀⠀⠀⠀⡇⣿⠀⠀⠀⠀⡾⠀⠀
     ⠸⡇⠀⠀⠀⠀⠷⠿⠀⠀⠀⢰⠇⠀⠀
⢀⡴⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢶⡀⠀
⢰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄
⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷
⢹⠀⠀⠀⢰⡆⠀⠀⠀⠀⠀⠀⢀⣄⠀⠀⠀⡟
⠈⢧⡀⠀⠀⠀⠀⠀⢄⡀⣀⠀⠀⠁⠀⠀⣸⠃
⠀⠈⠻⢦⣀⠀⠀⠀⠚⠙⠂⠀⠀⠀⣀⡴⠋⠀
     ⠈⠉⠓⠒⠲⠶⠶⠒⠒⠋⠁
"""

# --- FUNÇÕES ---

def gerar_senha():
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    senha_gerada = [
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@#$%&*"),
        *(random.choice(caracteres) for _ in range(9))
    ]
    random.shuffle(senha_gerada)
    senha_entry.delete(0, 'end')
    senha_entry.insert(0, "".join(senha_gerada))
    animar()

def limpar_campos():
    senha_entry.delete(0, 'end')
    resultado.configure(text="Esperando... ᨘ⡴⠒⢦", text_color="#9D174D")
    for b in [b1, b2, b3, b4, b_uso]: b.configure(fg_color="#FFFFFF")
    strength_bar.set(0)

def alternar_visualizacao():
    if senha_entry.cget("show") == "*":
        senha_entry.configure(show="")
        btn_olho.configure(text="🔒", fg_color="#DA4BEC")
    else:
        senha_entry.configure(show="*")
        btn_olho.configure(text="🎀", fg_color="#CA2583")

def salvar_senha(nova_senha):
    if nova_senha not in historico_senhas:
        historico_senhas.append(nova_senha)
        caixa_salvas.configure(state="normal")
        caixa_salvas.insert("end", f" • {nova_senha}\n")
        caixa_salvas.configure(state="disabled")

def finalizar_validacao():
    senha = senha_entry.get()
    especiais = "!@#$%&*"
    
    # Critérios
    c1 = len(senha) >= 8
    c2 = any(c.isupper() for c in senha)
    c3 = any(c.isdigit() for c in senha)
    c4 = any(c in especiais for c in senha)
    c5 = senha not in historico_senhas
    
    res = [c1, c2, c3, c4]
    strength_bar.set(sum(res) / 4)
    
    cards = [b1, b2, b3, b4]
    for i, check in enumerate(res):
        cards[i].configure(fg_color="#D1FAE5" if check else "#EE646D")

    if all(res):
        if not c5:
            b_uso.configure(fg_color="#FFE4E6")
            resultado.configure(text="❌ SENHA JÁ UTILIZADA!", text_color="#E11D48")
        else:
            b_uso.configure(fg_color="#D1FAE5")
            resultado.configure(text="✅ SENHA VÁLIDA ✨", text_color="#059669")
            salvar_senha(senha)
    else:
        b_uso.configure(fg_color="#FFFFFF")
        resultado.configure(text="❌ SENHA INVÁLIDA", text_color="#E11D48")

def animar():
    resultado.configure(text="Analisando... ദ്ദി◝ ⩊ ◜.ᐟ", text_color="#2563EB")
    for b in [b1, b2, b3, b4, b_uso]: b.configure(fg_color="#FFFFFF")
    app.after(1000, finalizar_validacao)

# --- INTERFACE ---

titulo_frame = ctk.CTkFrame(app, fg_color="transparent")
titulo_frame.pack(pady=20)

header = ctk.CTkLabel(titulo_frame, text=" ✨𝓑𝓾𝓷𝓷𝔂 𝓖𝓾𝓪𝓻𝓭 𝓥𝓘𝓟 ✨🛡️", font=("Impact", 38), text_color="#831843")
header.pack()

sub_header = ctk.CTkLabel(titulo_frame, text="Ⓟⓞⓛⓘⓣⓘⓒⓐ ⓓⓔ ⓢⓔⓝⓗⓐⓢ", font=("Segoe UI", 20, "bold"), text_color="#CA6991")
sub_header.pack()

container = ctk.CTkFrame(app, fg_color="transparent")
container.pack(fill="x", padx=40)

# ESQUERDA
painel_input = ctk.CTkFrame(container, fg_color="#FFFFFF", border_width=3, border_color="#831843", corner_radius=30)
painel_input.pack(side="left", fill="both", expand=True, padx=15, pady=5)

laco_label = ctk.CTkLabel(painel_input, text=LACO_BRAILLE, font=("Courier New", 16, "bold"), text_color="#BE185D")
laco_label.pack(pady=(15, 0))

resultado = ctk.CTkLabel(painel_input, text="Esperando... ᨘ⡴⠒⢦", font=("Segoe UI", 18, "bold"), text_color="#9D174D")
resultado.pack(pady=5)

strength_bar = ctk.CTkProgressBar(painel_input, width=300, height=12, fg_color="#F3F4F6", progress_color="#F472B6")
strength_bar.set(0)
strength_bar.pack(pady=5)

input_area = ctk.CTkFrame(painel_input, fg_color="transparent")
input_area.pack(pady=5, padx=50, fill="x")

senha_entry = ctk.CTkEntry(input_area, placeholder_text="Senha... ♡", height=45, show="*", border_width=2, border_color="#F472B6")
senha_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

btn_olho = ctk.CTkButton(input_area, text="🎀", width=50, height=45, fg_color="#CA2583", command=alternar_visualizacao)
btn_olho.pack(side="right")

# Dashboard de botões
btns_frame = ctk.CTkFrame(painel_input, fg_color="transparent")
btns_frame.pack(pady=10)
ctk.CTkButton(btns_frame, text="VERIFICAR", font=("Impact", 20), fg_color="#DB2777", height=50, width=140, corner_radius=15, command=animar).grid(row=0, column=0, padx=5)
ctk.CTkButton(btns_frame, text="GERAR 🎲", font=("Impact", 20), fg_color="#831843", height=50, width=100, corner_radius=15, command=gerar_senha).grid(row=0, column=1, padx=5)

ctk.CTkButton(painel_input, text="Limpar", font=("Segoe UI", 12), fg_color="transparent", text_color="#831843", width=60, command=limpar_campos).pack()

# DIREITA
painel_check = ctk.CTkFrame(container, fg_color="#FDF2F8", border_width=3, border_color="#831843", corner_radius=30)
painel_check.pack(side="right", fill="both", expand=True, padx=15, pady=5)

# Aumentei o width e travei a fonte para o coelho não cortar
coelho_display = ctk.CTkTextbox(painel_check, font=("Courier New", 12), text_color="#831843", fg_color="transparent", width=380, height=320)
coelho_display.pack(pady=(15, 0))
coelho_display.insert("0.0", COELHO_BRAILLE)
coelho_display.configure(state="disabled")

def criar_card(texto):
    f = ctk.CTkFrame(painel_check, fg_color="#FFFFFF", height=42, border_width=1, border_color="#F472B6", corner_radius=12)
    f.pack(fill="x", padx=40, pady=3)
    f.pack_propagate(False)
    l = ctk.CTkLabel(f, text=texto, font=("Segoe UI", 11, "bold"), text_color="#831843")
    l.pack(expand=True)
    return f

b1, b2, b3, b4, b_uso = criar_card("♡ 8 Cᴀʀᴀᴄᴛᴇʀᴇs"), criar_card("♡ Lᴇᴛʀᴀ Mᴀɪúsᴄᴜʟᴀ"), criar_card("♡ Núᴍᴇʀᴏ"), criar_card("♡ Cᴀʀᴀᴄᴛᴇʀᴇ Esᴘᴇᴄɪᴀʟ"), criar_card("♡ Sᴇɴʜᴀ Nᴜɴᴄᴀ Usᴀᴅᴀ")

# COFRE
painel_salvas = ctk.CTkFrame(app, fg_color="#FFFFFF", border_width=3, border_color="#831843", corner_radius=25)
painel_salvas.pack(fill="x", padx=55, pady=20)

ctk.CTkLabel(painel_salvas, text="📂 𝓢𝓮𝓷𝓱𝓪𝓼 𝓼𝓪𝓵𝓿𝓪𝓼", font=("Segoe UI", 14, "bold"), text_color="#831843").pack(pady=5)

caixa_salvas = ctk.CTkTextbox(painel_salvas, height=120, fg_color="#FDF2F8", border_width=1, border_color="#F472B6", font=("Consolas", 11))
caixa_salvas.pack(fill="x", padx=20, pady=(0, 15))
caixa_salvas.insert("0.0", "𝐒𝐞𝐧𝐡𝐚𝐬 𝐮𝐭𝐢𝐥𝐢𝐳𝐚𝐝𝐚𝐬:\n")
for s in historico_senhas: caixa_salvas.insert("end", f" • {s}\n")
caixa_salvas.configure(state="disabled")

app.mainloop()