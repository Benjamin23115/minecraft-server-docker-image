########################################################
############## Build Stage #############################
########################################################
FROM eclipse-temurin:23-jre AS build

# Set working directory
WORKDIR /opt/minecraft

# Copy all scripts from your local directory to the Docker image
COPY *.py ./
COPY *.sh ./

# Make scripts executable
RUN chmod +x *.py

########################################################
############## Runtime Stage ############################
########################################################
FROM eclipse-temurin:23-jre AS runtime
ARG TARGETARCH

# Install Python and pip in the runtime image
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-requests \
    python3-bs4 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /data

# Copy Python scripts for plugins from the build stage
COPY --from=build /opt/minecraft/*.py /opt/minecraft/

# Copy Shell start scripts from the build stage
COPY --from=build /opt/minecraft/*.sh /opt/minecraft/

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

CMD ["/opt/minecraft/startScript.sh"]
