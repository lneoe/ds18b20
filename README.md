#DS18B20 temperature sensor with python


##Run on Raspberry Pi
    I runing this with Archlinux

###I Used Systemd/Timers
#### ds18b20.timer

    [Unit]
    Description=Run ds18b20 for temperature

	[Timer]
	OnBootSec=1min
	OnUnitActiveSec=1min

	[Install]
	WantedBy=timers.target

####ds18b20.service

	[Unit]
	Description=Run ds18b20 sensor

	[Service]
	User=your-username
	ExecStart=/usr/bin/env/python2 /your-path/temperature.py

#### Start ds18b20
**start ds18b20**

	systemctl start ds18b20

**start on system boot**

	systemctl enable ds18b20



