import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout


import matplotlib.pyplot as plt
import os
import functions  # importa seu arquivo com as codificações


def plotar(tempo, sinal, titulo=""):
    plt.figure(figsize=(10, 3))
    plt.title(titulo)
    plt.plot(tempo, sinal, drawstyle='steps-post')
    plt.ylim(-2, 2)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafico.png")
    plt.close()


class TelaMenuInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        btn_gerar = Button(text="Gerar Gráficos", size_hint=(0.4, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.6})
        btn_gerar.bind(on_press=self.ir_para_entrada)
        layout.add_widget(btn_gerar)

        btn_sobre = Button(text="Sobre os Códigos de Linha", size_hint=(0.4, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.3})
        btn_sobre.bind(on_press=self.abrir_popup_sobre)
        layout.add_widget(btn_sobre)

        self.add_widget(layout)

    def ir_para_entrada(self, *args):
        self.manager.current = "entrada_bits"


    def abrir_popup_sobre(self, *args):
        texto = (
            "Este trabalho implementa esquemas de codificação de linha como NRZ-L, NRZ-I, AMI, "
            "Pseudoternário, Manchester e Manchester Diferencial. São técnicas utilizadas em comunicação digital "
            "para transformar bits em sinais físicos transmitíveis.\n\n"
            "Esses métodos ajudam a garantir sincronização entre transmissor e receptor, reduzir o consumo de energia, "
            "e permitir a detecção de erros. Cada técnica possui características distintas e é adequada para diferentes cenários."
        )

        # Layout principal com padding
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Botão X de fechar (alinhado à direita)
        fechar_layout = AnchorLayout(anchor_x='right', anchor_y='top', size_hint=(1, None), height=40)
        btn_fechar = Button(text='X', size_hint=(None, None), size=(40, 40))
        fechar_layout.add_widget(btn_fechar)
        content.add_widget(fechar_layout)

        # Scroll com texto
        scroll = ScrollView(size_hint=(1, 1))
        label = Label(
            text=texto,
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='16sp',
            text_size=(660, None),  
            padding=(20, 10)        # padding nas laterais e topo/baixo
        )
        label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1]))
        scroll.add_widget(label)

        content.add_widget(scroll)

        # Popup
        popup = Popup(title="Sobre os Códigos de Linha",
                    content=content,
                    size_hint=(0.9, 0.7),
                    auto_dismiss=False)

        # Botão fecha o popup
        btn_fechar.bind(on_release=popup.dismiss)
        popup.open()


class TelaEntradaBits(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.indice_codificacao = 0
        self.layout = FloatLayout()

        self.entrada = TextInput(hint_text="Digite a sequência binária", multiline=False,
                                 size_hint=(0.8, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.7})
        self.layout.add_widget(self.entrada)

        self.label_codificacao = Label(text=functions.codificacoes[self.indice_codificacao],
                                       size_hint=(0.8, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.4}) #AHAHA
        self.layout.add_widget(self.label_codificacao)

        btn_ok = Button(text="OK", size_hint=(0.2, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.5})
        btn_ok.bind(on_press=self.gerar_grafico)
        self.layout.add_widget(btn_ok)

        btn_anterior = Button(text="Anterior", size_hint=(0.2, 0.15), pos_hint={"center_x": 0.25, "center_y": 0.5})
        btn_anterior.bind(on_press=self.codificacao_anterior)
        self.layout.add_widget(btn_anterior)

        btn_proximo = Button(text="Próximo", size_hint=(0.2, 0.15), pos_hint={"center_x": 0.75, "center_y": 0.5})
        btn_proximo.bind(on_press=self.codificacao_proxima)
        self.layout.add_widget(btn_proximo)

        btn_voltar = Button(text="Voltar", size_hint=(0.2, 0.1), pos_hint={"x": 0.02, "top": 0.98})
        btn_voltar.bind(on_press=self.voltar)
        self.layout.add_widget(btn_voltar)

        self.imagem = Image(size_hint=(0.9, 0.35), pos_hint={"center_x": 0.5, "y": 0.02})
        self.layout.add_widget(self.imagem)

        self.add_widget(self.layout)

    def gerar_grafico(self, *args):
        bits = self.entrada.text.strip()
        if not all(b in '01' for b in bits):
            popup = Popup(title="Erro", content=Label(text="Digite apenas 0 e 1."),
                          size_hint=(0.6, 0.3))
            popup.open()
            return

        nome_codificacao = functions.codificacoes[self.indice_codificacao]
        funcao = functions.funcoes_codificacao[nome_codificacao]

        tempo, sinal = funcao(bits)
        plotar(tempo, sinal, titulo=f"{nome_codificacao} para bits: {bits}")

        if os.path.exists("grafico.png"):
            self.imagem.source = "grafico.png"
            self.imagem.reload()

    def codificacao_anterior(self, *args):
        self.indice_codificacao = (self.indice_codificacao - 1) % len(functions.codificacoes)
        self.label_codificacao.text = functions.codificacoes[self.indice_codificacao]
        
        if self.entrada.text.strip():
            self.gerar_grafico()

    def codificacao_proxima(self, *args):
        self.indice_codificacao = (self.indice_codificacao + 1) % len(functions.codificacoes)
        self.label_codificacao.text = functions.codificacoes[self.indice_codificacao]
        
        if self.entrada.text.strip():
            self.gerar_grafico()


    def voltar(self, *args):
        self.manager.current = "menu_inicial"


class LineCodeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaMenuInicial(name="menu_inicial"))
        sm.add_widget(TelaEntradaBits(name="entrada_bits"))
        return sm


if __name__ == '__main__':
    LineCodeApp().run()
