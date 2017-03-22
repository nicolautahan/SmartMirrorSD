from Tkinter import *
import feedparser

fonte = 'CODE Light'
text_size = 30
refresh_rate = 60000

class Feed_Reader(Frame):
	def __init__(self, root, title, url):
		Frame.__init__(self, bg = 'black')
		self.url = url

		titleLB = Label(self, 
						text = title, 
						font = (fonte, text_size), 
						bg = 'black', 
						fg = 'white'
						)
		titleLB.pack(side = TOP, anchor = W, expand = YES, fill = BOTH)

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

		self.title = title.rsplit('-', 1)
		self.titleLB = Label(root, text = title, font = (fonte, text_size), bg = 'black', fg = 'white')
		self.titleLB.pack(side = TOP, anchor = W)

news_url = 'http://news.google.com/news?ned=pt-BR_br&output=rss'

mail_usr = 'nicolau.test'
mail_psw = 'anavitoria'
mail_url = 'https://%s:%s@mail.google.com/mail/feed/atom' % (mail_usr, mail_psw)

root = Tk()

topFrame = Frame(root, bg = 'black')
topFrame.pack(side = TOP, anchor = W, fill = BOTH, expand = YES)

bottomFrame = Frame(root, bg = 'black')
bottomFrame.pack(side = TOP, anchor = W, fill = BOTH, expand = YES)

mail = Feed_Reader(topFrame, 'Mail', mail_url)
mail.pack(side = TOP, anchor = W)

news = Feed_Reader(bottomFrame, 'Noticias', news_url)
news.pack(side = TOP, anchor = W)

root.mainloop()