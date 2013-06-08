#-*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| File contributors :                                                       |
#|       - Georges Bossert <georges.bossert (a) supelec.fr>                  |
#|       - Frédéric Guihéry <frederic.guihery (a) amossys.fr>                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports                                                  |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Related third party imports                                               |
#+---------------------------------------------------------------------------+
from functools import wraps

#+---------------------------------------------------------------------------+
#| Local application imports                                                 |
#+---------------------------------------------------------------------------+


def typeCheck(*types):
    """Decorator which reduces the amount of code to type-check attributes.

    Its allows to replace the following code:
    ::
        @id.setter
        def id(self, id):
            if not isinstance(id, uuid.UUID):
               raise TypeError("Invalid types for argument id, must be an UUID")
            self.__id = id

    with:
    ::
        @id.setter
        @typeCheck(uuid.UUID)
        def id(self, id):
           self.__id = id

    .. note:: set type = "SELF" to check the type of the self parameter
    .. warning:: if argument is None, the type checking is not executed on it.

    """
    def _typeCheck_(func):
        def wrapped_f(*args, **kwargs):
            arguments = args[1:]
            if len(arguments) == len(types):
                # Replace "SELF" with args[0] type
                final_types = []
                for type in types:
                    if type == "SELF":
                        final_types.append(args[0].__class__)
                    else:
                        final_types.append(type)

                for i, argument in enumerate(arguments):
                    if argument is not None and not isinstance(argument, final_types[i]):
                        raise TypeError("Invalid types for arguments, expecting: {0}".format(', '.join([t.__name__ for t in final_types])))
            return func(*args, **kwargs)
        return wraps(func)(wrapped_f)
    return _typeCheck_