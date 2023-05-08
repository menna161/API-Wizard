from datetime import datetime
import re
import string


def encode(self, encoding):
    output = [('%s=%s' % (self.key, _quote(self.value)))]
    for (key, value) in self.items():
        if ((key == 'max-age') and isinstance(value, int)):
            output.append(('%s=%d' % (self._keys[key], value)))
        elif ((key == 'expires') and isinstance(value, datetime)):
            output.append(('%s=%s' % (self._keys[key], value.strftime('%a, %d-%b-%Y %T GMT'))))
        elif (key in self._flags):
            output.append(self._keys[key])
        else:
            output.append(('%s=%s' % (self._keys[key], value)))
    return '; '.join(output).encode(encoding)
