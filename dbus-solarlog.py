#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  solarlog_modbusquery - Read only query of the Solarlog PV Datalogger using TCP/IP modbus protocol
#  Copyright (C) 2022 Christian Stehle
#  Based on the work of Kilian Knoll https://github.com/kaeferfreund/dbus-kostal
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#  Please note that any incorrect or careless usage of this module as well as errors in the implementation can damage your Inverter!
#  Therefore, the author does not provide any guarantee or warranty concerning to correctness, functionality or performance and does not accept any liability for damage caused by this module, examples or mentioned information.
#  Thus, use it at your own risk!
#
#
#  Purpose:
#           Query values from Solarlog Datalogger
#           Used with Solarlog 500
#  Based on the documentation provided by Solarlog:
#           https://www.solar-log.com/data_sheets/datasheets/de_DE/Komponenten/Kommunikation/SolarLog_Datasheet_Modbus_TCP_Free_DE.pdf
#
# Requires pymodbus
# Tested with:
#           python 3.5
#           pymodbus 2.10
# Please change the IP address of your Solarlog Box (e.g. 192.168.178.41) to suite your environment - see below)
#
import pymodbus
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from vedbus import VeDbusService
from dbus.mainloop.glib import DBusGMainLoop
try:
    import gobject  # Python 2.x
except:
    from gi.repository import GLib as gobject  # Python 3.x
import dbus
import dbus.service
import sys
import os
import platform

# our own packages
sys.path.insert(1, os.path.join(os.path.dirname(
    __file__), '/opt/victronenergy/dbus-modem'))

# Again not all of these needed this is just duplicating the Victron code.


class SystemBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SYSTEM)


class SessionBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SESSION)


def dbusconnection():
    return SessionBus() if 'DBUS_SESSION_BUS_ADDRESS' in os.environ else SystemBus()


powerAC = 0.0
currentL1 = 0.0
currentL2 = 0.0
currentL3 = 0.0
voltageL1 = 0.0
voltageL2 = 0.0
voltageL3 = 0.0
powerPV = 0.0

# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
DBusGMainLoop(set_as_default=True)


