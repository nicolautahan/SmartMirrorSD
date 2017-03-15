import feedparser
from Tkinter import *

refresh_rate = 300000
text_size = 25
fonte = 'Helvetica'

class Noticias(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg='black')

		self.newsLB = Label(self, text = 'Noticias', font=(fonte, text_size), bg = 'black', fg = 'white')
		self.newsLB.pack(side = TOP, anchor = E)

		self.titleFR = Frame(self, bg= 'black')
		self.titleFR.pack(side = TOP, anchor = W)

		self.get_noticias()

	def get_noticias(self):
		self.news_url = 'http://news.google.com/news?ned=pt-BR_br&output=rss'
		self.feed = feedparser.parse(self.news_url)
		
		for noticias in self.feed.entries[0:3]:
			self.post = Titulo(self.titleFR, noticias.title)

		self.newsLB.after(refresh_rate, self.get_noticias)


class Titulo(Frame):
	def __init__(self, root, noticia = ''):
		Frame.__init__(self, bg= 'black')

		self.titulo = noticia
		self.noticiaLB = Label(root, text = self.titulo, font=(fonte, text_size), bg = 'black', fg = 'white')
		self.noticiaLB.pack(side = TOP, anchor = W)

			
root = Tk()

test_frame = Frame(root, bg = 'black')
test_frame.pack(side = LEFT, anchor = S, fill = BOTH, expand = YES)

noti = Noticias(test_frame)
noti.pack()

root.mainloop()