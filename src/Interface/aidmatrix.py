import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image

# Configurações de aparência
customtkinter.set_appearance_mode("Dark")  # Modos: "System" (padrão), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Temas: "blue" (padrão), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self, graph = None):
        super().__init__()


        self.graph = graph
        # Configurações da janela
        self.title("CustomTkinter complex_example.py")
        self.geometry("1440x900")

        # Configuração do layout em grade
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)  # Ajustar peso para a coluna da imagem
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)  # Aumenta o peso da linha 1 para centralizar os botões
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # Criação da área de conteúdo principal (logo e botões)
        self.logo_label = customtkinter.CTkLabel(self, text="AidMatrix PRO+", font=customtkinter.CTkFont(size=60, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(100, 200), sticky="n")  # Coloca o logo mais para cima e centralizado

        # Botões para diferentes seções com tamanho maior
        self.sidebar_button_1 = customtkinter.CTkButton(self, text="Mostrar Grafo", command=self.show_graph, width=200, height=50)
        self.sidebar_button_1.grid(row=1, column=0, columnspan=2, padx=20, pady=10)  # Centraliza os botões
        
        self.sidebar_button_2 = customtkinter.CTkButton(self, text="Visualizar Algoritmos", width=200, height=50)
        self.sidebar_button_2.grid(row=2, column=0, columnspan=2, padx=20, pady=10)  # Centraliza os botões
        
        self.sidebar_button_3 = customtkinter.CTkButton(self, text="Resultados Históricos", width=200, height=50)
        self.sidebar_button_3.grid(row=3, column=0, columnspan=2, padx=20, pady=10)  # Centraliza os botões

        # Criação de um rótulo para exibir a imagem quando o botão for clicado
        self.image_label = customtkinter.CTkLabel(self, text="", image=None)  # Inicialmente vazio
        self.image_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="n")  # Ajustar a posição da imagem


    def show_graph(self):
        pass


