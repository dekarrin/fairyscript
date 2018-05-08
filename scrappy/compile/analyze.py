# analyze scrappy code
from . import scp


class AnalysisCompiler(object):

	def __init__(self):
		self._warnings = {}
		self._chars = {}
		self._labels_map = {}
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

	def set_options(self, options):
		pass

	def set_characters(self, chars):
		self._chars = chars

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
		self._build_cameras_output()
		self._build_scenes_output()
		self._build_transitions_output()
		self._build_ids_output()
		self._build_names_output()
		self._build_fmv_output()
		self._build_gfx_output()
		self._build_sfx_output()
		self._build_bgm_output()

		return self._compiled

	def _build_bgm_output(self):
		full_list = self._resources['bgm'].keys()
		full_list.sort()

		num = len(full_list)
		self.add_line(pluralize(num, "Music Track"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._resources['bgm'][(n, t)]
				if t == 'name':
					n = scp.quote(n)
				self.add_line(n + ": " + pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_sfx_output(self):
		full_list = self._resources['sfx'].keys()
		full_list.sort()

		num = len(full_list)
		self.add_line(pluralize(num, "SFX"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._resources['sfx'][(n, t)]
				if t == 'name':
					n = scp.quote(n)
				self.add_line(n + ": " + pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_gfx_output(self):
		full_list = self._resources['gfx'].keys()
		full_list.sort()

		num = len(full_list)
		self.add_line(pluralize(num, "GFX"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._resources['gfx'][(n, t)]
				if t == 'name':
					n = scp.quote(n)
				self.add_line(n + ": " + pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_fmv_output(self):
		full_list = self._resources['fmv'].keys()
		full_list.sort()

		num = len(full_list)
		self.add_line(pluralize(num, "FMV"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._resources['fmv'][(n, t)]
				if t == 'name':
					n = scp.quote(n)
				self.add_line(n + ": " + pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_names_output(self):
		fmvs = [(scp.quote(name), 'fmv') for name in self._names['fmv'].keys()]
		gfxs = [(scp.quote(name), 'gfx') for name in self._names['gfx'].keys()]
		sfxs = [(scp.quote(name), 'sfx') for name in self._names['sfx'].keys()]
		bgms = [(scp.quote(name), 'bgm') for name in self._names['bgm'].keys()]
		full_list = fmvs + gfxs + sfxs + bgms
		full_list.sort()

		num = len(full_list)
		self.add_line(pluralize(num, "Names"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._names[t][n]
				self.add_line(n + " (" + t.upper() + "): " + pluralize(ref_count, "reference"))
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
		full_list.sort()

		num = len(full_list)
		self.add_line(pluralize(num, "ID"))
		self._inc_indent()
		if num > 0:
			for n, t in full_list:
				ref_count = self._ids[t][n]
				self.add_line(n + " (" + t.upper() + "): " + pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_transitions_output(self):
		num = len(self._transitions)
		self.add_line(pluralize(num, "Transition"))
		self._inc_indent()
		if num > 0:
			for t in self._transitions:
				ref_count = self._transitions[t]
				self.add_line(t + ": " + pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_scenes_output(self):
		num = len(self._scenes)
		self.add_line(pluralize(num, "Scene"))
		self._inc_indent()
		if num > 0:
			for s in self._scenes:
				ref_count = self._scenes[s]
				self.add_line(s + ": " + pluralize(ref_count, "reference"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_cameras_output(self):
		snap = self._cam_directives['snap']
		pan = self._cam_directives['pan']
		zoom = self._cam_directives['zoom']
		total = snap + pan + zoom

		self.add_line(pluralize(total, "Camera Directive"))
		self._inc_indent()
		self.add_line("snap: " + pluralize(snap, "reference"))
		self.add_line("pan: " + pluralize(pan, "reference"))
		self.add_line("zoom: " + pluralize(zoom, "reference"))
		self._dec_indent()
		self.add_line()

	def _build_sections_output(self):
		num = len(self._labels_map)
		self.add_line(pluralize(num, "Section"))
		self._inc_indent()
		if num > 0:
			for sec in self._labels_map:
				ref_count = self._labels_map[sec]
				self.add_line(sec + ": " + pluralize(ref_count, "references"))
		else:
			self.add_line("(none)")
		self._dec_indent()
		self.add_line()

	def _build_characters_output(self):
		num_chars = len(self._chars)
		self.add_line(pluralize(num_chars, "Character"))
		self._inc_indent()
		if len(self._chars) > 0:
			for name in self._chars:
				char_data = self._chars[name]
				lines = char_data['lines']
				states = char_data['states']
				self.add_line(name + " (" + pluralize(lines, "line") + "):")
				self._inc_indent()
				for state in states:
					ref_count = states[state]
					self.add_line(name + " " + state + ": " + pluralize(ref_count, "references"))
				self._dec_indent()
				self.add_line()
		else:
			self.add_line("(none)")
			self.add_line()
		self._dec_indent()

	def compile_statement(self, statement):
		if statement['type'] == 'line':
			self._compile_line(statement)
		elif statement['type'] == 'comment':
			pass
		else:
			instruction = statement['instruction']
			func = getattr(AnalysisCompiler, '_compile_' + instruction)
			func(self, statement)

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

		if scp.typed_check(resource, 'string'):
			ref_type = 'name'
			ref_dict = self._names
		elif scp.typed_check(resource, 'id'):
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
		label = ""
		if scp.typed_check(choice['label'], 'id'):
			label = " " + choice['label'][1]
		if label not in self._labels_map:
			self._labels_map[label] = 0

		for c in choice['choices']:
			dest = c['target'][1]
			if dest not in self._labels_map:
				self._labels_map[dest] = 0
			self._labels_map[dest] += 1

	# noinspection PyPep8Naming
	def _compile_DESCRIPTION(self, desc):
		pass

	# noinspection PyPep8Naming
	def _compile_SECTION(self, section):
		dest = section['section'][1]
		if dest not in self._labels_map:
			self._labels_map[dest] = 0

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
		if dest not in self._labels_map:
			self._labels_map[dest] = 0
		self._labels_map[dest] += 1

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


def pluralize(num, word, append="s"):
	if num != 1:
		return str(num) + " " + word + append
	else:
		return str(num) + " " + word
