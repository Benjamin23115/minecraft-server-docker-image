########################################################
############## Build Stage #############################
########################################################
FROM eclipse-temurin:22-jre AS build

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install pip packages
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4

# Set working directory
WORKDIR /opt/minecraft

# Copy all Python scripts from your local directory to the Docker image
COPY *.py ./

# Make scripts executable
RUN chmod +x *.py
RUN chmod +x .sh

# Run getPaperServer.py to download Paper with API
RUN python3 /opt/minecraft/getPaperServer.py

########################################################
############## Runtime Stage ############################
########################################################
FROM eclipse-temurin:22-jre AS runtime
ARG TARGETARCH

# Set working directory
WORKDIR /data

# Copy built jar from the build stage
COPY --from=build /opt/minecraft/minecraftspigot.jar /opt/minecraft/paperspigot.jar

# Copy Python scripts for plugins from the build stage
COPY --from=build /opt/minecraft/getGitHubPlugins.py /opt/minecraft/
COPY --from=build /opt/minecraft/getPlugins.py /opt/minecraft/

# Copy Shell start script
COPY --from=build /opt/minecraft/startScript.sh /opt/minecraft/

# Install rcon-cli
ARG RCON_CLI_VER=1.6.7
ADD https://github.com/itzg/rcon-cli/releases/download/${RCON_CLI_VER}/rcon-cli_${RCON_CLI_VER}_linux_${TARGETARCH}.tar.gz /tmp/rcon-cli.tgz
RUN tar -x -C /usr/local/bin -f /tmp/rcon-cli.tgz rcon-cli && \
    rm /tmp/rcon-cli.tgz

# Define volumes for external data (Server, World, Config...)
VOLUME "/data"

# Expose Minecraft ports
EXPOSE 25565/tcp
EXPOSE 25565/udp
EXPOSE 19132/tcp
EXPOSE 19132/udp

# Set working directory
WORKDIR /data

#Xms: Initial memory allocation pool size
#Xmx: Maximum memory allocation pool size
# -Dcom.mojang.eula.agree=true: Automtically accept EULA
CMD ["./opt/minecraft/startScript.sh"]
