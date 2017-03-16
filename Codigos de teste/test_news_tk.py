# -----------------------------------------	#
# Teste Tkinter, Feed and News v1.0			#
#											#
# Nicolau Tahan - 15/03/17					#
# -----------------------------------------	#

import feedparser
from Tkinter import *

refresh_rate = 300000 # Refresh nas noticias a cada 5 min
text_size = 25
fonte = 'Helvetica'

class Noticias(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg='black')

		# So um titulozinho pra parte das noticias
		# PQ Q ESSA PORRA NAO CONSEGUE FICAR NA DIREITA????
		self.newsLB = Label(self, text = 'Noticias', font=(fonte, text_size), bg = 'black', fg = 'white')
		self.newsLB.pack(side = TOP, anchor = E)

		# Precisamos declarar essa Frame para os titulos das noticias
		self.titleFR = Frame(self, bg= 'black')	
		self.titleFR.pack(side = TOP, anchor = W)

		self.get_noticias()

	def get_noticias(self):

		# Noticias originam do RSS feed do Google News, valeu migos
		self.news_url = 'http://news.google.com/news?ned=pt-BR_br&output=rss'
		self.feed = feedparser.parse(self.news_url)
		
		# Usamos apenas as 3 ultimas noticias
		for noticias in self.feed.entries[0:3]:
			self.post = Titulo(self.titleFR, noticias.title)

		self.newsLB.after(refresh_rate, self.get_noticias)


# Mais facil criar uma classe para cada noticia pois assim as 
# mesmas ja vem com um frame unico, diminui erros
class Titulo(Frame):
	def __init__(self, root, noticia = ''):
		Frame.__init__(self, bg= 'black')

		self.titulo = noticia.rsplit('-', 1)
		self.noticiaLB = Label(root, text = self.titulo[0], font=(fonte, text_size), bg = 'black', fg = 'white')
		self.noticiaLB.pack(side = TOP, anchor = W)


# ------------------------------------ BLOCO DE TESTE ------------------------------------------ #
root = Tk()

test_frame = Frame(root, bg = 'black')
test_frame.pack(side = LEFT, anchor = S, fill = BOTH, expand = YES)

noti = Noticias(test_frame)
noti.pack()

root.mainloop()