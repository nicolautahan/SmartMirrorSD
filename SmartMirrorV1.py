# -----------------------------------------------------	#
# SmartMirror v1.0 										#
#														#
# Nicolau Tahan e Arthur Demarchi - 29/03/17			#
#														#
# Powered by Dark Sky (https://darksky.net/poweredby/)	#
# -----------------------------------------------------	#

from Tkinter import *
import time
import feedparser
import json
import requests

# -------------------------------- Variaveis Globais -------------------------------------------------- #

clima_token = 'bb32dfc53f3c76134d49fef7e8c83801'
clima_lang = 'en'
clima_unit = 'si'

fonte = 'CODE Light'
small_text_size = 13
medium_text_size = 17
text_size = 20
large_text_size = 35
xlarge_text_size = 60

time_refresh_rate = 200 #ms
refresh_rate = 60000 #ms

# --------------------------------- Classes ------------------------------------------------------------ #

class Relogio(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg='black')

		# Defina as variaveis internas
		self.hora = ''
		self.dia_semana = ''
		self.data = ''

		# Defina as Labels do tempo, dia da semana e data
		self.horaLB = Label(self, text= self.hora, font=(fonte, xlarge_text_size), fg = 'white', bg = 'black')
		self.horaLB.pack(side = TOP, anchor = W)

		self.dia_semanaLB = Label(self, text= self.dia_semana, font=(fonte, small_text_size), fg = 'white', bg = 'black')
		self.dia_semanaLB.pack(side = TOP, anchor = W)

		self.dataLB = Label(self, text= self.data, font=(fonte, small_text_size), fg = 'white', bg = 'black')
		self.dataLB.pack(side = TOP, anchor = W)

		# A propria classe Relogio chama o metodo Tick() quando eh inicializada
		self.tick()

	def tick(self):

		# Receba as informacoes da hora, dia e data
		self.hora2 = time.strftime('%H:%M')
		self.dia_semana2 = time.strftime('%A')
		self.data2 = time.strftime('%d %b, %Y')

		# Atualiza as variaveis caso houver alguma mudanca
		if self.hora != self.hora2:
			self.hora = self.hora2
		if self.dia_semana != self.dia_semana2:
			self.dia_semana = self.dia_semana2
		if self.data != self.data2:
			self.data = self.data2

		# Atualiza as Labels com o metodo config()
		self.horaLB.config(text = self.hora)
		self.dia_semanaLB.config(text = self.dia_semana)
		self.dataLB.config(text = self.data)

		# O metodo se chama apos 200ms para checar por mudancas
		self.horaLB.after(time_refresh_rate, self.tick)

class Clima(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg = 'black')

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
		self.prevLB = Label(self, text = self.previsao, font = (fonte, small_text_size), bg = 'black', fg = 'white')
		self.prevLB.pack(side = TOP, anchor = E)

		self.get_clima()

	# Metodo para buscar a latitude e longitude
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


# Classe de Mail e News foram unidas em uma unica classe FeedReader
class Feed_Reader(Frame):
	def __init__(self, root, title, url):
		Frame.__init__(self, root, bg = 'black')
		self.url = url

		titleLB = Label(self, 
						text = title, 
						font = (fonte, large_text_size), 
						bg = 'black', 
						fg = 'white'
						)
		titleLB.pack(side = TOP, anchor = W, fill = BOTH)

		self.entrieFR = Frame(self, bg = 'black')
		self.entrieFR.pack(side = TOP, anchor = W)

		self.get_entries(self.url)

	def get_entries(self, url):
		self.feed = feedparser.parse(url)

		for children in self.entrieFR.winfo_children():
			children.destroy()

		for entrie in self.feed.entries[0:3]:
			self.post = Titulo(self.entrieFR, entrie['title'])

		self.entrieFR.after(refresh_rate, self.get_entries)


class Titulo(Frame):
	def __init__(self, root, title):
		Frame.__init__(self, bg = 'black')

		self.title = title.rsplit('-', 1) # Retira a fonte da noticia (Quem precisa de fonte, seculo XXI)
		self.titleLB = Label(root, text = title, font = (fonte, medium_text_size), bg = 'black', fg = 'white')
		self.titleLB.pack(side = TOP, anchor = W)

class Screen_Builder():
	def __init__(self):
		self.root = Tk()	# Tela Principal

		self.screen_full = False
		self.root.bind('<Return>', self.toggle_fullscreen)

		# Variaveis para o feed

		#news_url = 'http://news.google.com/news?ned=pt-BR_br&outpu t=rss'
		self.news_url = 'http://feeds.reuters.com/reuters/topNews'

		#mail_usr = 'nicolau.test'
		#mail_psw = 'anavitoria'
		#mail_url = 'https://%s:%s@mail.google.com/mail/feed/atom' % (mail_usr, mail_psw)

		# Posicionamento dos frames

		self.topFrame = Frame(self.root, bg = 'black')
		self.topFrame.pack(side = TOP, anchor = W, fill = BOTH, expand = YES)

		self.top_leftFrame = Frame(self.topFrame, bg = 'black')
		self.top_leftFrame.pack(side = LEFT, anchor = N)

		#sub_top_leftFrame = Frame(topFrame, bg = 'black')
		#sub_top_leftFrame.pack(side = LEFT, anchor = N)

		self.top_rightFrame = Frame(self.topFrame, bg = 'black')
		self.top_rightFrame.pack(side = RIGHT, anchor = N)

		self.bottomFrame = Frame(self.root, bg = 'black')
		self.bottomFrame.pack(side = BOTTOM, anchor = W, fill = BOTH, expand = YES)

		# Declaracao das Classes
		relogio = Relogio(self.top_leftFrame)
		relogio.pack(side = TOP, anchor = W)

		#mail = Feed_Reader(sub_top_leftFrame, title = "Mail", url = mail_url)
		#mail.pack(side = TOP, anchor = W)

		clima = Clima(self.top_rightFrame)
		clima.pack(side = TOP, anchor = E)

		news = Feed_Reader(self.bottomFrame, title = "News", url = self.news_url)
		news.pack(side = BOTTOM, anchor = W, fill = BOTH)

	def toggle_fullscreen(self, event = None):
		self.screen_full = not self.screen_full
		self.root.attributes("-fullscreen", self.screen_full)

tk = Screen_Builder()
tk.root.mainloop()
