# dbus-solarlog Service
Victron Venus OS Modbus Driver for Solarlog PV Logger

### Purpose

This service is meant to be run on a Venus OS Device (Multiplus-II GX, Cerbo GX,...) from Victron.

The Python script cyclically reads the total PV-Power (PAC) from the Solarlog Datalogger (Minimum Firmware 2.8.1 Build 49) and publishes information on the dbus as single PV Inverter, using the service name pvinverter.pv0. This makes the Venus OS work as if you had a physical PV Inverter installed. 

### Configuration

In the Python file, you must put the IP of your Solarlog device.

### Installation

1. Copy the files to the /data folder on your venus:

   - /data/dbus-solarlog/dbus-solarlog.py
   - /data/dbus-solarlog/kill_me.sh
   - /data/dbus-solarlog/install.sh
   - /data/dbus-solarlog/service/run

2. Set permissions for files:

   `chmod 755 /data/dbus-solarlog/install.sh`
   
3. Get two files from the [velib_python](https://github.com/victronenergy/velib_python) and install them on your venus:

   - /data/dbus-solarlog/vedbus.py
   - /data/dbus-solarlog/ve_utils.py

4. Run install-script

   /data/dbus-solarlog/install.sh

   The install-script sets the proper rights and enables the script as a service. It also adds the script to /data/rc.local, so this service should be reboot- and update-safe. The daemon-tools should automatically start this service within seconds and you should see the device "Solarlog" in your Venus OS Device list.
   
5. Remove Driver

   - rm /service/dbus-solarlog
   - clean up or remove /data/rc.local

### Debugging

You can check the status of the service with svstat:

`svstat /service/dbus-solarlog`

It will show something like this:

`/service/dbus-solarlog: up (pid 10078) 325 seconds`

If the number of seconds is always 0 or 1 or any other small number, it means that the service crashes and gets restarted all the time.

When you think that the script crashes, start it directly from the command line:

`python /data/dbus-solarlog/dbus-solarlog.py`

and see if it throws any error messages.

If the script stops with the message

`dbus.exceptions.NameExistsException: Bus name already exists: com.victronenergy.grid"`

it means that the service is still running or another service is using that bus name.

#### Restart the script

If you want to restart the script, for example after changing it, just run the following command:

`/data/dbus-solarlog/kill_me.sh`

The daemon-tools will restart the scriptwithin a few seconds.

### Hardware

In my installation at home, I am using the following Hardware:

- Solarlog 500 Datalogger
- Victron MultiPlus-II GX - Battery Inverter (single phase)
- EM24 Ethernet Grid Logger
- Pylontech US3000C - LiFePO Battery

### Credits 🙌🏻

This project is build upon the basis of the inspirational work of:

- RalfZim via GitHub https://github.com/RalfZim
- Kaeferfreund via GitHub https://github.com/kaeferfreund/dbus-kostal
- Fabian Lauer via GitHub https://github.com/fabian-lauer/dbus-shelly-3em-smartmeter


