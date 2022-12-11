import pickle

from tkinter.messagebox import showerror

from bin.vectorize_qr import Point
from bin.machinify_vector import ToolList, EngraveParams


class Persistence:
    _pathname = '../assets/'
    _filename = 'persistence.dat'
    _tool_list = ToolList()
    _z_params = EngraveParams()
    _xy0 = Point()
    _has_loaded = False

    @classmethod
    def save(cls, data):
        if type(data) == ToolList:
            cls._tool_list = data
        elif type(data) == EngraveParams:
            cls._z_params = data
        elif type(data) == Point:
            cls._xy0 = data
        else:
            raise ValueError(str(data) + " is no type known to Persistence")

        with open(cls._pathname + cls._filename, 'wb') as file:
            pickle.dump([cls._tool_list,
                         cls._z_params,
                         cls._xy0],
                        file, protocol=2)

    @classmethod
    def load(cls, data):
        if not cls._has_loaded:
            try:
                with open(cls._pathname + cls._filename, 'rb') as file:
                    cls._tool_list, \
                        cls._z_params, \
                        cls._xy0 \
                        = pickle.load(file)
            except FileNotFoundError:
                showerror(title='Database file not found', message='Could not locate saved data under'
                                                                   + cls._pathname + cls._filename + '. \n' +
                                                                   'Starting with a blank database...')
                pass
            cls._has_loaded = True

        if type(data) == ToolList:
            return cls._tool_list
        elif type(data) == EngraveParams:
            return cls._z_params
        elif type(data) == Point:
            return cls._xy0
        else:
            raise ValueError(str(data) + " is no type known to Persistence")
