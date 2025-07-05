from machine import Pin, SPI
from modules/ili9341_display import ILI9341, TextLineLayout, color565
from modules/thingspeak_driver import ThingSpeak
import dht
import time

# ========== Inicialização do thingSpeak ==========
ts = ThingSpeak()
if not ts.setup("YOUR UPDATE API KEY"):
    print("Erro na conexão com a rede ThingSpeak.")

# ========== Inicialização do Sensor ==========
sensor = dht.DHT22(Pin(21))

# ========== Inicialização do Display ==========
spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
cs = Pin(15)
dc = Pin(2)
rst = Pin(4)
display = ILI9341(spi, cs, dc, rst)

# ========== Definição de Cores ==========
WHITE = color565(255, 255, 255)
RED = color565(255, 0, 0)
BLACK = color565(0, 0, 0)
BLUE = color565(0, 0, 255)

# ========== Layout Inicial ==========
display.fill_screen(WHITE)
display.draw_rect_percent(0, 0, 1, 0.16, RED)
display.draw_text(0.5, 0.04, "Dados:", WHITE, scale=2)

layout_temp = TextLineLayout(
    display,
    text_fixo="Temp.: ",
    x_pct=0.73,
    y_pct=0.25,
    color_fixo=BLUE,
    color_var=BLACK,
    bg_color=WHITE,
    scale=2
)

layout_umid = TextLineLayout(
    display,
    text_fixo="Umid.: ",
    x_pct=0.73,
    y_pct=0.4,
    color_fixo=BLUE,
    color_var=BLACK,
    bg_color=WHITE,
    scale=2
)

# Layout para "Enviando..."
layout_status = TextLineLayout(
    display,
    text_fixo="",
    x_pct=1.3,
    y_pct=0.7,
    color_fixo=BLACK,
    color_var=BLACK,
    bg_color=WHITE,
    scale=2
)

# ========== Loop Principal ==========
erro_count = 0
MAX_ERROS = 3

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        erro_count = 0

        layout_temp.update_var_text("{:.1f}C".format(temp), color=BLACK)
        layout_umid.update_var_text("{:.1f}%".format(hum), color=BLACK)

        # Exibir status "Enviando..."
        layout_status.update_var_text("Enviando...", color=BLACK)

        # Envio direto
        sucesso = ts.send_data(temperatura=temp, umidade=hum)

        # Limpar status após envio
        layout_status.update_var_text("")

        if not sucesso:
            print("Falha ao enviar dados ao ThingSpeak.")

        print("Umidade: {:.1f}% | Temperatura: {:.1f}°C".format(hum, temp))

    except Exception as e:
        erro_count += 1
        print(f"[{erro_count}] Erro ao ler o DHT22:", e)

        if erro_count >= MAX_ERROS:
            layout_temp.update_var_text("Erro", color=RED)
            layout_umid.update_var_text("Erro", color=RED)
            layout_status.update_var_text("Erro", color=RED)
            print("Erro contínuo: sensor não respondeu.")
            erro_count = 0

    time.sleep(20)
  
