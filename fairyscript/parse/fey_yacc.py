from ply import yacc

from .fey_lex import tokens

def p_block_2_stmt(p):
	'''block : statement'''
	p[0] = [ p[1] ]
	
def p_block_2_stmt_block(p):
	'''block : statement block'''
	p[0] = [ p[1] ] + p[2]
	
def p_statement_2_type(p):
	'''statement	: directive
					| annotation
					| line'''
	p[0] = p[1]
	
def p_statement_2_comment(p):
	'statement : COMMENT'
	p[0] = {'type': 'comment', 'text': p[1]}
	
def p_directive_2_specific(p):
	'''directive	: scene_directive
					| enter_directive
					| action_directive
					| exit_directive
					| music_directive
					| gfx_directive
					| sfx_directive
					| fmv_directive
					| camera_directive
					| choice_directive'''
	p[0] = p[1]
					
def p_annotation_2_specific(p):
	'''annotation	: description_annotation
					| section_annotation
					| flagset_annotation
					| varset_annotation
					| dialog_annotation
					| goto_annotation
					| execute_annotation
					| end_annotation
					| while_annotation
					| include_annotation
                    | characters_annotation
					| if_annotation'''
	p[0] = p[1]
	
def p_annotation_2_python(p):
	'annotation : PYTHON_BLOCK'
	first_brace = p[1].index('{')
	last_brace = p[1].rindex('}')
	py = unescape(p[1][first_brace+1:last_brace])
	p[0] = make_annotation('PYTHON', body=py)

def p_line_2_id_str(p):
	'''line : ID ':' STRING'''
	p[0] = make_line(('id', p[1]), ('string', unescape(p[3])))
	
def p_line_2_str_str(p):
	'''line : STRING ':' STRING'''
	p[0] = make_line(('string', unescape(p[1])), ('string', unescape(p[3])))
	
def p_line_2_str(p):
	'''line : ':' STRING'''
	p[0] = make_line(None, ('string', unescape(p[2])))
	
def p_line_2_id_attr_str(p):
	'''line : ID '(' actor_states ')' ':' STRING'''
	p[0] = make_line(('id', p[1]), ('string', unescape(p[6])), p[3])
	
def p_line_2_str_attr_str(p):
	'''line : STRING '(' actor_states ')' ':' STRING'''
	p[0] = make_line(('string', unescape(p[1])), ('string', unescape(p[6])), p[3])
	
def p_line_2_str_attr(p):
	'''line : '(' actor_states ')' ':' STRING'''
	p[0] = make_line(None, ('string', unescape(p[5])), p[2])

def p_scene_directive_2_id(p):
	'''scene_directive : DIRECTIVEOPEN_SCENE ':' ID ']' '''
	p[0] = make_directive('SCENE', name=('id', p[3]), transition=None)
	
def p_scene_directive_2_trans_to_id(p):
	'''scene_directive : DIRECTIVEOPEN_SCENE ':' transition_to ID ']' '''
	p[0] = make_directive('SCENE', name=('id', p[4]), transition=p[3])

def p_enter_directive_2_id(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=[], transition=None, motion=None)
	
def p_enter_directive_2_id_states(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=p[5], transition=None, motion=None)
	
def p_enter_directive_2_id_trans_in(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID transition_in ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=[], transition=p[4], motion=None)
	
def p_enter_directive_2_id_states_trans_in(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' transition_in ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=p[5], transition=p[7], motion=None)
	
def p_enter_directive_2_id_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID motion_geometry ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=[], transition=None, motion=p[4])
	
def p_enter_directive_2_id_states_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' motion_geometry ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=p[5], transition=None, motion=p[7])
	
def p_enter_directive_2_id_trans_in_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID transition_in motion_geometry ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=[], transition=p[4], motion=p[5])
	
def p_enter_directive_2_id_states_trans_in_motion(p):
	'''enter_directive : DIRECTIVEOPEN_ENTER ':' ID '(' actor_states ')' transition_in motion_geometry ']' '''
	p[0] = make_directive('ENTER', target=('id', p[3]), states=p[5], transition=p[7], motion=p[8])

