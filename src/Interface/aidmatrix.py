import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk

# Configurações de aparência
customtkinter.set_appearance_mode("Dark")  # Modos: "System" (padrão), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Temas: "blue" (padrão), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self, graph=None):
        super().__init__()

        self.graph = graph  # Salva o objeto gráfico
        # Configurações da janela
        self.title("CustomTkinter Complex Example")
        self.geometry("1440x900")

        # Configuração do layout em grade
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)  # Ajustar peso para a coluna da imagem
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # Criação da área de conteúdo principal (logo e botões)
        self.logo_label = customtkinter.CTkLabel(self, text="AidMatrix PRO+", font=customtkinter.CTkFont(size=60, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(100, 200), sticky="n")

        # Botões
        self.sidebar_button_1 = customtkinter.CTkButton(self, text="Mostrar Grafo", command=self.show_graph, width=200, height=50)
        self.sidebar_button_1.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self, text="Visualizar Algoritmos", width=200, height=50)
        self.sidebar_button_2.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self, text="Resultados Históricos", width=200, height=50)
        self.sidebar_button_3.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

        # Rótulo para exibir a imagem
        self.image_label = customtkinter.CTkLabel(self, text="", image=None)
        self.image_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="n")

    def show_graph(self):
        root = customtkinter.CTk()
        root.title("grafo.com")
        root.geometry("1680x1050")
        img = customtkinter.CTkImage(light_image=Image.open("graph.png"),dark_image= Image.open("graph.png"), size=(1680,1050))
        my_label = customtkinter.CTkLabel(root, text="", image=img)
        my_label.pack(pady=10)
