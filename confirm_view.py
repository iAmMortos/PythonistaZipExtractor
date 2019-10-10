import ui

class ConfirmView (ui.View):
	
	def did_load(self):
		self.proceed = False
		self.tf = self['tf']
		self.yes_btn = self['yes_btn']
		self.yes_btn.action = self.yes_action
		self.no_btn = self['no_btn']
		self.no_btn.action = self.no_action
		self.zip = self['zip']
		self.zip.enabled = False
		self.sw = self['sw']
		
	def init(self, path, file):
		self.tf.text = path
		self.zip.text = file
	
	@staticmethod
	def load_view(path, file):
		v = ui.load_view()
		v.init(path, file)
		return v
		
	def yes_action(self, target):
		self.proceed = True
		self.path = self.tf.text
		self.clearfirst = self.sw.value
		self.close()
		
	def no_action(self, target):
		self.close()
