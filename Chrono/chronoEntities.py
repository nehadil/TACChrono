class ChronoEntity:
	def __init__(self, id, label, span, text):
		self.id = id
		self.label = label
		self.span = span
		self.text = text

	def print_xml(self):
		return "\t<Mention id=\"{}\" label=\"{}\" span=\"{} {}\" str=\"{}\"/>".format(self.id, self.label,self.span[0], self.span[1],self.text )