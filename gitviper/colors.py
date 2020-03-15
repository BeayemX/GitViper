import re

BLACK	= "\033[30m"
RED		= "\033[31m"
GREEN	= "\033[32m"
YELLOW	= "\033[33m"
BLUE	= "\033[34m"
MAGENTA	= "\033[35m"
CYAN	= "\033[36m"
WHITE	= "\033[37m"

BG_BLACK	= "\033[40m"
BG_RED		= "\033[41m"
BG_GREEN	= "\033[42m"
BG_YELLOW	= "\033[43m"
BG_BLUE		= "\033[44m"
BG_MAGENTA	= "\033[45m"
BG_CYAN		= "\033[46m"
BG_WHITE	= "\033[47m"

RESET 			= "\033[0;0m"
BOLD   			= "\033[1m"
FAINT			= '\033[2m'
ITALIC			= '\033[3m'
UNDERLINE		= '\033[4m'
BLINK			= '\033[5m'
INVERSE 		= "\033[7m"
CONCEALED 		= "\033[8m"
STRIKETHROUGH 	= "\033[9m"

# use with caution, these may have chagned
# BOLD_OFF caused double underline...
# BOLD_OFF  		= "\033[21m"
# UNDERLINE_OFF   = "\033[24m"
# INVERSE_OFF     = "\033[27m"

"""
def clear_screen():
	print("\033[2J")

def clear_line():
	print("\033[K", end='', flush=True)

def move_cursor_up(rows=1):
	print("\033["+ str(rows) +"A", sep=' ', end='', flush=True)
"""
def string_to_color(color_as_string):
	if color_as_string == None:
		return None
	return _get_color_from_string(color_as_string.lower()) # TODO use .casefold() instead of lower()?

def _get_color_from_string(color_as_string):
	# TODO use dictionary to return color?
	# i.e. `return color_dict[color_as_string]`
	if color_as_string == "black": return BLACK
	if color_as_string == "white": return WHITE
	if color_as_string == "red": return RED
	if color_as_string == "green": return GREEN
	if color_as_string == "blue": return BLUE
	if color_as_string == "yellow": return YELLOW
	if color_as_string == "magenta": return MAGENTA
	if color_as_string == "cyan": return CYAN

	if color_as_string == "bg_black": return BG_BLACK
	if color_as_string == "bg_white": return BG_WHITE
	if color_as_string == "bg_red": return BG_RED
	if color_as_string == "bg_green": return BG_GREEN
	if color_as_string == "bg_blue": return BG_BLUE
	if color_as_string == "bg_yellow": return BG_YELLOW
	if color_as_string == "bg_magenta": return BG_MAGENTA
	if color_as_string == "bg_cyan": return BG_CYAN

	if color_as_string == "bold": return BOLD

	return None

def remove_color_codes_from_string(text):
	ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
	return ansi_escape.sub('', text)
