# -----------------------------------------	#
# Teste Tkinter e Time v1.0					#
#											#
# Nicolau Tahan - 15/03/17					#
# -----------------------------------------	#

from Tkinter import *
import time

fonte = 'Helvetica'
large_text_size = 35

class Relogio(Frame):
	def __init__(self, root):
		Frame.__init__(self, root, bg='black')

		# Defina as variaveis internas
		self.hora = ''
		self.dia_semana = ''
		self.data = ''

		# Defina as Labels do tempo, dia da semana e data
		self.horaLB = Label(root, text= self.hora, font=(fonte, large_text_size), fg = 'white', bg = 'black')
		self.horaLB.pack(side = TOP, anchor = W)

		self.dia_semanaLB = Label(root, text= self.dia_semana, font=(fonte, large_text_size), fg = 'white', bg = 'black')
		self.dia_semanaLB.pack(side = TOP, anchor = W)

		self.dataLB = Label(root, text= self.data, font=(fonte, large_text_size), fg = 'white', bg = 'black')
		self.dataLB.pack(side = TOP, anchor = W)

		# A propria classe Relogio chama o metodo Tick() quando eh inicializada
		self.tick()

	def tick(self):

		# Receba as informacoes da hora, dia e data
		self.hora2 = time.strftime('%H: %M')
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
		self.horaLB.after(200, self.tick)



root = Tk()

test_frame = Frame(root, bg = 'black')
test_frame.pack(side = TOP, fill = BOTH, expand = YES)

rel = Relogio(test_frame)
rel.pack()

root.mainloop()