import pickle

from tkinter.messagebox import showerror

from bin.machinify_vector import ToolList, EngraveParams


class Persistence:
    _pathname = '../assets/'
    _filename = 'persistence.dat'
    _tool_list = ToolList()
    _z_params = EngraveParams()

    @classmethod
    def save(cls, data):
        if type(data) == ToolList:
            cls._tool_list = data
        elif type(data) == EngraveParams:
            cls._z_params = data
        else:
            raise ValueError(str(data) + " is no type known to Persistence")

        with open(cls._pathname + cls._filename, 'wb') as file:
            pickle.dump([cls._tool_list,
                         cls._z_params],
                        file, protocol=2)

    @classmethod
    def load(cls, data):
        try:
            with open(cls._pathname + cls._filename, 'rb') as file:
                cls._tool_list, \
                    cls._z_params \
                    = pickle.load(file)
        except FileNotFoundError:
            showerror(title='Database file not found', message='Could not locate saved data under'
                                                               + cls._pathname + cls._filename + '. \n' +
                                                               'Starting with a blank database...')
            pass
        
        if type(data) == ToolList:
            return cls._tool_list
        elif type(data) == EngraveParams:
            return cls._z_params
        else:
            raise ValueError(str(data) + " is no type known to Persistence")
