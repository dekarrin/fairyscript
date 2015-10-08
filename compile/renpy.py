import scp

class RenpyCompiler(object):
	def __init__(self):
		self.default_destination = 'center'
		self.default_origin = 'center'
		self.default_duration = 0.5
		self.quickly_rel = 0.25
		self.slowly_rel = 2
		self.tab_spaces = 4
		self.background_ent = 'bg'
		self._indent_lev = 0
		self._compiled = None
		self._to_add = ""
		self._has_enter_trans = False
		self._has_exit_trans = False
		self._scene_trans = None
		self._warnings = {}
		self._gfx_targets = {}
		self._cur_scene_gfx = []
		self._cur_img_gfx = []
		self._use_camera_system = False
		self._cam_zoom = 'CAM_ZOOM_NORMAL'
		self._cam_pan = 'CAM_PAN_CENTER'
		
	def add_gfx_target(self, effect, target):
		if target.upper() != 'SCENE' and target.upper() != 'IMAGE' and target.upper() != 'DISPLAYABLE':
			self.add_warning('bad_gfx_binding', "'%s' is an invalid binding for GFX '%s'; must be one of 'scene', 'image', or 'displayable'" % (target, effect))
		self._gfx_targets[effect] = target.upper()
		
	def clear_gfx_targets(self):
		self._gfx_targets = {}
		
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
	
	def compile_script(self, script):
		self._compiled = ""
		self.last_line = False
		
		if script is not None:
			for statement in script:
				self.compile_statement(statement)
		return self._compiled
		
	def compile_statement(self, statement):
		if statement['type'] == 'line':
			if self._has_enter_trans or self._has_exit_trans:
				self._finish_transition()
			self._compile_line(statement)
			self.last_line = True
		elif statement['type'] == 'comment':
			pass
		else:
			if self.last_line:
				self.add_line()
				self.last_line = False
			instruction = statement['instruction']
			func = getattr(RenpyCompiler, '_compile_' + instruction)
			if (self._has_enter_trans and instruction is not 'ENTER') or (self._has_exit_trans and instruction is not 'EXIT'):
				self._finish_transition()
			func(self, statement)
		
	def add(self, text):
		self._to_add += text
		
	def add_line(self, text=""):
		self.add(text)
		indent = (' ' * self.tab_spaces * self._indent_lev)
		self._compiled += indent + self._to_add + '\n'
		self._to_add = ""
		
	def _compile_line(self, line):
		text = scp.quote(line['text'][1])
		if line['speaker'] is None:
			self.add_line(text)
		else:
			if line['speaker'][0] is 'id':
				self.add_line(line['speaker'][1] + ' ' + text)
			else:
				self.add_line(scp.quote(line['speaker'][1]) + ' ' + text)
				
	def _compile_SCENE(self, scene):
		self.add_line("scene " + self.background_ent + " " + scene['name'][1])
		if scene['transition'] is not None:
			self._has_enter_trans = True
			self._scene_trans = scene['transition'][1]
		else:
			self.add_line()
	
	def _compile_ENTER(self, enter):
		if self._has_enter_trans and enter['transition'] is not None and not scp.typed_check(enter['transition'], 'rel', 'WITH PREVIOUS'):
			self._finish_transition()
		self.add_line(build_show(enter['target'][1], enter['states']))
		geom = enter['motion']
		if geom is not None:
			orig = None
			dest = None
			if geom['origin'] is None and geom['duration'] is not None:
				orig = self.default_origin
			elif geom['origin'] is not None:
				orig = geom['origin'][1]
			if geom['destination'] is None and orig is not None:
				dest = self.default_destination
			elif geom['destination'] is not None:
				dest = geom['destination'][1]
			if orig is None:
				self.add_line('at ' + dest)
			else:
				self.add_line('at ' + orig)
		if enter['transition'] is not None and not scp.typed_check(enter['transition'], 'rel', 'WITH PREVIOUS'):
			self._has_enter_trans = True
			self._scene_trans = enter['transition'][1]
		if geom is not None and orig is not None:
			time = scp.get_duration(geom['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
			self.add_line(build_show(enter['target'][1], enter['states']))
			self.add_line('at ' + dest)
			self.add_line('with MoveTransition(' + str(time) + ')')
		self.add_line()
			
	def _compile_ACTION(self, action):
		self.add_line(build_show(action['target'][1], action['states']))
		if action['destination'] is not None:
			time = scp.get_duration(action['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
			self.add_line('at ' + action['destination'][1])
			self.add_line('with MoveTransition(' + str(time) + ')')
		self.add_line()
	
	def _compile_EXIT(self, exit):
		if self._has_exit_trans and exit['transition'] is not None and not scp.typed_check(exit['transition'], 'rel', 'WITH PREVIOUS'):
			self._finish_transition()
		self.add_line('show ' + exit['target'][1])
		geom = exit['motion']
		if geom is not None:
			orig = None
			dest = None
			if geom['origin'] is None and geom['duration'] is not None:
				orig = self.default_origin
			elif geom['origin'] is not None:
				orig = geom['origin'][1]
			if geom['destination'] is None and orig is not None:
				dest = self.default_destination
			elif geom['destination'] is not None:
				dest = geom['destination'][1]
			if orig is None:
				self.add_line('at ' + dest)
			else:
				self.add_line('at ' + orig)
		if exit['transition'] is not None and not scp.typed_check(exit['transition'], 'rel', 'WITH PREVIOUS'):
			self._has_exit_trans = True
			self._scene_trans = exit['transition'][1]
		if geom is not None and orig is not None:
			time = scp.get_duration(geom['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
			self.add_line('show ' + exit['target'][1])
			self.add_line('at ' + orig)
			self.add_line('with MoveTransition(' + str(time) + ')')
		self.add_line('hide ' + exit['target'][1])
		self.add_line()
		
	def _compile_MUSIC(self, music):
		if music['action'] == 'start':
			self.add('play music ')
			if scp.typed_check(music['target'], 'id'):
				self.add(music['target'][1])
			elif scp.typed_check(music['target'], 'string'):
				self.add(scp.quote(music['target'][1]))
			if music['fadeout'] is not None:
				time = scp.get_duration(music['fadeout'], self.quickly_rel, self.slowly_rel, self.default_duration)
				self.add(' fadeout ' + str(time))
		elif music['action'] == 'stop':
			explicit_all = False
			if scp.typed_check(music['target'], 'rel', 'ALL'):
				explicit_all = True
			self.add('stop music')
			if not explicit_all:
				self._warnings['targeted_music_stop'] = ["Ren'py does not support targeted music stop; any such directives will be compiled as if they were STOP ALL"]
			if music['duration'] is not None:
				time = scp.get_duration(music['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
				self.add(' fadeout ' + str(time))
		self.add_line()
		self.add_line()
		
	def _compile_GFX(self, gfx):
		if scp.typed_check(gfx['target'], 'id'):
			eff = gfx['target'][1]
			if eff not in self._gfx_targets:
				self.add_warning('no_gfx_binding', "GFX '%s' does not have any binding defined; assuming 'scene'" % eff)
				self.add_gfx_target(eff, 'scene')
			binding_type = self._gfx_targets[eff]
		if gfx['action'] == 'start':
			if scp.typed_check(gfx['loop'], 'boolean', True):
				if binding_type != 'DISPLAYABLE':
					eff += '_loop'
				else:
					self.add_warning('loop_displayable', "The GFX '%s' cannot be looped, because it is bound to a displayable" % eff)
			if binding_type == 'SCENE':
				self.add_line('show layer master')
				self._cur_scene_gfx.append(eff)
				prefix = self._get_current_scene_transforms()
				self.add_line('at ' + prefix)
			elif binding_type == 'IMAGE':
				img = eff + '_img'
				self.add_line('show ' + img)
				prefix = ""
				self._cur_img_gfx.append(eff)
				self.add_line('at ' + eff)
			elif binding_type == 'DISPLAYABLE':
				self.add_line('show ' + eff)
		elif gfx['action'] == 'stop':
			dissolve = None
			if gfx['duration'] is not None:
				time = scp.get_duration(gfx['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
				dissolve = "with Dissolve(" + str(time) + ")"
			if scp.typed_check(gfx['target'], 'rel', 'ALL'):
				self.add_line('show layer master')
				if self._use_camera_system:
					self.add_line('at ' + self._get_current_camera())
				self._cur_scene_gfx = []
				for fx in self._cur_img_gfx:
					self.add_line('hide ' + fx)
				self._cur_img_gfx = []
			else:
				if binding_type == 'SCENE':
					try:
						self._cur_scene_gfx.remove(eff)
						self._cur_scene_gfx.remove(eff + '_loop')
					except:
						pass
					self.add_line("show layer master")
					prefix = self._get_current_scene_transforms()
					if len(prefix) > 0:
						self.add_line('at ' + prefix)
				elif binding_type == 'IMAGE':
					if eff + '_loop' in self._cur_img_gfx:
						self._cur_img_gfx.remove(eff + '_loop')
						self.add_line('hide ' + eff + '_loop' + '_img')
					if eff in self._cur_img_gfx:
						self._cur_img_gfx.remove(eff)
						self.add_line('hide ' + eff + '_img')
				elif binding_type == 'DISPLAYABLE':
					self.add_line('hide ' + eff)
			if dissolve is not None:
				self.add_line(dissolve)
		self.add_line()
		
	def _compile_SFX(self, sfx):
		if sfx['action'] == 'start':
			self.add('play sound ')
			if scp.typed_check(sfx['target'], 'string'):
				self.add(scp.quote(sfx['target'][1]))
			else:
				self.add(sfx['target'][1])
			if scp.typed_check(sfx['loop'], 'boolean', True):
				self.add(' loop')
		elif sfx['action'] == 'stop':
			explicit_all = False
			if scp.typed_check(sfx['target'], 'rel', 'ALL'):
				explicit_all = True
			self.add('stop sound')
			if not explicit_all:
				self._warnings['targeted_sfx_stop'] = ["Ren'py does not support targeted sound stop; any such directives will be compiled as if they were STOP ALL"]
			if sfx['duration'] is not None:
				time = scp.get_duration(sfx['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
				self.add(' fadeout ' + str(time))
		self.add_line()
		self.add_line()
			
	def _compile_FMV(self, fmv):
		name = fmv['target'][1]
		if scp.typed_check(fmv['target'], 'string'):
			name = scp.quote(name)
		self.add_line('renpy.movie_cutscene(' + name + ')')
		self.add_line()
		
	def _compile_CAMERA(self, camera):
		if not self._use_camera_system:
			for a in camera['actions']:
				if a['type'] == 'SNAP':
					self._compile_line({'speaker': None, 'text': ('string', "[snap camera to %s]" % a['target'][1])})
				elif a['type'] == 'PAN':
					self._compile_line({'speaker': None, 'text': ('string', "[pan camera to %s]" % a['target'][1])})
				elif a['type'] == 'ZOOM':
					self._compile_line({'speaker': None, 'text': ('string', "[zoom camera %s]" % a['target'][1].lower())})
				self.add_line()
		else:
			for a in camera['actions']:
				if a['type'] == 'SNAP':
					self._cam_pan = a['target'][1]
					self.add_line('show layer master')
					self.add_line('at ' + self._get_current_scene_transforms())
				elif a['type'] == 'PAN':
					time = scp.get_duration(a['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
					self._cam_pan = a['target'][1]
					self.add_line('show layer master')
					self.add_line('at ' + self._get_current_scene_transforms())
					self.add_line('with MoveTransition(' + time + ')')
				elif a['type'] == 'ZOOM':
					time = scp.get_duration(a['duration'], self.quickly_rel, self.slowly_rel, self.default_duration)
					self._cam_zoom = a['target'][1]
					self.add_line('show layer master')
					self.add_line('at ' + self._get_current_scene_transforms())
					self.add_line('with MoveTransition(' + time + ')')
			self.add_line()
			
	def _compile_CHOICE(self, choice):
		label = ""
		if scp.typed_check(choice['label'], 'id'):
			label = " " + choice['label'][1]
		self.add_line("menu" + label + ":")
		self._indent_lev += 1
		if scp.typed_check(choice['title'], 'string'):
			self.add_line(scp.quote(choice['title'][1]))
			self.add_line()
		for c in choice['choices']:
			cond = ""
			if c['condition'] is not None:
				cond = " if " + str(c['condition'][1])
			self.add_line(scp.quote(c['text'][1]) + cond + ":")
			self._indent_lev += 1
			for v in c['sets']:
				self._compile_VARSET(v, noline=True)
			self.add_line('jump ' + c['target'][1])
			self.add_line()
			self._indent_lev -= 1
		self._indent_lev -= 1
			
	def _compile_DESCRIPTION(self, desc):
		# ren'py does not use descriptions, so we throw this out
		pass
		
	def _compile_SECTION(self, section):
		params=""
		for p in section['params']:
			params += p['name'][1]
			if 'default' in p:
				params += "=" + scp.get_expr(p['default'])
			params += ", "
		if len(params) > 0:
			params = '(' + params[:-2] + ')'
		self.add_line('label ' + section['section'][1] + params + ":")
		self._indent_lev += 1
		
	def _compile_FLAGSET(self, flagset):
		self.add_line('$ ' + flagset['name'][1] + ' = ' + scp.get_expr(flagset['value']))
		self.add_line()
		
	def _compile_VARSET(self, varset, noline=False):
		self.add_line('$ ' + varset['name'][1] + ' ' + scp.get_expr(varset['value'], '= '))
		if not noline:
			self.add_line()
		
	def _compile_DIALOG(self, dialog):
		self.add_line('window ' + dialog['mode'].lower())
		self.add_line()
		
	def _compile_GOTO(self, goto):
		self.add_line('jump ' + goto['destination'][1])
		self.add_line()
		
	def _compile_EXECUTE(self, execute):
		params = ""
		use_pass = False
		for p in execute['params']:
			if 'name' in p:
				use_pass = True
				params += p['name'][1] + "="
			params += scp.get_expr(p['value'])
			params += ', '
		if len(params) > 0:
			params = '(' + params[:-2] + ')'
		if use_pass:
			self.add_line('call expression %s pass %s' % (scp.quote(execute['section'][1]), params))
		else:
			self.add_line('call %s%s' % (execute['section'][1], params))
		self.add_line()
		
	def _compile_END(self, end):
		if 'retval' in end:
			self.add_line('return ' + scp.get_expr(end['retval']))
		self._indent_lev -= 1
		self.add_line()
		
	def _compile_WHILE(self, whilestmt):
		self.add_line('while ' + scp.get_expr(whilestmt['condition']) + ':')
		self._indent_lev += 1
		for st in whilestmt['statements']:
			self.compile_statement(st)
		self._indent_lev -= 1
		self.add_line()
		
	def _compile_IF(self, ifstmt):
		elsebr = None
		firstbr = True
		for br in ifstmt['branches']:
			if br['condition'] is None:
				elsestmt = br
			else:
				if firstbr:
					self.add_line('if ' + scp.get_expr(br['condition']) + ':')
					firstbr = False
				else:
					self.add_line('elif ' + scp.get_expr(br['condition']) + ':')
				self._indent_lev += 1
				for st in br['statements']:
					self.compile_statement(st)
				self._indent_lev -= 1
		if elsebr is not None:
			self.add_line('else:')
			self._indent_lev += 1
			for st in elsebr['statements']:
				self.compile_statement(st)
			self._indent_lev -= 1
			
	def _compile_PYTHON(self, python):
		self.add_line('python:')
		self._indent_lev += 1
		lines = python['body'].split('\n')
		for line in lines:
			self.add_line(line.strip())
		self._indent_lev -= 1
		self.add_line()
	
	def _get_current_scene_transforms(self):
		effects = ""
		for fx in self._cur_scene_gfx:
			effects += fx + ", "
		if self._use_camera_system:
			return effects + self._get_current_camera()
		return effects[:-2]
		
	def _get_current_camera(self):
		return self._cam_pan + ", " + self._cam_zoom
				
	def _finish_transition(self):
		self.add_line("with " + self._scene_trans)
		self._has_enter_trans = False
		self._has_exit_trans = False
		self.add_line()
		
def build_show(target, states):
	show = 'show ' + target
	for s in states:
		show += " " + s[1]
	return show