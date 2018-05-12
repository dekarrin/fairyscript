from . import fey
import re

from ..docx import Document
from ..docx.enum.text import WD_PARAGRAPH_ALIGNMENT as WD_ALIGN_PARAGRAPH, WD_UNDERLINE
from ..docx.enum.style import WD_STYLE_TYPE
from ..docx.shared import Inches
from ..docx.shared import Pt
from ..docx.shared import RGBColor


class DocxCompiler(object):
	def __init__(self):
		self.screenplay_mode = False
		self.scene_metadata = None
		self.main_character = None
		self.paragraph_spacing = 0
		self.include_flagsets = True
		self.include_varsets = True
		self.include_python = True
		self.title = None
		
		self._document = None
		self._last_paragraph = None
		self._just_completed_line = False
		self._last_speaker = None
		self._last_run = None
		self._num_docs = 0
		self._warnings = {}
		self._screenplay_actor_margin = Inches(4)
		self._add_break = True
		self._indent_level = 0
		self._outer_loops_ending = 0
		self._chars = None
		
	def set_options(self, options):
		self.paragraph_spacing = options.paragraph_spacing
		self.title = options.title
		self.include_flagsets = options.include_flags
		self.include_varsets = options.include_vars
		self.include_python = options.include_python
		
	def set_characters(self, chars):
		self._chars = chars
	
	def compile_script(self, script, inputfile=None, add_title=True):
		self._check_screenplay_vars()
		self._num_docs += 1
		self._indent_level = 0
		self._outer_loops_ending = 0
		if inputfile is None:
			self._document = Document()
		else:
			self._document = Document(inputfile)
		self._set_style_defaults()
		if add_title:
			if self.title is None:
				self._document.add_heading("Script File #" + str(self._num_docs))
			else:
				self._document.add_heading(self.title % str(self._num_docs))
		self._last_paragraph = None
		self._last_run = None
		self._just_completed_line = False
		self._last_speaker = None
		
		if script is not None:
			for statement in script:
				self.compile_statement(statement)
		return self._document
	
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
		
	def set_para_format(self, **kwargs):
		fmt = self._last_paragraph.paragraph_format
		for k in kwargs:
			setattr(fmt, k, kwargs[k])
			
	def set_text_format(self, **kwargs):
		fmt = self._last_run.font
		for k in kwargs:
			setattr(fmt, k, kwargs[k])
			
	def set_text_color(self, r, g, b):
		c = self._last_run.font.color
		c.rgb = RGBColor(r, g, b)
	
	def add_actor_run(self, actor, fmt_str=None):
		if fmt_str is None:
			fmt_str = "%s"
		if actor in self._chars:
			c = self._chars[actor]
			self.add_run(fmt_str % c['name'])
			if c['color'] is not None:
				r = int(c['color'][1:3], 16)
				g = int(c['color'][3:5], 16)
				b = int(c['color'][5:7], 16)
				self.set_text_color(r, g, b)
		else:
			self.add_run(fmt_str % actor)
			
	def _set_style_defaults(self):
		styles = self._document.styles
		normal_style = styles['Normal']
		normal_fmt = normal_style.paragraph_format
		normal_fmt.space_before = Pt(self.paragraph_spacing)
		normal_fmt.space_after = Pt(self.paragraph_spacing)
		fmt = normal_style.font
		fmt.size = Pt(11)
		if 'Slugline Transition' not in styles:
			sl_trans_style = styles.add_style('Slugline Transition', WD_STYLE_TYPE.PARAGRAPH)
			sl_trans_style.base_style = styles['Normal']
			pfmt = sl_trans_style.paragraph_format
			pfmt.alignment = WD_ALIGN_PARAGRAPH.RIGHT
			pfmt.keep_together = True
			pfmt.keep_with_next = True
			pfmt.widow_control = True
			ffmt = sl_trans_style.font
			ffmt.bold = True
			ffmt.italic = True
		if 'Slugline' not in styles:
			sl_style = styles.add_style('Slugline', WD_STYLE_TYPE.PARAGRAPH)
			sl_style.base_style = styles['Normal']
			pfmt = sl_style.paragraph_format
			pfmt.widow_control = True
			ffmt = sl_style.font
			ffmt.bold = True
			ffmt.all_caps = True
		if 'Actor Instruction' not in styles:
			ai_style = styles.add_style('Actor Instruction', WD_STYLE_TYPE.PARAGRAPH)
			ai_style.base_style = styles['Normal']
			ffmt = ai_style.font
			ffmt.italic = True
		if 'Engine Instruction' not in styles:
			ei_style = styles.add_style('Engine Instruction', WD_STYLE_TYPE.PARAGRAPH)
			ei_style.base_style = styles['Normal']
			ffmt = ei_style.font
			ffmt.bold = True
			ffmt.italic = True
		if 'Reader Instruction' not in styles:
			ri_style = styles.add_style('Reader Instruction', WD_STYLE_TYPE.PARAGRAPH)
			ri_style.base_style = styles['Normal']
			ffmt = ri_style.font
			ffmt.bold = True
			ffmt.italic = True
			ffmt.all_caps = True
		if 'Choice' not in styles:
			ch_style = styles.add_style('Choice', WD_STYLE_TYPE.PARAGRAPH)
			ch_style.base_style = styles['List Bullet']
			ffmt = ch_style.font
			ffmt.bold = True
		if 'Choice Condition' not in styles:
			chc_style = styles.add_style('Choice Condition', WD_STYLE_TYPE.CHARACTER)
			chc_style.base_style = styles['Choice']
			ffmt = chc_style.font
			ffmt.italic = True
		if 'Choice Instruction' not in styles:
			chi_style = styles.add_style('Choice Instruction', WD_STYLE_TYPE.PARAGRAPH)
			chi_style.base_style = styles['List Bullet 2']
			ffmt = chi_style.font
			ffmt.italic = True
		if 'Code' not in styles:
			s = styles.add_style('Code', WD_STYLE_TYPE.PARAGRAPH)
			pfmt = s.paragraph_format
			pfmt.space_before = Pt(0)
			pfmt.space_after = Pt(0)
			ffmt = s.font
			ffmt.name = "Courier New"
			ffmt.size = Pt(styles['Normal'].font.size.pt - 3)
		if 'Hyperlink' not in styles:
			s = styles.add_style('Hyperlink', WD_STYLE_TYPE.CHARACTER)
			ffmt = s.font
			ffmt.color.rgb = RGBColor(0x00, 0x00, 0xff)
			ffmt.underline = WD_UNDERLINE.SINGLE
		
	def add_paragraph(self, text=None, bold=None, italic=None, style=None):
		if style is None:
			self._last_paragraph = self._document.add_paragraph()
		else:
			self._last_paragraph = self._document.add_paragraph(style=style)
		self._last_run = None
		if text is not None:
			self.add_run(text, bold, italic)
		if self._indent_level > 0:
			tabs = 0.5 * self._indent_level
			fmt = self._last_paragraph.paragraph_format
			start = 0
			if fmt.left_indent is not None:
				start = fmt.left_indent.inches
			fmt.left_indent = Inches(tabs + start)
			
	def add_bookmark(self, title):
		self._last_paragraph.add_bookmark(title)
		
	def add_internal_link(self, text, bookmark):
		self._last_paragraph.add_hyperlink(text=text, anchor=bookmark, style='Hyperlink')
			
	def add_run(self, text, bold=None, italic=None, style=None):
		if style is not None:
			self._last_run = self._last_paragraph.add_run(text, style=style)
		else:
			self._last_run = self._last_paragraph.add_run(text)
		if bold is not None:
			self.set_text_format(bold=bold)
		if italic is not None:
			self.set_text_format(italic=italic)
		
	def compile_statement(self, statement):
		self._add_break = True
		if statement['type'] == 'line':
			self._compile_line(statement)
		else:
			if self._just_completed_line and not self.screenplay_mode:
				self.add_paragraph()
				self._last_speaker = None
				self._just_completed_line = False
			if statement['type'] == 'comment':
				self.add_paragraph('(' + fey.extract_comment(statement['text']) + ')', style='Actor Instruction')
			else:
				instruction = statement['instruction']
				func = getattr(DocxCompiler, '_compile_' + instruction)
				func(self, statement)
			if self._add_break and self._outer_loops_ending == 0:
				self.add_paragraph()
		
	def _compile_line(self, line):
		internal = False
		sp = line['speaker']
		if sp is not None:
			sp = sp[1]
		else:
			internal = True
		continuing = self._just_completed_line and sp == self._last_speaker
		if self.screenplay_mode:
			cont = ""
			vo = ""
			if continuing:
				cont = " (CONT'D)"
			if internal:
				vo = " (V.O.)"
				charname = self.main_character.upper()
			else:
				charname = sp.upper()
			self.add_paragraph(charname + vo + cont)
			self.set_para_format(left_indent=self._screenplay_actor_margin)
		else:
			if self._just_completed_line and sp != self._last_speaker:
				self.add_paragraph()
			if sp is None:
				self.add_paragraph(line['text'][1])
			else:
				self.add_paragraph()
				self.add_actor_run(sp, "%s:")
				self.add_run(' "' + line['text'][1] + '"')
		self._just_completed_line = True
		self._last_speaker = sp

	# noinspection PyPep8Naming
	def _compile_SCENE(self, scene):
		if scene['transition'] is None:
			trans = "cut to:"
		else:
			trans = scene['transition'][1] + " to:"
		self.add_paragraph(trans.capitalize() + "\n\n", style='Slugline Transition')
		name = fey.to_words(scene['name'][1])
		self.add_paragraph(name, style='Slugline')

	# noinspection PyPep8Naming
	def _compile_ENTER(self, enter):
		geom = enter['motion']
		dest = None
		origin = None
		if geom is not None:
			if geom['destination'] is not None:
				dest = geom['destination'][1]
			if geom['origin'] is not None:
				origin = geom['origin'][1]
				
		line = fey.to_words(enter['target'][1]).title()
		if len(enter['states']) > 0:
			line += ','
			line += make_states(enter['states'])
			line += ', '
		else:
			line += ' '
		if enter['transition'] is not None:
			line += fey.to_words(enter['transition'][1]).lower() + 's in to '
		else:
			line += 'enters '
		line += 'the scene'
		if origin is not None:
			line += ' near the ' + fey.to_words(origin).lower()
		if dest is not None:
			line += ' and moves to the ' + fey.to_words(dest).lower()
		if geom is not None:
			line += fey.get_duration_words(geom['duration'], 'over %d seconds')
		line += '.'
		self.add_paragraph(line, style='Actor Instruction')

	# noinspection PyPep8Naming
	def _compile_ACTION(self, action):
		line = fey.to_words(action['target'][1]).title() + ' '
		if len(action['states']) > 0:
			line += 'changes to appear'
			line += make_states(action['states'])
			if action['destination'] is not None:
				line += ', and then '
		if action['destination'] is not None:
			line += 'moves to the ' + fey.to_words(action['destination'][1]).lower()
			line += fey.get_duration_words(action['duration'], 'over %d seconds')
		line += '.'
		self.add_paragraph(line, style='Actor Instruction')

	# noinspection PyPep8Naming
	def _compile_EXIT(self, xit):
		geom = xit['motion']
		dest = None
		origin = None
		if geom is not None:
			if geom['destination'] is not None:
				dest = geom['destination'][1]
			if geom['origin'] is not None:
				origin = geom['origin'][1]
		
		line = fey.to_words(xit['target'][1]).title() + ' '
		if geom is not None:
			line += 'moves '
		if origin is not None:
			line += 'from the ' + fey.to_words(origin).lower() + ' '
		if dest is not None:
			line += 'to the ' + fey.to_words(dest).lower() + ' '
		if geom is not None:
			line += 'and '
		if xit['transition'] is not None:
			line += fey.to_words(xit['transition'][1]).lower() + 's out of '
		else:
			line += 'exits '
		line += 'the scene'
		if geom is not None:
			line += fey.get_duration_words(geom['duration'], 'over %d seconds')
		line += '.'
		self.add_paragraph(line, style='Actor Instruction')

	# noinspection PyPep8Naming
	def _compile_MUSIC(self, music):
		self.add_paragraph(style='Actor Instruction')
		song = music['target'][1]
		if fey.typed_check(music['target'], 'string'):
			dot = song.rfind('.')
			song = song[0:dot]
		line = 'We hear '
		if music['action'] == 'start':
			if music['fadeout'] is not None:
				line += 'the current music fade out' + fey.get_duration_words(music['fadeout'], 'over %d seconds') + ', '
				line += 'and then we hear '
			line += 'the song '
			self.add_run(line)
			self.add_run(fey.to_words(song).title(), italic=False)
			self.add_run(' begin to play.')
		elif music['action'] == 'stop':
			if fey.typed_check(music['target'], 'rel'):
				line += song.lower() + ' music '
			else:
				line += 'the song '
				self.add_run(line)
				self.add_run(fey.to_words(song).title(), italic=False)
				line = ' '
			if music['duration'] is not None:
				line += 'fade out' + fey.get_duration_words(music['duration'], 'over %d seconds') + '.'
			else:
				line += 'stop.'
			self.add_run(line)

	# noinspection PyPep8Naming
	def _compile_GFX(self, gfx):
		line = 'We see '
		if gfx['action'] == 'start':
			a = fey.indef_article(gfx['target'][1])
			line += a + ' ' + fey.to_words(gfx['target'][1]).upper()
			if fey.typed_check(gfx['loop'], 'boolean', True):
				line += ' effect begin and continue'
			line += '.'
		elif gfx['action'] == 'stop':
			if fey.typed_check(gfx['target'], 'rel'):
				line += gfx['target'][1].lower() + ' effects '
			else:
				line += 'the ' + fey.to_words(gfx['target'][1]).upper() + ' effect '
			if gfx['duration'] is not None:
				line += 'fade away' + fey.get_duration_words(gfx['duration'], 'over %d seconds') + '.'
			else:
				line += 'stop.'
		self.add_paragraph(line, style='Actor Instruction')

	# noinspection PyPep8Naming
	def _compile_SFX(self, sfx):	
		fx = sfx['target'][1]
		if fey.typed_check(sfx['target'], 'string'):
			dot = fx.rfind('.')
			fx = fx[0:dot]
		line = 'We hear '
		if sfx['action'] == 'start':
			a = fey.indef_article(fx)
			line += a + ' ' + fey.to_words(fx).upper()
			if fey.typed_check(sfx['loop'], 'boolean', True):
				line += ' sound begin to repeat'
			line += '.'
		elif sfx['action'] == 'stop':
			if fey.typed_check(sfx['target'], 'rel'):
				line += fx.lower() + ' repeating sounds '
			else:
				line += 'the repeated ' + fey.to_words(fx).upper() + ' sound '
			if sfx['duration'] is not None:
				line += 'fade away' + fey.get_duration_words(sfx['duration'], 'over %d seconds') + '.'
			else:
				line += 'stop.'
		self.add_paragraph(line, style='Actor Instruction')

	# noinspection PyPep8Naming
	def _compile_FMV(self, fmv):
		self.add_paragraph(style='Actor Instruction')
		self.add_run("We see the full-motion video ")
		self.add_run(fey.to_words(fmv['target'][1]), italic=False)
		self.add_run(' play.')

	# noinspection PyPep8Naming
	def _compile_CAMERA(self, camera):
		line = 'We'
		acts_added = 0
		for act in camera['actions']:
			if acts_added == len(camera['actions']) - 1 and len(camera['actions']) > 1:
				line += ' and then'
			if 'duration' in act and fey.typed_check(act['duration'], 'rel'):
				line += fey.get_duration_words(act['duration'], '')
			if act['type'] == 'SNAP':
				line += ' focus on the ' + fey.to_words(act['target'][1])
			elif act['type'] == 'PAN':
				line += ' shift our focus to the ' + fey.to_words(act['target'][1])
			elif act['type'] == 'ZOOM':
				line += ' move '
				if fey.typed_check(act['target'], 'rel', 'IN'):
					line += 'in closer'
				elif fey.typed_check(act['target'], 'rel', 'OUT'):
					line += 'back farther'
			if 'duration' in act and not fey.typed_check(act['duration'], 'rel'):
				line += fey.get_duration_words(act['duration'], 'over %d seconds')
			if acts_added < len(camera['actions']) - 1 and len(camera['actions']) > 2:
				line += ','
			acts_added += 1
		line += '.'
		self.add_paragraph(line, style='Actor Instruction')

	# noinspection PyPep8Naming
	def _compile_CHOICE(self, choice):
		if choice['label'] is not None:
			labelstmt = {'type': 'annotation', 'instruction': 'SECTION', 'section': choice['label'], 'params': []}
			self.compile_statement(labelstmt)
		self.add_paragraph("We are presented with a choice:", style='Actor Instruction')
		if choice['title'] is not None:
			self.add_paragraph(choice['title'][1], italic=False)
		for c in choice['choices']:
			self.add_paragraph(style='Choice')
			if c['condition'] is None:
				self.add_run(c['text'][1])
			else:
				self.add_run(c['text'][1] + "\n")
				if fey.typed_check(c['condition'], 'boolean', True):
					self.add_run('(always shown)', style='Choice Condition')
				elif fey.typed_check(c['condition'], 'boolean', False):
					self.add_run('(never shown)', style='Choice Condition')
				elif fey.typed_check(c['condition'], 'id'):
					cond_id = fey.to_words(c['condition'][1]).lower()
					if cond_id.startswith('have '):
						cond_ph = cond_id[len('have '):]
						self.add_run('(choice shown only if we have ' + cond_ph + ')', style='Choice Condition')
					else:
						self.add_run('(choice shown only if \'' + cond_id + '\' is set)', style='Choice Condition')
				else:
					self.add_run('(choice shown only if ' + fey.to_human_readable(c['condition'][1]) + ')', style='Choice Condition')
			if self.include_varsets:
				for v in c['sets']:
					self.add_paragraph(self.make_varset(v)[0], style='Choice Instruction')
			self.add_paragraph(style='Choice Instruction')
			go = self.make_goto({'destination': c['target']})
			self.add_run(go[0])
			self.add_internal_link(go[1], go[2])
			self.add_run('.')

	# noinspection PyPep8Naming
	def _compile_DESCRIPTION(self, desc):
		self.add_paragraph(style='Actor Instruction')
		if desc['target'] is not None:
			self.add_run("Regarding ")
			self.add_run(fey.to_words(desc['target'][1]).title() + ': ', italic=False)
		self.add_run(desc['text'][1])

	# noinspection PyPep8Naming
	def _compile_SECTION(self, section):
		name = fey.to_words(section['section'][1]).title()
		bookmark = self.to_bookmark(name)
		self._document.add_heading(fey.to_words(section['section'][1]).title(), level=2, bookmark_name=bookmark)
		self._add_break = False

	# noinspection PyPep8Naming
	def _compile_FLAGSET(self, flagset):
		if self.include_flagsets:
			fs = self.make_flagset(flagset)
			if fs[1]:
				style = 'Actor Instruction'
			else:
				style = 'Engine Instruction'
			self.add_paragraph(fs[0], style=style)
		else:
			self._add_break = False

	# noinspection PyPep8Naming
	def _compile_VARSET(self, varset):
		if self.include_varsets:
			vs = self.make_varset(varset)
			if vs[1]:
				style = 'Actor Instruction'
			else:
				style = 'Engine Instruction'
			self.add_paragraph(vs[0], style=style)
		else:
			self._add_break = False

	# noinspection PyPep8Naming
	def _compile_DIALOG(self, dialog):
		if dialog['mode'] == 'AUTO':
			line = 'Set the dialog window to automatically show/hide.'
		else:
			line = dialog['mode'].capitalize() + " the dialog window."
		self.add_paragraph(line, style='Engine Instruction')

	# noinspection PyPep8Naming
	def _compile_GOTO(self, goto):
		self.add_paragraph(style='Reader Instruction')
		go = self.make_goto(goto)
		self.add_run(go[0])
		self.add_internal_link(go[1], go[2])

	# noinspection PyPep8Naming
	def _compile_EXECUTE(self, execute):
		section_name = fey.to_words(execute['section'][1]).title()
		bookmark = self.to_bookmark(section_name)
		self.add_paragraph("Execute ", style='Reader Instruction')
		self.add_internal_link(section_name, bookmark)

	# noinspection PyPep8Naming
	def _compile_INCLUDE(self, include):
		if not include['parsing'][1]:
			try:
				with open(include['file'][1]) as inc_file:
					for line in inc_file:
						self.add_paragraph(line)
			except IOError as e:
				self.add_warning("file_inclusion", "can't include '%s': %s" % (include['file'][1], str(e)))

	# noinspection PyPep8Naming
	def _compile_END(self, end):
		if 'retval' in end:
			self.add_paragraph('Return from this section', style='Reader Instruction')
		else:
			self._add_break = False

	# noinspection PyPep8Naming
	def _compile_WHILE(self, whilestmt):
		line = "Do the following "
		cond = fey.get_expr(whilestmt['condition'])
		if fey.typed_check(whilestmt['condition'], 'boolean'):
			tcond = whilestmt['condition'][1]
			if tcond:
				line += 'forever:'
			else:
				line = 'Never do the following:'
		elif fey.typed_check(whilestmt['condition'], 'id'):
			cond_words = fey.to_words(whilestmt['condition'][1]).lower()
			if cond_words.startswith('have '):
				cond_ph = cond_words[len('have '):]
				line += 'while we have ' + cond_ph + ':'
			else:
				line += 'while ' + fey.quote(cond_words, "'") + ' is set:'
		else:
			line += 'while ' + fey.to_human_readable(cond) + ':'
		if self.contains_writeable(whilestmt['statements']):
			self.add_paragraph(line, style='Engine Instruction')
			self.compile_block(whilestmt['statements'])
		else:
			self._add_break = False

	# noinspection PyPep8Naming
	def _compile_IF(self, ifstmt):
		elsebr = None
		firstbr = True
		had_output = False
		for br in ifstmt['branches']:
			if br['condition'] is None:
				elsebr = br
			else:
				if not self.contains_writeable(br['statements']):
					continue
				had_output = True
				negation = ''
				if firstbr:
					line = '%s do the following'
					firstbr = False
				else:
					line = 'Otherwise,%s do the following'
				cond = fey.get_expr(br['condition'])
				if fey.typed_check(br['condition'], 'boolean'):
					tcond = br['condition'][1]
					if tcond:
						negation = ' always'
						line += ':'
					else:
						negation = ' never'
						line += ':'
				elif fey.typed_check(br['condition'], 'id'):
					cond_words = fey.to_words(br['condition'][1]).lower()
					if cond_words.startswith('have '):
						cond_ph = cond_words[len('have '):]
						line += ' only if we have ' + cond_ph + ':'
					else:
						line += ' only if ' + fey.quote(cond_words, "'") + ' is set:'
				else:
					line += ' only if ' + fey.to_human_readable(cond) + ':'
				self.add_paragraph((line % negation).strip().capitalize(), style='Engine Instruction')
				self.compile_block(br['statements'])
		if elsebr is not None and had_output and self.contains_writeable(elsebr['statements']):
			self.add_paragraph("Otherwise, do the following:", style='Engine Instruction')
			self.compile_block(elsebr['statements'])
		if not had_output:
			self._add_break = False

	# noinspection PyPep8Naming
	def _compile_CHARACTERS(self, characters):
		pass

	# noinspection PyPep8Naming
	def _compile_PYTHON(self, python):
		if self.include_python:
			self.add_paragraph("Execute the following python code:", style='Engine Instruction')
			self.add_paragraph("{")
			lines = python['body'].split('\n')
			start = re.match(r'\s*', lines[0]).end(0)
			self._indent_level += 1
			for line in lines:	
				self.add_paragraph(line[start:], style='Code')
			self._indent_level -= 1
			self.add_paragraph("}")
		else:
			self.add_paragraph("Execute python code here.", style='Engine Instruction')
		
	def _check_screenplay_vars(self):
		if self.screenplay_mode:
			if self.main_character is None:
				msg = "a main character is required for screenplay mode; using 'Main character'"
				self.add_warning('main_char_not_defined', msg)
				self.main_character = 'Main character'
				
	def compile_block(self, statements):
		self.add_paragraph("{")
		self._indent_level += 1
		stmts_added = 0
		for st in statements:
			if stmts_added == len(statements) - 1:
				self._outer_loops_ending += 1
			self.compile_statement(st)
			stmts_added += 1
		self._outer_loops_ending -= 1
		self._indent_level -= 1
		self._last_speaker = None
		self._just_completed_line = False
		self.add_paragraph("}")

	# noinspection PyMethodMayBeStatic
	def make_flagset(self, flagset):
		line = ''
		value = fey.get_expr(flagset['value'])
		tvalue = flagset['value'][1]
		flag = fey.to_words(flagset['name'][1]).lower()
		nat_lang = flag.startswith('have ')
		if nat_lang:
			phrase = flag[len('have '):]
		else:
			phrase = ""
		if fey.typed_check(flagset['value'], 'boolean'):
			if not nat_lang:
				if tvalue:
					line = 'Set the flag ' + fey.quote(flag, "'") + '.'
				else:
					line = 'Unset the flag ' + fey.quote(flag, "'") + '.'
			else:
				if tvalue:
					line = 'We have now ' + phrase + '.'
				else:
					line = 'We have now not ' + phrase + '.'
		elif fey.typed_check(flagset['value'], 'id'):
			if nat_lang:
				line = 'Whether we have ' + phrase + ' is determined by '
			else:
				line = 'Set the flag ' + fey.quote(flag, "'") + ' to the same as '
			value_id = fey.to_words(value).lower()
			if value_id.startswith('have '):
				val_phrase = value_id[len('have '):]
				line += 'whether we have ' + val_phrase + '.'
			else:
				line += 'the value of the variable ' + fey.quote(value_id, "'") + '.'
		elif fey.typed_check(flagset['value'], 'expr'):
			if nat_lang:
				line = 'Whether we have now ' + flag + ' is determined by the value of the variable ' + value + '.'
			else:
				line = 'Set the flag ' + fey.quote(flag, "'") + ' to the same as the value of the variable ' + value + '.'
		return line, nat_lang
		
	def make_varset(self, varset):
		if fey.typed_check(varset['value'], 'boolean'):
			return self.make_flagset(varset)
		var = fey.to_words(varset['name'][1]).lower()
		value = fey.get_expr(varset['value'])
		if fey.typed_check(varset['value'], 'incdec'):
			readable = fey.to_human_readable(var + value)
			var_in = readable.rfind(var)
			var_str = readable[var_in:].replace(var, fey.quote(var, "'"), 1)
			readable = readable[0:var_in] + var_str
			line = readable.strip().capitalize() + '.'
		else:
			line = 'Set the variable ' + fey.quote(var, "'") + ' to ' + value + '.'
		return line, False
		
	def make_goto(self, goto):
		bookmark = self.to_bookmark(fey.to_words(goto['destination'][1]).title())
		return 'Jump to ', fey.to_words(goto['destination'][1]).title(), bookmark

	# noinspection PyMethodMayBeStatic
	def to_bookmark(self, text, hidden=False):
		text = text.strip()
		if not hidden:  # initial digit okay if hidden; '_' will be added at start
			text = re.sub(r'^\d', '_', text)  # remove initial digit
		text = re.sub(r'\W', '_', text)  # remove illegal chars
		text = re.sub('_+', '_', text)  # collapse runs of underscores

		# add/remove initial underscore
		if not hidden and text[0] == '_':
			text = text[1:]
		elif hidden and text[0] != '_':
			text = '_' + text

		# truncate to 40 chars:
		if len(text) > 40:
			text = text[:40]

		return text
		
	def contains_writeable(self, stmts):
		for s in stmts:
			if s['type'] == 'line' or s['type'] == 'comment':
				return True
			else:
				if s['instruction'] == 'VARSET':
					if self.include_varsets:
						return True
				elif s['instruction'] == 'FLAGSET':
					if self.include_flagsets:
						return True
				elif s['instruction'] == 'IF':
					for br in s['branches']:
						if self.contains_writeable(br['statements']):
							return True
				elif s['instruction'] == 'WHILE':
					if self.contains_writeable(s['statements']):
						return True
				else:
					return True
		return False


def make_states(states):
	states_added = 0
	line = ''
	for s in states:
		if states_added == len(states) - 1 and len(states) > 1:  # we are on the last one
			line += ' and'
		line += ' ' + fey.to_words(s[1]).lower()
		if states_added < len(states) - 1 and len(states) > 2:
			line += ','
		states_added += 1
	return line
