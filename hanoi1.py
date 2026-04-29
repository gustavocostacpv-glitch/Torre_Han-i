import tkinter as tk
from tkinter import messagebox

class HanoiVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi - Interactive")
        self.root.geometry("8000x500")
        self.root.configure(bg="#121212")

        self.cores = ["#FF5E5E", "#FFBD44", "#33FF57", "#33CCFF", "#A29BFE", "#F06292"]
        
        # Painel Lateral
        self.side_panel = tk.Frame(root, bg="#1e1e1e", width=200)
        self.side_panel.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(self.side_panel, text="MODO JOGO", fg="#00FFC2", 
                 bg="#1e1e1e", font=("Arial", 12, "bold")).pack(pady=20)

        tk.Label(self.side_panel, text="Discos:", fg="white", bg="#1e1e1e").pack()
        self.slider = tk.Scale(self.side_panel, from_=1, to=8, orient="horizontal",
                               bg="#1e1e1e", fg="white", highlightthickness=0)
        self.slider.set(3)
        self.slider.pack(pady=10, padx=10)

        self.btn_reset = tk.Button(self.side_panel, text="RECOMEÇAR", command=self.resetar_jogo,
                                  bg="#00FFC2", fg="#121212", font=("Arial", 10, "bold"),
                                  relief="flat", cursor="hand2", width=15)
        self.btn_reset.pack(pady=10)

        self.lbl_movimentos = tk.Label(self.side_panel, text="Movimentos: 0", 
                                       fg="#bdc3c7", bg="#1e1e1e")
        self.lbl_movimentos.pack(side="bottom", pady=20)

        # Canvas
        self.canvas = tk.Canvas(root, bg="#121212", highlightthickness=0)
        self.canvas.pack(side="right", expand=True, fill="both")
        
        # Variáveis de controle de arrasto
        self.disco_selecionado = None
        self.origem_pino = None
        self.pos_inicial = None
        
        self.resetar_jogo()

        # Eventos de Mouse
        self.canvas.bind("<Button-1>", self.clicar)
        self.canvas.bind("<B1-Motion>", self.arrastar)
        self.canvas.bind("<ButtonRelease-1>", self.soltar)

    def desenhar_cenario(self):
        self.canvas.delete("all")
        self.pinos_x = []
        for i in range(3):
            x = (i + 1) * (600 / 4)
            self.pinos_x.append(x)
            self.canvas.create_rectangle(x-5, 100, x+5, 400, fill="#34495e", outline="")
            self.canvas.create_text(x, 420, text=f"Pino {chr(65+i)}", fill="white")

    def resetar_jogo(self):
        self.desenhar_cenario()
        n = self.slider.get()
        self.mov_count = 0
        self.lbl_movimentos.config(text="Movimentos: 0")
        self.torres = [list(range(n, 0, -1)), [], []]
        self.discos_gui = {}

        for i, disco in enumerate(self.torres[0]):
            self.criar_disco_visual(0, i, disco)

    def criar_disco_visual(self, pino_idx, altura_idx, valor):
        x = self.pinos_x[pino_idx]
        y = 380 - (altura_idx * 22)
        w = valor * 30 + 20
        cor = self.cores[valor % len(self.cores)]
        id_disco = self.canvas.create_rectangle(x-w/2, y, x+w/2, y+20, 
                                                fill=cor, outline="white", tags=f"disco_{valor}")
        self.discos_gui[valor] = id_disco

    def clicar(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        if tags and "disco_" in tags[0]:
            valor_disco = int(tags[0].split("_")[1])
            
            # Verificar se é o disco no topo de alguma torre
            for i, torre in enumerate(self.torres):
                if torre and torre[-1] == valor_disco:
                    self.disco_selecionado = valor_disco
                    self.origem_pino = i
                    self.pos_inicial = self.canvas.coords(item)
                    return

    def arrastar(self, event):
        if self.disco_selecionado:
            id_disco = self.discos_gui[self.disco_selecionado]
            coords = self.canvas.coords(id_disco)
            w = coords[2] - coords[0]
            h = 20
            self.canvas.coords(id_disco, event.x - w/2, event.y - h/2, event.x + w/2, event.y + h/2)

    def soltar(self, event):
        if self.disco_selecionado is None:
            return

        # Descobrir pino mais próximo
        destino_pino = None
        menor_distancia = 50 
        for i, px in enumerate(self.pinos_x):
            dist = abs(event.x - px)
            if dist < menor_distancia:
                destino_pino = i
                
        id_disco = self.discos_gui[self.disco_selecionado]
        
        # Validar Movimento
        valido = False
        if destino_pino is not None:
            # Se a torre de destino estiver vazia ou o disco for menor que o topo
            if not self.torres[destino_pino] or self.disco_selecionado < self.torres[destino_pino][-1]:
                valido = True

        if valido and destino_pino != self.origem_pino:
            # Executar movimento
            self.torres[self.origem_pino].pop()
            self.torres[destino_pino].append(self.disco_selecionado)
            self.mov_count += 1
            self.lbl_movimentos.config(text=f"Movimentos: {self.mov_count}")
            
            # Posicionar corretamente no pino
            self.posicionar_no_pino(id_disco, destino_pino, len(self.torres[destino_pino]) - 1)
            
            # Checar vitória
            if len(self.torres[2]) == self.slider.get():
                messagebox.showinfo("Parabéns!", "Você resolveu o puzzle!")
        else:
            # Voltar para posição original
            self.canvas.coords(id_disco, *self.pos_inicial)

        self.disco_selecionado = None

    def posicionar_no_pino(self, id_disco, pino_idx, altura_idx):
        x = self.pinos_x[pino_idx]
        y = 380 - (altura_idx * 22)
        coords = self.canvas.coords(id_disco)
        w = coords[2] - coords[0]
        self.canvas.coords(id_disco, x-w/2, y, x+w/2, y+20)

if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiVisual(root)
    root.mainloop()
