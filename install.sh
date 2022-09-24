#!/bin/bash

# set permissions for script files
chmod a+x /data/dbus-solarlog/kill_me.sh
chmod 744 /data/dbus-solarlog/kill_me.sh

chmod a+x /data/dbus-solarlog/service/run
chmod 755 /data/dbus-solarlog/service/run



# create sym-link to run script in deamon
ln -s /data/dbus-solarlog/service /service/dbus-solarlog



# add install-script to rc.local to be ready for firmware update
filename=/data/rc.local
if [ ! -f $filename ]
then
    touch $filename
    chmod 755 $filename
    echo "#!/bin/bash" >> $filename
    echo >> $filename
fi

grep -qxF '/data/dbus-solarlog/install.sh' $filename || echo '/data/dbus-solarlog/install.sh' >> $filename
