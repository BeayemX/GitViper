from gitviper.colors import string_to_color

class Task:
    # default parameters do not work because these values
    # will be parsed from config file and 'None' will be forwarded
    def __init__(self, representation, task_configuration_obj):
        value = task_configuration_obj.get('key')
        color = task_configuration_obj.get('color')
        priority = task_configuration_obj.get('priority')
        font_color = task_configuration_obj.get('font_color')
        bold = task_configuration_obj.get('bold')
        row = task_configuration_obj.get('row')

        if not value:
            value = representation

        self.representation = representation
        self.value = value if value != None else representation
        self.priority = priority if priority != None else 0 # priorities below 1 will be displayed in the second line
        self.row = row if row != None else 0

        # prepare local variables for string to color-class conversion
        color = color if color != None else "white"
        bgcolor = "bg_" + color

        # get font color
        # used in TaskList when displayed as normal text
        self.color = string_to_color(color)

        # TODO rename, because bg color is not quite correct?
        # calculate bgcolor
        # used in Overview as Task-tag-item
        self.bgcolor = ""

        if bold:
            self.bgcolor += string_to_color("bold")
        if font_color:
            self.bgcolor += string_to_color(font_color)

        self.bgcolor += string_to_color(bgcolor)
