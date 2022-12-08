

class Tool:
    def __init__(self, number, name, dia, fxy, fz, s, angle=0, tip=0):
        self.number = number
        self.name = name
        self.diameter = dia
        self.fxy = fxy
        self.fz = fz
        self.speed = s
        self.angle = angle
        self.tip = tip

    def get_description(self):
        return str(self.number) + '_' + self.name + '_' + str(self.diameter) + 'mm'


class ToolList:
    def __init__(self):
        self.tools = dict()
        self.selected_tool = None

    def add_or_update(self, tool):
        self.tools.update({tool.number: tool})

    def remove(self, key):
        if key in self.tools:
            self.tools.pop(key)

    def select_tool(self, key):
        if key in self.tools:
            self.selected_tool = self.tools.get(key)

    def get_selected_tool(self):
        return self.selected_tool

    def get_tool_list_string(self):
        tools = list(self.tools.values())
        tools_list = list()
        for tool in tools:
            tools_list.append(tool.get_description())
        return tools_list
