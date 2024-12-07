#!/bin/sh

python /opt/minecraft/getPlugins.py
java -Dcom.mojang.eula.agree=true -Xms1G -Xmx6G -jar /opt/minecraft/paperspigot.jar