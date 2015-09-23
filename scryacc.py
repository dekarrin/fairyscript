import ply.yacc as yacc

from scrlex import tokens

def p_enter_directive_2_id(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=[], transition=None, motion=None)
	
def p_enter_directive_2_id_states(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=p[5], transition=None, motion=None)
	
def p_enter_directive_2_id_trans_in(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID transition_in ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=[], transition=p[4], motion=None)
	
def p_enter_directive_2_id_states_trans_in(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' transition_in ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=p[5], transition=p[7], motion=None)
	
def p_enter_directive_2_id_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID motion_geometry ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=[], transition=None, motion=p[4])
	
def p_enter_directive_2_id_states_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' motion_geometry ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=p[5], transition=None, motion=p[7])
	
def p_enter_directive_2_id_trans_in_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID transition_in motion_geometry ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=[], transition=p[4], motion=p[5])
	
def p_enter_directive_2_id_states_trans_in_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' transition_in motion_geometry ']' '''
	p[0] = make_dir('ENTER', target=('id', p[3]), states=p[5], transition=p[7], motion=p[8])

def p_action_directive_2_states(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' actor_states ']' '''
	p[0] = make_dir('ACTION', target=('id', p[2]), states=p[4], destination=None)
	
def p_action_directive_2_go_destination(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' GO destination ']' '''
	p[0] = make_dir('ACTION', target=('id', p[2]), states=[], destination=p[5])
	
def p_action_directive_2_states_go_destination(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' actor_states ',' GO destination ']' '''
	p[0] = make_dir('ACTION', target=('id', p[2]), states=p[4], destination=p[7])

