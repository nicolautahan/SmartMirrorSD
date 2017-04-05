from Tkinter import *
import time
import feedparser
import requests
import json

clima_token = 'bb32dfc53f3c76134d49fef7e8c83801'
clima_lang = 'en'
clima_unit = 'si'

fonte = 'CODE Light'
large_text_size = 35
time_refresh_rate = 200
text_size = 20
small_text_size = 13
xlarge_text_size = 50
refresh_rate = 60000

class Relogio(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg='black')

		# Defina as variaveis internas
		self.hora = ''
		self.dia_semana = ''
		self.data = ''

		# Defina as Labels do tempo, dia da semana e data
		self.horaLB = Label(self, text= self.hora, font=(fonte, large_text_size), fg = 'white', bg = 'black')
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
		self.dia_semana2 = time.strftime('%A, idiota..')
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


class Noticias(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg='black')

		self.newsLB = Label(self, text = 'Noticias', font=(fonte, large_text_size), bg = 'black', fg = 'white')
		self.newsLB.pack(side = TOP, anchor = W, expand = YES, fill = BOTH)

		self.titleFR = Frame(self, bg= 'black')
		self.titleFR.pack(side = TOP, anchor = W, expand = YES, fill = BOTH)

		self.get_noticias()

	def get_noticias(self):
		self.news_url = 'http://news.google.com/news?ned=pt-BR_br&output=rss'
		self.feed = feedparser.parse(self.news_url)

		for widget in self.titleFR.winfo_children():
			widget.destroy()
		
		for noticias in self.feed.entries[0:3]:
			self.post = Titulo(self.titleFR, noticias.title)

		self.newsLB.after(refresh_rate, self.get_noticias)


class Titulo(Frame):
	def __init__(self, root, noticia = ''):
		Frame.__init__(self, bg= 'black')

		self.titulo = noticia.rsplit('-', 1)
		self.noticiaLB = Label(root, text = self.titulo[0], font=(fonte, text_size), bg = 'black', fg = 'white')
		self.noticiaLB.pack(side = TOP, anchor = W)


class Clima(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg='black')

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


class Mail(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg = 'black')
		
		self.username = 'nicolau.test'
		self.psw = 'anavitoria'

		mailLB = Label(self, text = 'Mail', font = (fonte, large_text_size), bg = 'black', fg = 'white')
		mailLB.pack(side = TOP, anchor = E, expand = YES, fill = BOTH)

		self.feedFR = Frame(self, bg = 'black')
		self.feedFR.pack(side = TOP, anchor = W, expand = YES, fill = BOTH)

		self.get_mail()

	def get_mail(self):
		mail_url = 'https://%s:%s@mail.google.com/mail/feed/atom' % (self.username, self.psw)
		mail_feed = feedparser.parse(mail_url)

		for widget in self.feedFR.winfo_children():
			widget.destroy()

		for feed_entrie in mail_feed.entries[0:3]:
			self.post = Titulo(self.feedFR, feed_entrie['title'])

		self.feedFR.after(refresh_rate, self.get_mail)




root = Tk()

topFrame = Frame(root, bg = 'black')
topFrame.pack(side = TOP, anchor = W, expand = YES, fill = BOTH)

bottomFrame = Frame(root, bg = 'black')
bottomFrame.pack(side = BOTTOM, anchor = W, expand = YES, fill = BOTH)

midFrame = Frame(topFrame, bg = 'black')
midFrame.pack(side = LEFT, anchor = N, expand = YES, fill = BOTH)

clima = Clima(topFrame)
clima.pack(side = RIGHT, anchor = N)

rel = Relogio(midFrame)
rel.pack(side = TOP, anchor = W)

news = Noticias(bottomFrame)
news.pack(side = BOTTOM, anchor = W)

mail = Mail(midFrame)
mail.pack(side = TOP, anchor = W)



root.mainloop()