class solarlog_modbusquery:
    def __init__(self):
        #Change the IP address and port to suite your environment:
        self.inverter_ip="192.168.0.2"
        self.inverter_port="502"
        #No more changes required beyond this point
        self.SolarlogRegister = []
        self.Adr3502=[]
        self.Adr3502=[3502]
        self.Adr3502.append("PAC")
        self.Adr3502.append("Float")
        self.Adr3502.append(0)

        self.Adr3506=[]
        self.Adr3506=[3506]
        self.Adr3506.append("UAC")
        self.Adr3506.append("Float")
        self.Adr3506.append(0)

        self.Adr3516=[]
        self.Adr3516=[3516]
        self.Adr3516.append("Total yield")
        self.Adr3516.append("Float")
        self.Adr3516.append(0)

    # -----------------------------------------
    # Routine to read a string from one address with 8 registers
    def ReadStr8(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 8, unit=71)
        STRG8Register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big)
        result_STRG8Register = STRG8Register.decode_string(8)
        return(result_STRG8Register)
    # -----------------------------------------
    # Routine to read a Float from one address with 2 registers

    def ReadFloat(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 2, unit=1)
        FloatRegister = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_FloatRegister = round(FloatRegister.decode_32bit_float(), 2)
        return(result_FloatRegister)
    # -----------------------------------------
    # Routine to read a U16 from one address with 1 register

    def ReadU16_1(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 1, unit=1)
        U16register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_U16register = U16register.decode_16bit_uint()
        return(result_U16register)
    # -----------------------------------------
    # Routine to read a U16 from one address with 2 registers

    def ReadU16_2(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 2, unit=1)
        U16register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_U16register = U16register.decode_16bit_uint()
        return(result_U16register)
    # -----------------------------------------
    # Routine to read a U32 from one address with 2 registers

    def ReadU32(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 8, unit=1)
        U32register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_U32register = U32register.decode_32bit_uint()
        return(result_U32register)
    # -----------------------------------------
    # Routine to read a U32 from one address with 2 registers

    def ReadS16(self, myadr_dec):
        r1 = self.client.read_holding_registers(myadr_dec, 1, unit=1)
        S16register = BinaryPayloadDecoder.fromRegisters(
            r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        result_S16register = S16register.decode_16bit_uint()
        return(result_S16register)

    try:
        def run(self):

            self.client = ModbusTcpClient(
                self.inverter_ip, port=self.inverter_port)
            self.client.connect()

            # LONG List of reads...
            self.Adr3502[3] = self.ReadU32(self.Adr3502[0])
            self.Adr3506[3] = self.ReadU16_1(self.Adr3506[0])
            self.Adr3516[3] = self.ReadU32(self.Adr3516[0])

            self.SolarlogRegister = []
            self.SolarlogRegister.append(self.Adr3502)
            self.SolarlogRegister.append(self.Adr3506)
            self.SolarlogRegister.append(self.Adr3516)

            self.client.close()
            
            #pv inverter          
            
            dbusservice['pvinverter.pv0']['/Ac/Current'] = round(self.Adr3502[3]/self.Adr3506[3],2)
            dbusservice['pvinverter.pv0']['/Ac/L1/Current'] = round(self.Adr3502[3]/self.Adr3506[3],2)
            dbusservice['pvinverter.pv0']['/Ac/L1/Voltage'] = self.Adr3506[3]
            dbusservice['pvinverter.pv0']['/Ac/Power'] = self.Adr3502[3]
            dbusservice['pvinverter.pv0']['/Ac/L1/Power'] = self.Adr3502[3]
            dbusservice['pvinverter.pv0']['/Ac/Energy/Forward'] = self.Adr3516[3]/1000.0
            dbusservice['pvinverter.pv0']['/Ac/L1/Energy/Forward'] = self.Adr3516[3]/1000.0
           
    except Exception as ex:
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXX- Hit the following error :From subroutine solarlog_modbusquery :", ex)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# -----------------------------


# Here is the bit you need to create multiple new services - try as much as possible to implement the Victron Dbus API requirements.


def new_service(base, type, physical, id, instance):
    self = VeDbusService("{}.{}.{}_id{:02d}".format(
        base, type, physical,  id), dbusconnection())

    # Create the management objects, as specified in the ccgx dbus-api document
    self.add_path('/Mgmt/ProcessName', __file__)
    self.add_path('/Mgmt/ProcessVersion',
                  'Unkown version, and running on Python ' + platform.python_version())
    self.add_path('/Connected', 1)
    self.add_path('/HardwareVersion', 0)

    def _kwh(p, v): return (str(v) + 'kWh')
    def _a(p, v): return (str(v) + 'A')
    def _w(p, v): return (str(v) + 'W')
    def _v(p, v): return (str(v) + 'V')
    def _c(p, v): return (str(v) + 'C')

 # Create device type specific objects

    if physical == 'pvinverter':
        self.add_path('/DeviceInstance', instance)
        self.add_path('/FirmwareVersion', "1234")
        # value used in ac_sensor_bridge.cpp of dbus-cgwacs
        self.add_path('/ProductId', 1234)
        self.add_path(
            '/ProductName', "Solarlog")
        self.add_path('/Ac/Energy/Forward', None, gettextcallback=_kwh)
        self.add_path('/Ac/L1/Energy/Forward', None, gettextcallback=_kwh)
        self.add_path('/Ac/Power', None, gettextcallback=_w)
        self.add_path('/Ac/Current', None, gettextcallback=_a)
        self.add_path('/Ac/L1/Current', None, gettextcallback=_a)
        self.add_path('/Ac/L1/Power', None, gettextcallback=_w)
        self.add_path('/Ac/L1/Voltage', None, gettextcallback=_v)
        self.add_path('/Ac/MaxPower', None, gettextcallback=_w)
        self.add_path('/ErrorCode', None)
        self.add_path('/Position', 0)
        self.add_path('/StatusCode', None)
    return self


def _update():
    try:
        Solarlogvalues = []
        Solarlogquery = solarlog_modbusquery()
        Solarlogquery.run()
    except Exception as ex:
        print("Issues querying Solarlog -ERROR :", ex)

    return True


dbusservice = {}  # Dictonary to hold the multiple services

base = 'com.victronenergy'

# service defined by (base*, type*, id*, instance):
# * items are include in service name
# Create all the dbus-services we want
dbusservice['pvinverter.pv0'] = new_service(
    base, 'pvinverter.pv0', 'pvinverter',        0, 20)

# Everything done so just set a time to run an update function to update the data values every 5 seconds. Solarlog refreshes only after 20 seconds
gobject.timeout_add(5000, _update)


print("Connected to dbus, and switching over to gobject.MainLoop() (= event based)")
mainloop = gobject.MainLoop()
mainloop.run()

if __name__ == "__main__":
    try:

        Solarlogquery = solarlog_modbusquery()
        Solarlogquery.run()
    except Exception as ex:
        print("Issues querying Solarlog -ERROR :", ex)
