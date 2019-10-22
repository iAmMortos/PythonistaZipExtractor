import ui
import sharedlibs
sharedlibs.add_path_for('view_swap')
from view_swap import ViewSwap
sharedlibs.add_path_for('list_selector')
from list_selector import ListSelector

class ConfirmView (ui.View):
	
	def did_load(self):
		self.ls = None
		self.proceed = False
		self.yes_btn = self['yes_btn']
		self.yes_btn.action = self.yes_action
		self.no_btn = self['no_btn']
		self.no_btn.action = self.no_action
		self.zip = self['zip']
		self.zip.enabled = False
		self.sw = self['sw']
		
	def init(self, pathstr, file):
		vs = ViewSwap(self)
		paths = pathstr.split('|')
		self.ls = ListSelector(paths, placeholder='Select a path...')
		vs.swap('dummy_ls', self.ls)
		self.ls.value = None if len(paths) == 0 else paths[0]
		self.zip.text = file
	
	@staticmethod
	def load_view(pathstr, file):
		v = ui.load_view()
		v.init(pathstr, file)
		return v
		
	def yes_action(self, target):
		self.proceed = True
		self.path = self.ls.value
		self.clearfirst = self.sw.value
		self.close()
		
	def no_action(self, target):
		self.close()
