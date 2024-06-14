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

# Make scripts executable (if needed)
RUN chmod +x *.py

# Run getPaperServer.py to download Paper with API
RUN python3 /opt/minecraft/getPaperServer.py

# Run getPlugins.py to download plugins
RUN python3 /opt/minecraft/getPlugins.py

########################################################
############## Runtime Stage ############################
########################################################
FROM eclipse-temurin:22-jre AS runtime
ARG TARGETARCH

# Set working directory
WORKDIR /data

# Copy built jar from the build stage
COPY --from=build /opt/minecraft/minecraftspigot.jar /opt/minecraft/paperspigot.jar

# Copy plugin jars from the build stage
COPY --from=build /opt/minecraft/plugins/*.jar /data/plugins/

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
CMD ["java", "-Xms1G", "-Xmx6G", "-Dcom.mojang.eula.agree=true" "-jar", "/opt/minecraft/paperspigot.jar"]