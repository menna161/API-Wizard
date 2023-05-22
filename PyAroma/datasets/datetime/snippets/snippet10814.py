from enum import IntEnum, unique
from threading import Timer
import binascii
import logging
import queue
import socket
import time
import serial
import datetime
from .web import WebServer
from .states import States
from .keys import Keys


def process(self, data_changed_callback):
    'Process data; returns when the reader signals EOF.\n        Callback is notified when any data changes.'
    try:
        while True:
            byte = self._read()
            frame_start_time = None
            frame_rx_time = datetime.datetime.now()
            while True:
                if (byte == self.FRAME_DLE):
                    frame_start_time = time.monotonic()
                    next_byte = self._read()
                    if (next_byte == self.FRAME_STX):
                        break
                    else:
                        continue
                byte = self._read()
                elapsed = (datetime.datetime.now() - frame_rx_time)
                if (elapsed.seconds > self.READ_TIMEOUT):
                    _LOGGER.info('Frame timeout')
                    return
            frame = bytearray()
            byte = self._read()
            while True:
                if (byte == self.FRAME_DLE):
                    next_byte = self._read()
                    if (next_byte == self.FRAME_ETX):
                        break
                    elif (next_byte != 0):
                        pass
                frame.append(byte)
                byte = self._read()
            frame_crc = int.from_bytes(frame[(- 2):], byteorder='big')
            frame = frame[:(- 2)]
            calculated_crc = (self.FRAME_DLE + self.FRAME_STX)
            for byte in frame:
                calculated_crc += byte
            if (frame_crc != calculated_crc):
                _LOGGER.warning('Bad CRC')
                continue
            frame_type = frame[0:2]
            frame = frame[2:]
            if (frame_type == self.FRAME_TYPE_KEEP_ALIVE):
                if (not self._send_queue.empty()):
                    self._send_frame()
                continue
            elif (frame_type == self.FRAME_TYPE_LOCAL_WIRED_KEY_EVENT):
                _LOGGER.debug('%3.3f: Local Wired Key: %s', frame_start_time, binascii.hexlify(frame))
            elif (frame_type == self.FRAME_TYPE_REMOTE_WIRED_KEY_EVENT):
                _LOGGER.debug('%3.3f: Remote Wired Key: %s', frame_start_time, binascii.hexlify(frame))
            elif (frame_type == self.FRAME_TYPE_WIRELESS_KEY_EVENT):
                _LOGGER.debug('%3.3f: Wireless Key: %s', frame_start_time, binascii.hexlify(frame))
            elif (frame_type == self.FRAME_TYPE_LEDS):
                states = int.from_bytes(frame[0:4], byteorder='little')
                flashing_states = int.from_bytes(frame[4:8], byteorder='little')
                states |= flashing_states
                if self._heater_auto_mode:
                    states |= States.HEATER_AUTO_MODE
                if ((states != self._states) or (flashing_states != self._flashing_states)):
                    self._states = states
                    self._flashing_states = flashing_states
                    data_changed_callback(self)
            elif (frame_type == self.FRAME_TYPE_PUMP_SPEED_REQUEST):
                value = int.from_bytes(frame[0:2], byteorder='big')
                _LOGGER.debug('%3.3f: Pump speed request: %d%%', frame_start_time, value)
                if (self._pump_speed != value):
                    self._pump_speed = value
                    data_changed_callback(self)
            elif ((frame_type == self.FRAME_TYPE_PUMP_STATUS) and (len(frame) >= 5)):
                self._multi_speed_pump = True
                speed = frame[2]
                power = ((((((frame[3] & 240) >> 4) * 1000) + ((frame[3] & 15) * 100)) + (((frame[4] & 240) >> 4) * 10)) + (frame[4] & 15))
                _LOGGER.debug('%3.3f; Pump speed: %d%%, power: %d watts', frame_start_time, speed, power)
                if (self._pump_power != power):
                    self._pump_power = power
                    data_changed_callback(self)
            elif (frame_type == self.FRAME_TYPE_DISPLAY_UPDATE):
                text = frame.replace(b'\xdf', b'\xc2\xb0').decode('utf-8')
                parts = text.split()
                _LOGGER.debug('%3.3f: Display update: %s', frame_start_time, parts)
                self._web.text_updated(text)
                try:
                    if ((parts[0] == 'Pool') and (parts[1] == 'Temp')):
                        value = int(parts[2][:(- 2)])
                        if (self._pool_temp != value):
                            self._pool_temp = value
                            self._is_metric = (parts[2][(- 1):] == 'C')
                            data_changed_callback(self)
                    elif ((parts[0] == 'Spa') and (parts[1] == 'Temp')):
                        value = int(parts[2][:(- 2)])
                        if (self._spa_temp != value):
                            self._spa_temp = value
                            self._is_metric = (parts[2][(- 1):] == 'C')
                            data_changed_callback(self)
                    elif ((parts[0] == 'Air') and (parts[1] == 'Temp')):
                        value = int(parts[2][:(- 2)])
                        if (self._air_temp != value):
                            self._air_temp = value
                            self._is_metric = (parts[2][(- 1):] == 'C')
                            data_changed_callback(self)
                    elif ((parts[0] == 'Pool') and (parts[1] == 'Chlorinator')):
                        value = int(parts[2][:(- 1)])
                        if (self._pool_chlorinator != value):
                            self._pool_chlorinator = value
                            data_changed_callback(self)
                    elif ((parts[0] == 'Spa') and (parts[1] == 'Chlorinator')):
                        value = int(parts[2][:(- 1)])
                        if (self._spa_chlorinator != value):
                            self._spa_chlorinator = value
                            data_changed_callback(self)
                    elif ((parts[0] == 'Salt') and (parts[1] == 'Level')):
                        value = float(parts[2])
                        if (self._salt_level != value):
                            self._salt_level = value
                            self._is_metric = (parts[3] == 'g/L')
                            data_changed_callback(self)
                    elif ((parts[0] == 'Check') and (parts[1] == 'System')):
                        value = ' '.join(parts[2:])
                        if (self._check_system_msg != value):
                            self._check_system_msg = value
                            data_changed_callback(self)
                    elif (parts[0] == 'Heater1'):
                        self._heater_auto_mode = (parts[1] == 'Auto')
                except ValueError:
                    pass
            elif (frame_type == self.FRAME_TYPE_LONG_DISPLAY_UPDATE):
                pass
            else:
                _LOGGER.debug('%3.3f: Unknown frame: %s %s', frame_start_time, binascii.hexlify(frame_type), binascii.hexlify(frame))
    except socket.timeout:
        _LOGGER.info('socket timeout')
    except serial.SerialTimeoutException:
        _LOGGER.info('serial timeout')
    except EOFError:
        _LOGGER.info('eof')
