# analyze fairyscript code
from . import fey


class AnalysisCompiler(object):

	def __init__(self):
		self._warnings = {}
		self._chars = {}
		self._sections = {}
		self._cam_directives = {'snap': 0, 'pan': 0, 'zoom': 0}
		self._scenes = {}
		self._transitions = {}
		self._resources = {
			'fmv': {},
			'gfx': {},
			'sfx': {},
			'bgm': {}
		}
		self._ids = {
			'fmv': {},
			'gfx': {},
			'sfx': {},
			'bgm': {}
		}
		self._names = {
			'fmv': {},
			'gfx': {},
			'sfx': {},
			'bgm': {}
		}
		self._compiled = ""
		self._to_add = ""
		self._indent_lev = 0

		self._order = 'name'

	def set_options(self, options):
		self._order = options.order

	def set_characters(self, chars):
		for k in chars:
			self._create_char_record(k)
			char_data = chars[k]
			for char_key in char_data:
				self._chars[k][char_key] = char_data[char_key]

	def compile_script(self, script):
		self._to_add = ""
		self._indent_lev = 0
		self._compiled = ""

		if script is not None:
			for statement in script:
				self.compile_statement(statement)

		self.add_line("Script Analysis (v1.0)")
		self.add_line("======================")
		self.add_line()
		self._build_characters_output()
		self._build_sections_output()
		self._build_scenes_output()
		self._build_transitions_output()
		self._build_ids_output()
		self._build_names_output()
		self._build_fmv_output()
		self._build_gfx_output()
		self._build_sfx_output()
		self._build_bgm_output()
		self._build_cameras_output()

		return self._compiled

	def add_warning(self, key, text):
		if key not in self._warnings:
			self._warnings[key] = []
		self._warnings[key].append(text)

	def get_warnings(self):
		warns = []
		for k in self._warnings:
			w_list = self._warnings[k]
			for w in w_list:
				warns.append(w)
		return warns

	def clear_warnings(self):
		self._warnings = {}

	def add(self, text):
		self._to_add += text

	def add_line(self, text=""):
		self.add(text)
		indent = ('\t' * self._indent_lev)
		self._compiled += indent + self._to_add + '\n'
		self._to_add = ""

	def _build_characters_output(self):
		num_chars = len(self._chars)
		self.add_line(fey.pluralize(num_chars, "Character"))
		self._inc_indent()
		mutable_chars = dict(self._chars)
		if num_chars > 0:
			# get internal dialog first
			if None in mutable_chars:
				lines = mutable_chars[None]['lines']
				self.add_line("Internal Dialog: " + fey.pluralize(lines, "line"))
				self.add_line()

				# remove the internal dialog data so we don't interfere with sorting
				del mutable_chars[None]

			# then get all but internal dialog
			char_names = self._sort_map_keys(mutable_chars, lambda x: x['lines'])
			for name in char_names:
				char_data = mutable_chars[name]
				lines = char_data['lines']
				state_keys = self._sort_ref_map_keys(char_data['states'])
				self.add_line(name + " (" + fey.pluralize(lines, "line") + "):")
				self._inc_indent()
				for state in state_keys:
					ref_count = char_data['states'][state]
					self.add_line(name + " " + state + ": " + fey.pluralize(ref_count, "reference"))
				self._dec_indent()
				self.add_line()
		else:
			self.add_line("(none)")
			self.add_line()
		self._dec_indent()

	def _build_sections_output(self):
		num = len(self._sections)
		self.add_line(fey.pluralize(num, "Section"))
		self._inc_indent()
		if num > 0:
			section_keys = self._sort_map_keys(self._sections)
			for sec in section_keys:
				ref_count = self._sections[sec]['refs']
				def_count = self._sections[sec]['defines']
				self.add_line(sec + ":")
				self._inc_indent()
				self.add_line(fey.pluralize(def_count, "definition"))
				self.add_line(fey.pluralize(ref_count, "reference"))
				self._dec_indent()
				self.add_line()
		else:
			self.add_line("(none)")
			self.add_line()
		self._dec_indent()

	def _build_scenes_output(self):
		num = len(self._scenes)
		self.add_line(fey.pluralize(num, "Scene"))
		self._inc_indent()
		if num > 0:
			scene_keys = self._sort_ref_map_keys(self._scenes)
			for s in scene_keys:
				ref_count = self._scenes[s]
				self.add_line(s + ": " + fey.pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_transitions_output(self):
		num = len(self._transitions)
		self.add_line(fey.pluralize(num, "Transition"))
		self._inc_indent()
		if num > 0:
			transition_keys = self._sort_ref_map_keys(self._transitions)
			for t in transition_keys:
				ref_count = self._transitions[t]
				self.add_line(t + ": " + fey.pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_ids_output(self):
		fmvs = [(name, 'fmv') for name in self._ids['fmv'].keys()]
		gfxs = [(name, 'gfx') for name in self._ids['gfx'].keys()]
		sfxs = [(name, 'sfx') for name in self._ids['sfx'].keys()]
		bgms = [(name, 'bgm') for name in self._ids['bgm'].keys()]
		full_list = fmvs + gfxs + sfxs + bgms
		full_list = self._sort_list(full_list, name_key=lambda x: x, usage_key=lambda x: self._ids[x[1]][x[0]])

		num = len(full_list)
		self.add_line(fey.pluralize(num, "ID"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._ids[t][n]
				self.add_line(n + " (" + t.upper() + "): " + fey.pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_names_output(self):
		fmvs = [(name, 'fmv') for name in self._names['fmv'].keys()]
		gfxs = [(name, 'gfx') for name in self._names['gfx'].keys()]
		sfxs = [(name, 'sfx') for name in self._names['sfx'].keys()]
		bgms = [(name, 'bgm') for name in self._names['bgm'].keys()]
		full_list = fmvs + gfxs + sfxs + bgms
		full_list = self._sort_list(full_list, name_key=lambda x: x, usage_key=lambda x: self._names[x[1]][x[0]])

		num = len(full_list)
		self.add_line(fey.pluralize(num, "Name"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._names[t][n]
				self.add_line(fey.quote(n) + " (" + t.upper() + "): " + fey.pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_resource_output(self, type_key, title):
		res_map = self._resources[type_key]
		full_list = self._sort_ref_map_keys(res_map)

		num = len(full_list)
		self.add_line(fey.pluralize(num, title))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = res_map[(n, t)]
				if t == 'name':
					n = fey.quote(n)
				self.add_line(n + ": " + fey.pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_fmv_output(self):
		self._build_resource_output("fmv", "FMV")

	def _build_gfx_output(self):
		self._build_resource_output("gfx", "GFX")

	def _build_sfx_output(self):
		self._build_resource_output("sfx", "SFX")

	def _build_bgm_output(self):
		self._build_resource_output("bgm", "Music Track")

	def _build_cameras_output(self):
		snap = self._cam_directives['snap']
		pan = self._cam_directives['pan']
		zoom = self._cam_directives['zoom']
		total = snap + pan + zoom

		self.add_line(fey.pluralize(total, "Camera Directive"))
		self._inc_indent()
		self.add_line("snap: " + fey.pluralize(snap, "reference"))
		self.add_line("pan: " + fey.pluralize(pan, "reference"))
		self.add_line("zoom: " + fey.pluralize(zoom, "reference"))
		self._dec_indent()
		self.add_line()

	def compile_statement(self, statement):
		if statement['type'] == 'line':
			self._compile_line(statement)
		elif statement['type'] == 'comment':
			pass
		else:
			instruction = statement['instruction']
			func = getattr(AnalysisCompiler, '_compile_' + instruction)
			func(self, statement)

	def _inc_indent(self):
		self._indent_lev += 1

	def _dec_indent(self):
		self._indent_lev -= 1
		if self._indent_lev < 0:
			self._indent_lev = 0

	def _reset_indent(self):
		self._indent_lev = 0

	def _inc_char_line_count(self, char_name):
		self._create_char_record(char_name)
		self._chars[char_name]['lines'] += 1

	def _inc_char_state_count(self, char_name, state):
		self._create_char_record(char_name)
		if state not in self._chars[char_name]['states']:
			self._chars[char_name]['states'][state] = 0
		self._chars[char_name]['states'][state] += 1

	def _create_char_record(self, char_name):
		if char_name not in self._chars:
			self._chars[char_name] = {'states': {}, 'lines': 0}

	def _compile_line(self, line):
		# TODO: differentiate between IDs and Names for characters
		if line['speaker'] is None:
			char_name = None
		else:
			char_name = line['speaker'][1]
		self._inc_char_line_count(char_name)

	# noinspection PyPep8Naming
	def _compile_SCENE(self, scene):
		name = scene['name'][1]
		if name not in self._scenes:
			self._scenes[name] = 0
		self._scenes[name] += 1
		if scene['transition'] is not None:
			trans = scene['transition'][1]
			if trans not in self._transitions:
				self._transitions[trans] = 0
			self._transitions[trans] += 1

	# noinspection PyPep8Naming
	def _compile_ENTER(self, enter):
		char_name = enter['target'][1]
		states = [s[1] for s in enter['states']]
		# TODO: work with EXIT and create an 'onstage' count for a character
		# TODO: work with SCENE and create a 'scene' count for a character
		for s in states:
			self._inc_char_state_count(char_name, s)

	# noinspection PyPep8Naming
	def _compile_ACTION(self, action):
		char_name = action['target'][1]
		states = [s[1] for s in action['states']]
		for s in states:
			self._inc_char_state_count(char_name, s)

	# noinspection PyPep8Naming
	def _compile_EXIT(self, xit):
		pass

	# noinspection PyPep8Naming
	def _compile_MUSIC(self, music):
		self._inc_resource_count('bgm', music['target'])

	# noinspection PyPep8Naming
	def _compile_GFX(self, gfx):
		self._inc_resource_count('gfx', gfx['target'])

	# noinspection PyPep8Naming
	def _compile_SFX(self, sfx):
		self._inc_resource_count('sfx', sfx['target'])

	# noinspection PyPep8Naming
	def _compile_FMV(self, fmv):
		self._inc_resource_count('fmv', fmv['target'])

	def _inc_resource_count(self, resource_kind, resource):
		resource_name = resource[1]

		if fey.typed_check(resource, 'string'):
			ref_type = 'name'
			ref_dict = self._names
		elif fey.typed_check(resource, 'id'):
			ref_type = 'id'
			ref_dict = self._ids
		else:
			return

		if resource_name not in ref_dict[resource_kind]:
			ref_dict[resource_kind][resource_name] = 0
		if (resource_name, ref_type) not in self._resources[resource_kind]:
			self._resources[resource_kind][(resource_name, ref_type)] = 0

		ref_dict[resource_kind][resource_name] += 1
		self._resources[resource_kind][(resource_name, ref_type)] += 1

	# noinspection PyPep8Naming
	def _compile_CAMERA(self, camera):
		# TODO: include targets
		for a in camera['actions']:
			self._cam_directives[a['type'].lower()] += 1

	# noinspection PyPep8Naming
	def _compile_CHOICE(self, choice):
		if fey.typed_check(choice['label'], 'id'):
			label = choice['label'][1]
			if label not in self._sections:
				self._sections[label] = {'defines': 0, 'refs': 0}
			self._sections[label]['defines'] += 1

		for c in choice['choices']:
			dest = c['target'][1]
			if dest not in self._sections:
				self._sections[dest] = {'defines': 0, 'refs': 0}
			self._sections[dest]['refs'] += 1

	# noinspection PyPep8Naming
	def _compile_DESCRIPTION(self, desc):
		pass

	# noinspection PyPep8Naming
	def _compile_SECTION(self, section):
		dest = section['section'][1]
		if dest not in self._sections:
			self._sections[dest] = {'defines': 0, 'refs': 0}
		self._sections[dest]['defines'] += 1

	# noinspection PyPep8Naming
	def _compile_FLAGSET(self, flagset):
		pass

	# noinspection PyPep8Naming
	def _compile_VARSET(self, varset, noline=False):
		pass

	# noinspection PyPep8Naming
	def _compile_DIALOG(self, dialog):
		pass

	# noinspection PyPep8Naming
	def _compile_GOTO(self, goto):
		dest = goto['destination'][1]
		if dest not in self._sections:
			self._sections[dest] = {'defines': 0, 'refs': 0}
		self._sections[dest]['refs'] += 1

	# noinspection PyPep8Naming
	def _compile_EXECUTE(self, execute):
		pass

	# noinspection PyPep8Naming
	def _compile_END(self, end):
		pass

	# noinspection PyPep8Naming
	def _compile_WHILE(self, while_stmt):
		pass

	# noinspection PyPep8Naming
	def _compile_IF(self, if_stmt):
		pass

	# noinspection PyPep8Naming
	def _compile_INCLUDE(self, include):
		pass

	# noinspection PyPep8Naming
	def _compile_CHARACTERS(self, characters):
		pass

	# noinspection PyPep8Naming
	def _compile_PYTHON(self, python):
		pass

	def _sort_list(self, items, name_key, usage_key):
		"""
		Use the preferred sorting algorithm to sort a list of data objects.
		:type items: list[Any]
		:param items: The list of items to sort.
		:type name_key: (Any) -> str
		:param name_key: The function to use to get the name of a data object.
		:type usage_key: (Any) -> int
		:param name_key: The function to use to get the number of usages of a data object.
		:rtype: list[str]
		:return: The list items, sorted using the preferred algorithm (set by the _order var).
		"""
		if self._order == "name":
			sorted_items = sorted(items, key=name_key)
		elif self._order == "usage":
			sorted_items = sorted(items, key=name_key)
			sorted_items = sorted(sorted_items, key=usage_key, reverse=True)
		else:
			raise ValueError("Bad sorting algorithm type '" + str(self._order) + "'")
		return sorted_items

	def _sort_ref_map_keys(self, ref_map):
		"""
		Use the preferred sorting algorithm to sort the keys of a dict that directly maps names to references.
		:type ref_map: dict[str, int]
		:param ref_map: The map whose keys to sort.
		:rtype: list[str]
		:return: The list of the dict's keys, sorted using the preferred algorithm (set by the _order var).
		"""
		return self._sort_map_keys(ref_map, usage_key=lambda x: x)

	def _sort_map_keys(self, obj_map, usage_key=None):
		"""
		Use the preferred sorting algorithm to sort the keys of a dict that maps names to dicts that contain a key that
		gives the number of usages.
		:type obj_map: dict[str, Any]
		:param obj_map: The map whose keys to sort.
		:type usage_key: (Any) -> int
		:param usage_key: Function to go from a mapped object to a reference count. By default, this will be to access
		the 'refs' index of the mapped object.
		:rtype: list[str]
		:return: The list of the dict's keys, sorted using the preferred algorithm (set by the _order var).
		"""
		dict_keys = obj_map.keys()
		if self._order == "name":
			dict_keys = sorted(dict_keys)
		elif self._order == "usage":
			if usage_key is None:
				def usage_key(x):
					return x['refs']
			dict_keys = sorted(dict_keys)
			dict_keys = sorted(dict_keys, key=lambda k: usage_key(obj_map[k]), reverse=True)
		else:
			raise ValueError("Bad sorting algorithm type '" + str(self._order) + "'")
		return dict_keys
