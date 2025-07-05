import urequests

import network

import time



class ThingSpeak:

    def __init__(self):

        self.api_key = None

        self.base_url = "https://api.thingspeak.com/update"

        self.last_send_time = 0

        self.min_interval = 15  # segundos



    def connect_wifi(self, ssid, password):

        wlan = network.WLAN(network.STA_IF)

        wlan.active(True)



        if wlan.isconnected():

            return True



        print("Conectando ao WiFi...")

        wlan.connect(ssid, password)

        for _ in range(10):

            if wlan.isconnected():

                print("Conectado:", wlan.ifconfig())

                return True

            time.sleep(1)



        print("Falha ao conectar ao WiFi.")

        return False



    def setup(self, api_key, ssid="Wokwi-GUEST", password=""):

        self.api_key = api_key

        return self.connect_wifi(ssid, password)



    def send_data(self, **fields):

        if not self.api_key:

            print("API Key não definida.")

            return False



        now = time.time()

        if now - self.last_send_time < self.min_interval:

            print("Aguardando intervalo mínimo entre envios...")

            return False



        data = {"api_key": self.api_key}

        for i, value in enumerate(fields.values(), start=1):

            if i > 8:

                break

            data[f"field{i}"] = value



        try:

            response = urequests.post(self.base_url, json=data, headers={'Content-Type': 'application/json'})

            if response.status_code == 200:

                print("Dados enviados com sucesso.")

                self.last_send_time = now

                return True

            print("Erro ao enviar:", response.status_code)

        except Exception as e:

            print("Erro de conexão:", e)

        finally:

            try:

                response.close()

            except:

                pass

        return False