def p_exit_directive_2_id(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID ']' '''
	p[0] = make_dir('EXIT', target=('id', p[3]), transition=None, motion=None)
	
def p_exit_directive_2_id_trans_out(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID transition_out ']' '''
	p[0] = make_dir('EXIT', target=('id', p[3]), transition=p[4])
	
def p_exit_directive_2_id_motion(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID motion_geometry ']' '''
	p[0] = make_dir('EXIT', target=('id', p[3]), transition=None, motion=p[4])
	
def p_exit_directive_2_id_trans_out_motion(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID transition_out motion_geometry ']' '''
	p[0] = make_dir('EXIT', target=('id', p[3]), transition=p[4], motion=p[5])

def p_music_directive_2_stop(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP ']' '''
	p[0] = make_dir('MUSIC', target=('rel', 'ALL'), duration=None, action='stop')
	
def p_music_directive_2_stop_dur(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP duration ']' '''
	p[0] = make_dir('MUSIC', target=('rel', 'ALL'), duration=p[4], action='stop')
	
def p_music_directive_2_stop_elem(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP any_element_id ']' '''
	p[0] = make_dir('MUSIC', target=p[4], duration=None, action='stop')
	
def p_music_directive_2_stop_elem_dur(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP any_element_id duration ']' '''
	p[0] = make_dir('MUSIC', target=p[4], duration=p[5], action='stop')
	
def p_music_directive_2_elem(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' element_id ']' '''
	p[0] = make_dir('MUSIC', target=p[3], fadeout=None, action='start')
	
def p_music_directive_2_elem_fadeout(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' element_id ',' FADEOUT_OLD ']' '''
	p[0] = make_dir('MUSIC', target=p[3], fadeout=('literal', 5), action='start')
	
def p_music_directive_2_elem_fadeout_dur(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' element_id ',' FADEOUT_OLD duration ']' '''
	p[0] = make_dir('MUSIC', target=p[3], fadeout=p[6], action='start')

def p_gfx_directive_2_elem_id(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' element_id ']' '''
	p[0] = make_dir('GFX', target=p[3], loop=('literal', False), action='start')
	
def p_gfx_directive_2_loop_elem_id(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' LOOP element_id ']' '''
	p[0] = make_dir('GFX', target=p[4], loop=('literal', True), action='start')
	
def p_gfx_directive_2_stop_elem(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP any_element_id ']' '''
	p[0] = make_dir('GFX', target=p[4], duration=None, action='stop')
	
def p_gfx_directive_2_stop_elem_dur(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP any_element_id duration ']' '''
	p[0] = make_dir('GFX', target=p[4], duration=p[5], action='stop')
	
def p_gfx_directive_2_stop(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP ']' '''
	p[0] = make_dir('GFX', target=('rel', 'ALL'), duration=None, action='stop')
	
def p_gfx_directive_2_stop_dur(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP duration ']' '''
	p[0] = make_dir('GFX', target=('rel', 'ALL'), duration=p[4], action='stop')

def p_sfx_directive_2_elem_id(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' element_id ']' '''
	p[0] = make_dir('SFX', target=p[3], loop=('literal', False), action='start')
	
def p_sfx_directive_2_loop_elem_id(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' LOOP element_id ']' '''
	p[0] = make_dir('SFX', target=p[4], loop=('literal', True), action='start')
	
def p_sfx_directive_2_stop_elem(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP any_element_id ']' '''
	p[0] = make_dir('SFX', target=p[4], duration=None, action='stop')
	
def p_sfx_directive_2_stop_elem_dur(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP any_element_id duration ']' '''
	p[0] = make_dir('SFX', target=p[4], duration=p[5], action='stop')
	
def p_sfx_directive_2_stop(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP ']' '''
	p[0] = make_dir('SFX', target=('rel', 'ALL'), duration=None, action='stop')
	
def p_sfx_directive_2_stop_dur(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP duration ']' '''
	p[0] = make_dir('SFX', target=('rel', 'ALL'), duration=p[4], action='stop')

def p_fmv_directive_2_elem_id(p):
	'''fmv_directive : DIRECTIVEOPEN_FMV ':' element_id ']' '''
	p[0] = make_dir('FMV', target=p[3])

def p_flagset_annotation_2_id(p):
	'''flagset_annotation : ANNOTATIONOPEN_FLAGSET ':' ID ')' '''
	p[0] = make_ann('FLAGSET', name=('id', p[3]), value=('literal', True))
	
def p_flagset_annotation_2_id_bool_expression(p):
	'''flagset_annotation : ANNOTATIONOPEN_FLAGSET ':' ID bool_expression ')' '''
	p[0] = make_ann('FLAGSET', name=('id', p[3]), value=p[4])
	
def p_dialog_annotation_2_token(p):
	'''dialog_annotation	: ANNOTATIONOPEN_DIALOG ':' HIDE ')'
							| ANNOTATIONOPEN_DIALOG ':' SHOW ')'
							| ANNOTATIONOPEN_DIALOG ':' AUTO ')' '''
	p[0] = make_ann('DIALOG', mode=p[3])

def p_goto_annotation_2_tokens(p):
	'''goto_annotation : ANNOTATIONOPEN_GOTO ':' ID ')' '''
	p[0] = make_ann('GOTO', destination=('id', p[3]))
	
def p_transition_to_2_id_to(p):
	'transition_to : ID TO'
	p[0] = ('id', p[1])
	
def p_actor_states_2_id(p):
	'actor_states : ID'
	p[0] = [ ('id', p[1]) ]
	
def p_actor_states_2_id_actor_states(p):
	'''actor_states : ID ',' actor_states'''
	p[0] = [ ('id', p[1] ) ] + p[3]

def p_transition_in_2_id_in(p):
	'transition_in : ID IN'
	p[0] = ('id', p[1])

def p_motion_geometry_2_destination(p):
	'motion_geometry : destination'
	p[0] = {'destination': p[1], 'origin': None, 'duration': None}
	
def p_motion_geometry_2_origin_destination(p):
	'motion_geometry : origin destination'
	p[0] = {'destination': p[2], 'origin': p[1], 'duration': None}
	
def p_motion_geometry_2_destination_duration(p):
	'motion_geometry : destination duration'
	p[0] = {'destination': p[1], 'origin': None, 'duration': p[2]}
	
def p_motion_geometry_2_origin_destination_duration(p):
	'motion_geometry : origin destination duration'
	p[0] = {'destination': p[2], 'origin': p[1], 'duration': p[3]}

def p_destination_2_to_id(p):
	'destination : TO ID'
	p[0] = ('id', p[2])

def p_transition_out_2_id_out(p):
	'transition_out : ID OUT'
	p[0] = ('id', p[1])
	
def p_any_elem_id_2_elem_id(p):
	'any_element_id : element_id'
	p[0] = p[1]
	
def p_any_elem_id_2_all(p):
	'any_element_id : ALL'
	p[0] = ('rel', p[1])
	
def p_duration_2_for_num(p):
	'''duration : FOR NUMBER
				| FOR NUMBER SECONDS'''
	p[0] = ('literal', to_number(p[2]))
	
def p_duration_2_relative(p):
	'''duration : QUICKLY
				| SLOWLY'''
	p[0] = ('rel', p[1])
	
def p_element_id_2_str(p):
	'element_id : STRING'
	p[0] = ('string', unescape_str(p[1]))

def p_element_id_2_id(p):
	'element_id : ID'
	p[0] = ('id', p[1])
	
def p_bool_expression_2_off(p):
	'bool_expression : OFF'
	p[0] = ('literal', False)
	
def p_bool_expression_2_on(p):
	'bool_expression : ON'
	p[0] = ('literal', True)
	
def p_bool_expression_2_bare(p):
	'bool_expression : BARE_EXPRESSION'
	p[0] = ('expr', unescape_str(p[1]).strip())
	
def p_by_amount(p):
	'by_amount : BY NUMBER'
	p[0] = ('literal', to_number(p[2]))
	
def p_origin(p):
	'origin : FROM ID'
	p[0] = ('id', p[2])

	
def to_number(s):
	if '.' in s:
		return float(s)
	else:
		return int(s)
		
def unescape_str(s):
	stripped = ''
	escaping = False
	s = s[1:-1]
	for c in s:
		if c == '\\' and not escaping:
			escaping = True
		else:
			stripped += c
			escaping = False
	return stripped
	
def make_ann(instruction, **kwargs):
	ann = {'type': 'annotation', 'instruction': instruction}
	for k in kwargs:
		ann[k] = kwargs[k]
	return ann
	
def make_dir(instruction, **kwargs):
	ann = {'type': 'directive', 'instruction': instruction}
	for k in kwargs:
		ann[k] = kwargs[k]
	return ann