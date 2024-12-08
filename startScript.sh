# Run Python scripts to get plugins and Paper server
python3 /opt/minecraft/getPlugins.py
python3 /opt/minecraft/getPaperServer.py
# Ensure the JAR file has the correct permissions
chmod +rwx *.jar

# Run the Java command with the full path to the JAR file
java -Dcom.mojang.eula.agree=true -Xms1G -Xmx6G -jar ./minecraftspigot.jar
