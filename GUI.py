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
import encode
import decode


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

        btn_gerar = Button(text="Codificar", size_hint=(0.4, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.75})
        btn_gerar.bind(on_press=self.ir_para_codificacao)
        layout.add_widget(btn_gerar)

        btn_gerar = Button(text="Decodificar", size_hint=(0.4, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.5})
        btn_gerar.bind(on_press=self.ir_para_decodificacao)
        layout.add_widget(btn_gerar)


        btn_sobre = Button(text="Sobre os Códigos de Linha", size_hint=(0.4, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.25})
        btn_sobre.bind(on_press=self.abrir_popup_sobre)
        layout.add_widget(btn_sobre)

        copyright_label = Label(
            text="Ohana LTDA © 2025 - Todos os direitos reservados.",
            size_hint=(1, 0.05),
            pos_hint={"center_x": 0.5, "y": 0.05}
        )
        layout.add_widget(copyright_label)


        self.add_widget(layout)

    def ir_para_codificacao(self, *args):
        self.manager.current = "codificar_bits"

    def ir_para_decodificacao(self, *args):
        self.manager.current = "decodificar_bits"


    def abrir_popup_sobre(self, *args):
        texto1 = (
            "Este trabalho implementa esquemas de codificação de linha como NRZ-L, NRZ-I, AMI, "
            "Pseudoternário, Manchester e Manchester Diferencial. São técnicas utilizadas em comunicação digital "
            "para transformar bits em sinais físicos transmitíveis.\n\n"
            "Esses métodos ajudam a garantir sincronização entre transmissor e receptor, reduzir o consumo de energia, "
            "e permitir a detecção de erros. Cada técnica possui características distintas e é adequada para diferentes cenários."
        )

        texto2 = (
            "Feito com amor por:\n\nCarlos Eduardo Velozo\nDavi de Castro Machado\nLucas Xavier Pairé\nMiguel Brondani"
        )

        # Layout principal com padding
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Botão X de fechar (alinhado à direita)
        fechar_layout = AnchorLayout(anchor_x='right', anchor_y='top', size_hint=(1, None), height=40)
        btn_fechar = Button(text='X', size_hint=(None, None), size=(40, 40))
        fechar_layout.add_widget(btn_fechar)
        content.add_widget(fechar_layout)

        # Scroll com o texto principal (texto1)
        scroll = ScrollView(size_hint=(1, 1))
        label = Label(
            text=texto1,
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='16sp',
            text_size=(660, None),
            padding=(20, 10)  # Padding nas laterais e topo/baixo
        )
        label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1]))
        scroll.add_widget(label)
        content.add_widget(scroll)

        # Adicionando o texto2 (centralizado horizontalmente)
        label2 = Label(
            text=texto2,
            size_hint_y=0.8,
            halign='center',  # Centraliza horizontalmente
            valign='middle',  # Centraliza verticalmente dentro do espaço
            font_size='16sp',
            text_size=(660, None),
            padding=(20, 10)
        )
        content.add_widget(label2)

        # Popup
        popup = Popup(title="Sobre os Códigos de Linha",
                    content=content,
                    size_hint=(0.9, 0.7),
                    auto_dismiss=False)

        # Botão fecha o popup
        btn_fechar.bind(on_release=popup.dismiss)
        popup.open()


class TelaCodificacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.indice_codificacao = 0
        self.layout = FloatLayout()

        self.entrada = TextInput(hint_text="Digite a sequência binária", multiline=False,
                                 size_hint=(0.8, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.7})
        self.layout.add_widget(self.entrada)

        self.label_codificacao = Label(text=encode.codificacoes[self.indice_codificacao],
                                       size_hint=(0.8, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.4}) 
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

        btn_voltar = Button(text="Decodificação", size_hint=(0.2, 0.1), pos_hint={"x": 0.75, "top": 0.98})
        btn_voltar.bind(on_press=self.ir_para_decodificacao)
        self.layout.add_widget(btn_voltar)

        self.imagem = Image(size_hint=(0.9, 0.35), pos_hint={"center_x": 0.5, "y": 0.02})
        self.layout.add_widget(self.imagem)

        self.add_widget(self.layout)

    def ir_para_decodificacao(self, *args):
        self.manager.current = "decodificar_bits"

    def gerar_grafico(self, *args):
        bits = self.entrada.text.strip()
        if not all(b in '01' for b in bits):
            
            content = FloatLayout()

            lbl = Label(
                text="Digite apenas 0 e 1.",
                size_hint=(1, 0.8),
                pos_hint={"x": 0, "y": 0.1}
            )
            content.add_widget(lbl)

            btn_fechar = Button(
                text="X",
                size_hint=(None, None),
                size=(35, 35),
                pos_hint={"right": 1, "top": 1.22}
            )
            content.add_widget(btn_fechar)

            popup = Popup(
                title="Erro",
                content=content,
                size_hint=(0.6, 0.4),
                auto_dismiss=False
            )

            btn_fechar.bind(on_release=popup.dismiss)

            popup.open()
            return

        nome_codificacao = encode.codificacoes[self.indice_codificacao]
        funcao = encode.funcoes_codificacao[nome_codificacao]

        tempo, sinal = funcao(bits)
        plotar(tempo, sinal, titulo=f"{nome_codificacao} para bits: {bits}   Sinais de saída: {sinal}")

        if os.path.exists("grafico.png"):
            self.imagem.source = "grafico.png"
            self.imagem.reload()

    def codificacao_anterior(self, *args):
        self.indice_codificacao = (self.indice_codificacao - 1) % len(encode.codificacoes)
        self.label_codificacao.text = encode.codificacoes[self.indice_codificacao]
        
        if self.entrada.text.strip():
            self.gerar_grafico()

    def codificacao_proxima(self, *args):
        self.indice_codificacao = (self.indice_codificacao + 1) % len(encode.codificacoes)
        self.label_codificacao.text = encode.codificacoes[self.indice_codificacao]
        
        if self.entrada.text.strip():
            self.gerar_grafico()


    def voltar(self, *args):
        self.manager.current = "menu_inicial"


class TelaDecodificacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.indice_decodificacao = 0
        self.layout = FloatLayout()

        self.entrada = TextInput(hint_text="Digite a sequência de sinais (ex: -1 1 1 -1)", multiline=False,
                                 size_hint=(0.8, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.7})
        self.layout.add_widget(self.entrada)

        self.label_decodificacao = Label(
            text=decode.decodificacoes[self.indice_decodificacao],
            size_hint=(0.8, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.3}
        )
        self.layout.add_widget(self.label_decodificacao)

        btn_ok = Button(text="OK", size_hint=(0.2, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.5})
        btn_ok.bind(on_press=self.gerar_saida)
        self.layout.add_widget(btn_ok)

        btn_anterior = Button(text="Anterior", size_hint=(0.2, 0.15),
                              pos_hint={"center_x": 0.25, "center_y": 0.5})
        btn_anterior.bind(on_press=self.decodificacao_anterior)
        self.layout.add_widget(btn_anterior)

        btn_proximo = Button(text="Próximo", size_hint=(0.2, 0.15),
                             pos_hint={"center_x": 0.75, "center_y": 0.5})
        btn_proximo.bind(on_press=self.decodificacao_proxima)
        self.layout.add_widget(btn_proximo)

        btn_voltar = Button(text="Voltar", size_hint=(0.2, 0.1),
                            pos_hint={"x": 0.02, "top": 0.98})
        btn_voltar.bind(on_press=self.voltar)
        self.layout.add_widget(btn_voltar)

        btn_cod = Button(text="Codificação", size_hint=(0.2, 0.1),
                         pos_hint={"x": 0.75, "top": 0.98})
        btn_cod.bind(on_press=self.ir_para_codificacao)
        self.layout.add_widget(btn_cod)

        # Label de resultado ou erro
        self.resultado_label = Label(
            text="Resultado da Decodificação:",
            size_hint=(0.8, 0.15), pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        self.layout.add_widget(self.resultado_label)

        self.add_widget(self.layout)

    def ir_para_codificacao(self, *args):
        self.manager.current = "codificar_bits"

    def gerar_saida(self, *args):
        sinais_texto = self.entrada.text.strip()
        sinais_list = sinais_texto.split()

        # 1) validação de caracteres
        if not all(b in ('-1', '0', '1') for b in sinais_list):
            self.resultado_label.text = "Digite apenas -1, 0 ou 1."
            return

        nome = decode.decodificacoes[self.indice_decodificacao]
        funcao = decode.funcoes_decodificacao[nome]

        # 2) validação de múltiplos de amostras por bit
        requisitos = {
            "NRZ-L": 1,
            "NRZ-I": 1,
            "AMI": 1,
            "Pseudoternário": 2,
            "MLT-3": 2,
            "Manchester": 4,
            "Manchester Diferencial": 4,
            "8B/6T": 6
        }
        req = requisitos.get(nome, 1)
        if len(sinais_list) % req != 0:
            self.resultado_label.text = f"O método {nome} precisa de múltiplos de {req} amostras."
            return

        # 3) chama a decodificação
        try:
            bits = funcao(sinais_list)
        except Exception as e:
            # Em caso de erro interno
            self.resultado_label.text = f"Erro ao decodificar: {e}"
            return

        # 4) exibe o resultado
        self.resultado_label.text = f"Resultado da Decodificação: {''.join(bits)}"

    def decodificacao_anterior(self, *args):
        self.indice_decodificacao = (self.indice_decodificacao - 1) % len(decode.decodificacoes)
        self.label_decodificacao.text = decode.decodificacoes[self.indice_decodificacao]
        if self.entrada.text.strip():
            self.gerar_saida()

    def decodificacao_proxima(self, *args):
        self.indice_decodificacao = (self.indice_decodificacao + 1) % len(decode.decodificacoes)
        self.label_decodificacao.text = decode.decodificacoes[self.indice_decodificacao]
        if self.entrada.text.strip():
            self.gerar_saida()

    def voltar(self, *args):
        self.manager.current = "menu_inicial"



class LineCodeApp(App):
    def build(self):
        self.title = "LineCode - Alpha 1.0"
        sm = ScreenManager()
        sm.add_widget(TelaMenuInicial(name="menu_inicial"))
        sm.add_widget(TelaCodificacao(name="codificar_bits"))
        sm.add_widget(TelaDecodificacao(name="decodificar_bits"))
        return sm


if __name__ == '__main__':
    LineCodeApp().run()
