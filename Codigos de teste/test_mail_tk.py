from Tkinter import *
import feedparser

text_size = 25
fonte = 'Helvetica'
refresh_rate = 300000

class Mail(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg = 'black')
		
		self.username = 'nicolau.test'
		self.psw = 'anavitoria'

		mailLB = Label(self, text = 'Mail', font = (fonte, text_size), bg = 'black', fg = 'white')
		mailLB.pack(side = TOP, anchor = W)

		self.feedFR = Frame(self, bg = 'black')
		self.feedFR.pack(side = TOP, anchor = W)

		self.get_mail()

	def get_mail(self):
		mail_url = 'https://%s:%s@mail.google.com/mail/feed/atom' % (self.username, self.psw)
		mail_feed = feedparser.parse(mail_url)

		for feed_entrie in mail_feed.entries[0:3]:
			self.post = Titulo(self.feedFR, feed_entrie['title'])

		self.feedFR.after(refresh_rate, self.get_mail)


class Titulo(Frame):
	def __init__(self, root, noticia = ''):
		Frame.__init__(self, bg= 'black')

		self.titulo = noticia.rsplit('-', 1)
		self.noticiaLB = Label(root, text = self.titulo[0], font=(fonte, text_size), bg = 'black', fg = 'white')
		self.noticiaLB.pack(side = TOP, anchor = W)


root = Tk()

mailFR = Frame(root, bg = 'black')
mailFR.pack(side = TOP, anchor = W)

mail = Mail(mailFR)
mail.pack(side = TOP, anchor = W)

root.mainloop()