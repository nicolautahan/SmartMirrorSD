# -----------------------------------------------------	#
# Teste Tkinter, Json Requests e Clima v1.0				#
#														#
# Nicolau Tahan - 16/03/17								#
# Powered by Dark Sky (https://darksky.net/poweredby/)	#
# -----------------------------------------------------	#

from Tkinter import *
import requests
import json

# Variaveis para o url da API
# Valores disponiveis @ https://darksky.net/dev/docs
clima_token = 'bb32dfc53f3c76134d49fef7e8c83801'
clima_lang = 'pt'
clima_unit = 'si'

fonte = 'CODE Light'
xlarge_text_size = 50
refresh_rate = 300000
text_size = 20
stext_size = 13

class Clima(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)

		self.temp = ''
		self.sumario = ''
		self.previsao = ''

		# Mesma coisa das outras classes, criar todas as labels vazias
		self.tempFR = Frame(self, bg = 'black')
		self.tempFR.pack(side = TOP, anchor = E)
		self.tempLB = Label(self.tempFR, text = self.temp, font = (fonte, xlarge_text_size), bg = 'black', fg = 'white')
		self.tempLB.pack(side = RIGHT, anchor = N)
		self.sumLB = Label(self, text = self.sumario, font = (fonte, text_size), bg = 'black', fg = 'white')
		self.sumLB.pack(side = TOP, anchor = E)
		self.prevLB = Label(self, text = self.previsao, font = (fonte, text_size), bg = 'black', fg = 'white')
		self.prevLB.pack(side = TOP, anchor = E)

		self.get_clima()

	# Metodo para buscar a latitude e longitude
	# TESTE PARA VER SE FUNCIONA NO LAB!!!!!!!!!!!!!
	def get_lat_long(self):
		geo_url = 'http://freegeoip.net/json/'
		req = requests.get(geo_url)
		self.geo_object = json.loads(req.text)

		return self.geo_object['latitude'], self.geo_object['longitude']

	def get_clima(self):
		lat, lon = self.get_lat_long()
		clima_url = 'https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s' % (clima_token, lat, lon, clima_lang, clima_unit)

		# Request para o objeto Clima, toda estrutura disponivel @ https://darksky.net/dev/docs
		clima_req = requests.get(clima_url)
		self.clima_object = json.loads(clima_req.text)

		grau = u'\N{DEGREE SIGN}'
		self.temp2 = str(int(self.clima_object['currently']['temperature'])) + grau # Retirar os pontos decimais
		self.sumario2 = self.clima_object['currently']['summary']
		self.previsao2 = self.clima_object['hourly']['summary']

		# Atualizar os valores das labels caso houver uma mudanca
		if self.temp != self.temp2:
			self.temp = self.temp2
			self.tempLB.config(text = self.temp)
		if self.sumario != self.sumario2:
			self.sumario = self.sumario2
			self.sumLB.config(text = self.sumario)
		if self.previsao != self.previsao2:
			self.previsao = self.previsao2
			self.prevLB.config(text = self.previsao)

		# Chamar a funcao de novo apos um certo tempo
		# OBS: 1000 Calls de graca, alem disso tem que pagar
		self.tempLB.after(refresh_rate, self.get_clima)


# ------------------------------------ BLOCO DE TESTE ------------------------------------------ #
root = Tk()

test_frame = Frame(root, bg = 'black')
test_frame.pack(fill = BOTH, expand = YES)

clima = Clima(test_frame)
clima.pack()

root.mainloop()