def p_action_directive_2_states(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' actor_states ']' '''
	p[0] = make_directive('ACTION', target=('id', p[2]), states=p[4], destination=None, duration=None)
	
def p_action_directive_2_go_destination(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' GO destination ']' '''
	p[0] = make_directive('ACTION', target=('id', p[2]), states=[], destination=p[5], duration=None)
	
def p_action_directive_2_go_destination_duration(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' GO destination duration ']' '''
	p[0] = make_directive('ACTION', target=('id', p[2]), states=[], destination=p[5], duration=p[6])
	
def p_action_directive_2_states_go_destination(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' actor_states ',' GO destination ']' '''
	p[0] = make_directive('ACTION', target=('id', p[2]), states=p[4], destination=p[7], duration=None)
	
def p_action_directive_2_states_go_destination_dur(p):
	'''action_directive : DIRECTIVEOPEN_ACTION ID ':' actor_states ',' GO destination duration ']' '''
	p[0] = make_directive('ACTION', target=('id', p[2]), states=p[4], destination=p[7], duration=p[8])

def p_exit_directive_2_id(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID ']' '''
	p[0] = make_directive('EXIT', target=('id', p[3]), transition=None, motion=None)
	
def p_exit_directive_2_id_trans_out(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID transition_out ']' '''
	p[0] = make_directive('EXIT', target=('id', p[3]), transition=p[4], motion=None)
	
def p_exit_directive_2_id_motion(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID motion_geometry ']' '''
	p[0] = make_directive('EXIT', target=('id', p[3]), transition=None, motion=p[4])
	
def p_exit_directive_2_id_trans_out_motion(p):
	'''exit_directive : DIRECTIVEOPEN_EXIT ':' ID transition_out motion_geometry ']' '''
	p[0] = make_directive('EXIT', target=('id', p[3]), transition=p[4], motion=p[5])

def p_music_directive_2_stop(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP ']' '''
	p[0] = make_directive('MUSIC', target=('rel', 'ALL'), duration=None, action='stop')
	
def p_music_directive_2_stop_dur(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP duration ']' '''
	p[0] = make_directive('MUSIC', target=('rel', 'ALL'), duration=p[4], action='stop')
	
def p_music_directive_2_stop_elem(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP any_element_id ']' '''
	p[0] = make_directive('MUSIC', target=p[4], duration=None, action='stop')
	
def p_music_directive_2_stop_elem_dur(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' STOP any_element_id duration ']' '''
	p[0] = make_directive('MUSIC', target=p[4], duration=p[5], action='stop')
	
def p_music_directive_2_elem(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' element_id ']' '''
	p[0] = make_directive('MUSIC', target=p[3], fadeout=None, action='start')
	
def p_music_directive_2_elem_fadeout(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' element_id ',' FADEOUT_OLD ']' '''
	p[0] = make_directive('MUSIC', target=p[3], fadeout=('number', 5), action='start')
	
def p_music_directive_2_elem_fadeout_dur(p):
	'''music_directive : DIRECTIVEOPEN_MUSIC ':' element_id ',' FADEOUT_OLD duration ']' '''
	p[0] = make_directive('MUSIC', target=p[3], fadeout=p[6], action='start')

def p_gfx_directive_2_id(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' ID ']' '''
	p[0] = make_directive('GFX', target=('id', p[3]), loop=('boolean', False), action='start')
	
def p_gfx_directive_2_loop_id(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' LOOP ID ']' '''
	p[0] = make_directive('GFX', target=('id', p[4]), loop=('boolean', True), action='start')
	
def p_gfx_directive_2_stop_elem(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP id_or_all ']' '''
	p[0] = make_directive('GFX', target=p[4], duration=None, action='stop')
	
def p_gfx_directive_2_stop_elem_dur(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP id_or_all duration ']' '''
	p[0] = make_directive('GFX', target=p[4], duration=p[5], action='stop')
	
def p_gfx_directive_2_stop(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP ']' '''
	p[0] = make_directive('GFX', target=('rel', 'ALL'), duration=None, action='stop')
	
def p_gfx_directive_2_stop_dur(p):
	'''gfx_directive : DIRECTIVEOPEN_GFX ':' STOP duration ']' '''
	p[0] = make_directive('GFX', target=('rel', 'ALL'), duration=p[4], action='stop')

def p_sfx_directive_2_elem_id(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' element_id ']' '''
	p[0] = make_directive('SFX', target=p[3], loop=('boolean', False), action='start')
	
def p_sfx_directive_2_loop_elem_id(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' LOOP element_id ']' '''
	p[0] = make_directive('SFX', target=p[4], loop=('boolean', True), action='start')
	
def p_sfx_directive_2_stop_elem(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP any_element_id ']' '''
	p[0] = make_directive('SFX', target=p[4], duration=None, action='stop')
	
def p_sfx_directive_2_stop_elem_dur(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP any_element_id duration ']' '''
	p[0] = make_directive('SFX', target=p[4], duration=p[5], action='stop')
	
def p_sfx_directive_2_stop(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP ']' '''
	p[0] = make_directive('SFX', target=('rel', 'ALL'), duration=None, action='stop')
	
def p_sfx_directive_2_stop_dur(p):
	'''sfx_directive : DIRECTIVEOPEN_SFX ':' STOP duration ']' '''
	p[0] = make_directive('SFX', target=('rel', 'ALL'), duration=p[4], action='stop')

def p_fmv_directive_2_elem_id(p):
	'''fmv_directive : DIRECTIVEOPEN_FMV ':' element_id ']' '''
	p[0] = make_directive('FMV', target=p[3])
	
def p_camera_directive_2_camera_actions(p):
	'''camera_directive : DIRECTIVEOPEN_CAMERA ':' camera_actions ']' '''
	p[0] = make_directive('CAMERA', actions=p[3])
	
def p_choice_directive_2_choices(p):
	'''choice_directive : DIRECTIVEOPEN_CHOICE ']' choices'''
	p[0] = make_directive('CHOICE', title=None, label=None, choices=p[3])
	
def p_choice_directive_2_label_choices(p):
	'''choice_directive : DIRECTIVEOPEN_CHOICE ':' ID ']' choices'''
	p[0] = make_directive('CHOICE', title=None, label=('id', p[3]), choices=p[5])
	
def p_choice_directive_2_title_choices(p):
	'''choice_directive : DIRECTIVEOPEN_CHOICE ']' STRING choices'''
	p[0] = make_directive('CHOICE', title=('string', unescape(p[3])), label=None, choices=p[4])
	
def p_choice_directive_2_label_title_choices(p):
	'''choice_directive : DIRECTIVEOPEN_CHOICE ':' ID ']' STRING choices'''
	p[0] = make_directive('CHOICE', title=('string', unescape(p[5])), label=('id', p[3]), choices=p[6])

def p_description_annotation_2_unstr(p):
	'''description_annotation : ANNOTATIONOPEN_DESCRIPTION ':' UNQUOTED_STRING ')' '''
	p[0] = make_annotation('DESCRIPTION', text=('string', unescape(' ' + p[3] + ' ')), target=None)
	
def p_description_annotation_2_id_str(p):
	'''description_annotation : ANNOTATIONOPEN_DESCRIPTION ':' ID ':' UNQUOTED_STRING ')' '''
	p[0] = make_annotation('DESCRIPTION', text=('string', unescape(' ' + p[5] + ' ')), target=('id', p[3]))
	
def p_description_annotation_2_c_unstr(p):
	'''description_annotation : ANNOTATIONOPEN_DESCRIPTION ':' ':' UNQUOTED_STRING ')' '''
	p[0] = make_annotation('DESCRIPTION', text=('string', unescape(' ' + p[4] + ' ')), target=None)
	
def p_section_annotation_2_id(p):
	'''section_annotation : ANNOTATIONOPEN_SECTION ':' ID ')' '''
	p[0] = make_annotation('SECTION', section=('id', p[3]), params=[])
	
def p_section_annotation_2_id_params(p):
	'''section_annotation : ANNOTATIONOPEN_SECTION ':' ID PARAMSOPEN params_declaration ')' '''
	p[0] = make_annotation('SECTION', section=('id', p[3]), params=p[5])
	
def p_flagset_annotation_2_id(p):
	'''flagset_annotation : ANNOTATIONOPEN_FLAGSET ':' ID ')' '''
	p[0] = make_annotation('FLAGSET', name=('id', p[3]), value=('boolean', True))
	
def p_flagset_annotation_2_id_bool_expression(p):
	'''flagset_annotation : ANNOTATIONOPEN_FLAGSET ':' ID bool_expression ')' '''
	p[0] = make_annotation('FLAGSET', name=('id', p[3]), value=p[4])
	
def p_varset_annotation_2_id(p):
	'''varset_annotation : ANNOTATIONOPEN_VARSET ':' ID ')' '''
	p[0] = make_annotation('VARSET', name=('id', p[3]), value=('number', 1))
	
def p_varset_annotation_2_id_params(p):
	'''varset_annotation	: ANNOTATIONOPEN_VARSET ':' ID inc_dec ')'
							| ANNOTATIONOPEN_VARSET ':' ID expression ')' '''
	p[0] = make_annotation('VARSET', name=('id', p[3]), value=p[4])
	
def p_dialog_annotation_2_token(p):
	'''dialog_annotation	: ANNOTATIONOPEN_DIALOG ':' HIDE ')'
							| ANNOTATIONOPEN_DIALOG ':' SHOW ')'
							| ANNOTATIONOPEN_DIALOG ':' AUTO ')' '''
	p[0] = make_annotation('DIALOG', mode=p[3])

def p_goto_annotation_2_tokens(p):
	'''goto_annotation : ANNOTATIONOPEN_GOTO ':' ID ')' '''
	p[0] = make_annotation('GOTO', destination=('id', p[3]))
	
def p_execute_annotation_2_id(p):
	'''execute_annotation : ANNOTATIONOPEN_EXECUTE ':' ID ')' '''
	p[0] = make_annotation('EXECUTE', section=('id', p[3]), params=[])
	
def p_execute_annotation_2_id_params(p):
	'''execute_annotation : ANNOTATIONOPEN_EXECUTE ':' ID PARAMSOPEN params_set ')' '''
	p[0] = make_annotation('EXECUTE', section=('id', p[3]), params=p[5])
	
def p_end_annotation_2_tokens(p):
	'''end_annotation : ANNOTATIONOPEN_END ')' '''
	p[0] = make_annotation('END')
	
def p_end_annotation_2_return(p):
	'''end_annotation : ANNOTATIONOPEN_END ':' RETURN expression ')' '''
	p[0] = make_annotation('END', retval=p[4])
	
def p_while_annotation_2_tokens(p):
	'''while_annotation : ANNOTATIONOPEN_WHILE ':' bool_expression ')' '{' block '}' '''
	p[0] = make_annotation('WHILE', condition=p[3], statements=p[6])
	
def p_if_annotation_2_single(p):
	'''if_annotation : ANNOTATIONOPEN_IF ':' bool_expression ')' '{' block '}' '''
	ifs = [ {'condition': p[3], 'statements': p[6]} ]
	p[0] = make_annotation('IF', branches=ifs)
	
def p_if_annotation_2_single_else(p):
	'''if_annotation : ANNOTATIONOPEN_IF ':' bool_expression ')' '{' block '}' ANNOTATIONOPEN_ELSE ')' '{' block '}' '''
	ifs = [ {'condition': p[3], 'statements': p[6]}, {'condition': None, 'statements': p[11]} ]
	p[0] = make_annotation('IF', branches=ifs)
	
def p_if_annotation_2_multi(p):
	'''if_annotation : ANNOTATIONOPEN_IF ':' bool_expression ')' '{' block '}' else_ifs'''
	ifs = [ {'condition': p[3], 'statements': p[6]} ] + p[8]
	p[0] = make_annotation('IF', branches=ifs)
	
def p_if_annotation_2_multi_else(p):
	'''if_annotation : ANNOTATIONOPEN_IF ':' bool_expression ')' '{' block '}' else_ifs ANNOTATIONOPEN_ELSE ')' '{' block '}' '''
	ifs = [ {'condition': p[3], 'statements': p[6]} ] + p[8] + [ {'condition': None, 'statements': p[12]} ]
	p[0] = make_annotation('IF', branches=ifs)
	
def p_include_annotation_2_str(p):
	'''include_annotation : ANNOTATIONOPEN_INCLUDE ':' STRING ')'
						  | ANNOTATIONOPEN_INCLUDE ':' STRING WITH_PARSING ')' '''
	p[0] = make_annotation('INCLUDE', file=('string', unescape(p[3])), langs=None, parsing=('boolean', True))
	
def p_include_annotation_2_str_fortarget(p):
	'''include_annotation : ANNOTATIONOPEN_INCLUDE ':' STRING FOR_TARGET id_list ')'
						  | ANNOTATIONOPEN_INCLUDE ':' STRING FOR_TARGET id_list WITH_PARSING ')' '''
	p[0] = make_annotation('INCLUDE', file=('string', unescape(p[3])), langs=p[5], parsing=('boolean', True))
	
def p_include_annotation_2_str_parsing_onoff(p):
	'''include_annotation : ANNOTATIONOPEN_INCLUDE ':' STRING WITH_PARSING bool_literal ')' '''
	p[0] = make_annotation('INCLUDE', file=('string', unescape(p[3])), langs=None, parsing=p[5])
	
def p_include_annotation_2_str_fortarget_parsing_onoff(p):
	'''include_annotation : ANNOTATIONOPEN_INCLUDE ':' STRING FOR_TARGET id_list WITH_PARSING bool_literal ')' '''
	p[0] = make_annotation('INCLUDE', file=('string', unescape(p[3])), langs=p[5], parsing=p[7])
	
def p_characters_annotation_2_str(p):
	'''characters_annotation : ANNOTATIONOPEN_CHARACTERS ':' STRING ')' '''
	p[0] = make_annotation('CHARACTERS', file=('string', unescape(p[3])))
	
def p_transition_to_2_id_to(p):
	'transition_to : ID TO'
	p[0] = ('id', p[1])
	
def p_actor_states_2_id(p):
	'actor_states : ID'
	p[0] = [ ('id', p[1]) ]
	
def p_actor_states_2_id_actor_states(p):
	'''actor_states : actor_states ',' ID'''
	p[0] = p[1] + [ ('id', p[3] ) ]

def p_transition_in_2_id_in(p):
	'transition_in : ID IN'
	p[0] = ('id', p[1])
	
def p_transition_in_2_with_scene(p):
	'transition_in : WITH_PREVIOUS'
	p[0] = ('rel', p[1])

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
	
def p_motion_geometry_2_origin(p):
	'motion_geometry : origin'
	p[0] = {'destination': None, 'origin': p[1], 'duration': None}
	
def p_motion_geometry_2_origin_duration(p):
	'motion_geometry : origin duration'
	p[0] = {'destination': None, 'origin': p[1], 'duration': p[2]}
	
def p_motion_geometry_2_duration(p):
	'motion_geometry : duration'
	p[0] = {'destination': None, 'origin': None, 'duration': p[1]}

def p_destination_2_to_id(p):
	'destination : TO ID'
	p[0] = ('id', p[2])

def p_transition_out_2_id_out(p):
	'transition_out : ID OUT'
	p[0] = ('id', p[1])
	
def p_transition_out_2_with_scene(p):
	'transition_out : WITH_PREVIOUS'
	p[0] = ('rel', p[1])
	
def p_any_elem_id_2_elem_id(p):
	'any_element_id : element_id'
	p[0] = p[1]
	
def p_any_elem_id_2_all(p):
	'any_element_id : ALL'
	p[0] = ('rel', p[1])
	
def p_duration_2_for_num(p):
	'''duration : FOR NUMBER
				| FOR NUMBER SECONDS'''
	p[0] = ('number', to_number(p[2]))
	
def p_duration_2_relative(p):
	'''duration : QUICKLY
				| SLOWLY'''
	p[0] = ('rel', p[1])
	
def p_element_id_2_str(p):
	'element_id : STRING'
	p[0] = ('string', unescape(p[1]))

def p_element_id_2_id(p):
	'element_id : ID'
	p[0] = ('id', p[1])
	
def p_camera_actions_2_camera_action(p):
	'camera_actions : camera_action'
	p[0] = [ p[1] ]
	
def p_camera_actions_2_camera_action_camera_actions(p):
	'camera_actions : camera_action AND camera_actions'
	p[0] = [ p[1] ] + p[3]
	
def p_choices_2_choice(p):
	'choices : choice'
	p[0] = [ p[1] ]
	
def p_choices_2_choice_choices(p):
	'choices : choice choices'
	p[0] = [ p[1] ] + p[2]
	
def p_params_declaration_2_id(p):
	'params_declaration : ID'
	p[0] = [ {'name': ('id', p[1]) } ]
	
def p_params_declaration_2_id_expr(p):
	'''params_declaration : ID '=' expression'''
	p[0] = [ {'name': ('id', p[1]), 'default': p[3] } ]
	
def p_params_declaration_2_id_params(p):
	'''params_declaration : ID ',' params_declaration'''
	p[0] = [ {'name': ('id', p[1]) } ] + p[3]
	
def p_params_declaration_2_id_expr_params(p):
	'''params_declaration : ID '=' expression ',' params_declaration'''
	p[0] = [ {'name': ('id', p[1]), 'default': p[3] } ] + p[5]
	
def p_bool_literal_2_off(p):
	'bool_literal : OFF'
	p[0] = ('boolean', False)
	
def p_bool_literal_2_on(p):
	'bool_literal : ON'
	p[0] = ('boolean', True)
	
def p_bool_expression_2_bool_literal(p):
	'bool_expression : bool_literal'
	p[0] = p[1]
	
def p_bool_expression_2_bare(p):
	'bool_expression : BARE_EXPRESSION'
	p[0] = ('expr', unescape(p[1]).strip())
	
def p_bool_expression_2_id(p):
	'bool_expression : ID'
	p[0] = ('id', p[1])
	
def p_inc_dec_2_rel(p):
	'''inc_dec	: INC
				| DEC'''
	p[0] = ('incdec', {'type': ('rel', p[1]), 'amount': ('number', 1)})
	
def p_inc_dec_2_rel_amount(p):
	'''inc_dec	: INC by_amount
				| DEC by_amount'''
	p[0] = ('incdec', {'type': ('rel', p[1]), 'amount': p[2]})
	
def p_expression_2_bool(p):
	'expression : bool_expression'
	p[0] = p[1]
	
def p_expression_2_string(p):
	'expression : STRING'
	p[0] = ('string', unescape(p[1]))
	
def p_expression_2_number(p):
	'expression : NUMBER'
	p[0] = ('number', to_number(p[1]))

def p_params_set_2_expr(p):
	'params_set : expression'
	p[0] = [ {'value': p[1] } ]
	
def p_params_set_2_id_expr(p):
	'''params_set : ID '=' expression'''
	p[0] = [ {'name': ('id', p[1]), 'value': p[3] } ]
	
def p_params_set_2_expr_params(p):
	'''params_set : expression ',' params_set '''
	p[0] = [ {'value': p[1] } ] + p[3]
	
def p_params_set_2_id_expr_params(p):
	'''params_set : ID '=' expression ',' params_set '''
	p[0] = [ {'name': ('id', p[1]), 'value': p[3] } ] + p[5]
	
def p_else_ifs_2_block(p):
	'''else_ifs : ANNOTATIONOPEN_ELIF ':' bool_expression ')' '{' block '}' '''
	p[0] = [ {'condition': p[3], 'statements': p[6]} ]
	
def p_else_ifs_2_block_else_ifs(p):
	'''else_ifs : ANNOTATIONOPEN_ELIF ':' bool_expression ')' '{' block '}' else_ifs '''
	p[0] = [ {'condition': p[3], 'statements': p[6]} ] + p[8]
	
def p_origin(p):
	'origin : FROM ID'
	p[0] = ('id', p[2])

def p_camera_action_2_snap_id(p):
	'camera_action : SNAP_TO ID'
	p[0] = {'type': 'SNAP', 'target': ('id', p[2])}
	
def p_camera_action_2_pan_id(p):
	'camera_action : PAN_TO ID'
	p[0] = {'type': 'PAN', 'target': ('id', p[2]), 'duration': None}
	
def p_camera_action_2_pan_id_dur(p):
	'camera_action : PAN_TO ID duration'
	p[0] = {'type': 'PAN', 'target': ('id', p[2]), 'duration': p[3]}

def p_camera_action_2_zoom(p):
	'''camera_action	: ZOOM IN
						| ZOOM OUT'''
	p[0] = {'type': 'ZOOM', 'target': ('rel', p[2]), 'duration': None}
	
def p_camera_action_2_zoom_dur(p):
	'''camera_action	: ZOOM IN duration
						| ZOOM OUT duration'''
	p[0] = {'type': 'ZOOM', 'target': ('rel', p[2]), 'duration': p[3]}
	
def p_by_amount(p):
	'by_amount : BY NUMBER'
	p[0] = ('number', to_number(p[2]))
	
def p_choice_2_dest(p):
	'''choice : '*' STRING ':' GO destination'''
	p[0] = make_choice(('string', unescape(p[2])), p[5])
	
def p_choice_2_cond_dest(p):
	'''choice : '*' STRING ':' SHOW_IF bool_expression ',' GO destination'''
	p[0] = make_choice(('string', unescape(p[2])), p[8], [], p[5])
	
def p_choice_2_varsets_dest(p):
	'''choice : '*' STRING ':' varsets AND GO destination'''
	p[0] = make_choice(('string', unescape(p[2])), p[7], p[4])
	
def p_choice_2_varsets_cond_dest(p):
	'''choice : '*' STRING ':' SHOW_IF bool_expression ',' varsets AND GO destination'''
	p[0] = make_choice(('string', unescape(p[2])), p[10], p[7], p[5])

def p_varsets_2_expr(p):
	'''varsets	: SET ID inc_dec
				| SET ID expression'''
	p[0] = [ {'name': ('id', p[2]), 'value': p[3]} ]

def p_varsets_2_varsets_and_expr(p):
	'''varsets	: varsets AND SET ID inc_dec
				| varsets AND SET ID expression'''
	p[0] = [ {'name': ('id', p[4]), 'value': p[5]} ] + p[1]
	
def p_id_or_all_2_id(p):
	'id_or_all : ID'
	p[0] = ('id', p[1])
	
def p_id_or_all_2_all(p):
	'id_or_all : ALL'
	p[0] = ('rel', p[1])
	
def p_id_list_2_id(p):
	'id_list : ID'
	p[0] = [ ('id', p[1]) ]
	
def p_id_list_2_id_list_and_id(p):
	'id_list : id_list AND ID'
	p[0] = p[1] + [ ('id', p[3]) ]
	
def p_error(p):
	parser.successful = False
	if not p:
		parser.error_messages.append(": unexpected end-of-file")
	else:
		t = None
		v = None
		if p.type == "STRING":
			t = "string"
			v = unescape(p.value)
		elif p.type == "BARE_EXPRESSION":
			t = "quoted expression"
			v = unescape(p.value)
		elif p.type == "ID":
			t = "identifier"
			v = p.value
		if t is not None:
			problem = "unexpected " + t + " \"" + v + "\""
		else:
			problem = "unexpected " + p.value
		parser.error_messages.append(":" + str(p.lineno) + ": " + problem)
	
def to_number(s):
	if '.' in s:
		return float(s)
	else:
		return int(s)
		
def unescape(s):
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
	
def make_annotation(instruction, **kwargs):
	ann = {'type': 'annotation', 'instruction': instruction}
	for k in kwargs:
		ann[k] = kwargs[k]
	return ann
	
def make_directive(instruction, **kwargs):
	dir = {'type': 'directive', 'instruction': instruction}
	for k in kwargs:
		dir[k] = kwargs[k]
	return dir
	
def make_line(speaker, line, states=None):
	if states is None:
		states = []
	return {'type': 'line', 'speaker': speaker, 'text': line, 'states': states}

def make_choice(text, jump_target, varsets=None, condition=None):
	if varsets is None:
		varsets = []
	return {'text': text, 'target': jump_target, 'sets': varsets, 'condition': condition}
	
parser = yacc.yacc()
parser.error_messages = []
