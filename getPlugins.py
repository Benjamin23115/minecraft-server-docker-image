import os
import requests
from getGitHubPlugins import getLatestJarURL

# Function to download plugin
def download_plugin(plugin_name, download_url):
    print("-----------------")
    print(f"Downloading {plugin_name} from {download_url}")
    print("-----------------")

    response = requests.get(download_url)
    if response.status_code == 200:
        with open(f"{plugin_name}.jar", 'wb') as f:
            f.write(response.content)
        print(f"Download of {plugin_name} successful.")
    else:
        print(f"Failed to download {plugin_name}.")

# Make folder "plugins" to store all of the downloaded plugins
os.makedirs("plugins", exist_ok=True)
os.chdir("plugins")

# EssentialsX for useful commands
# Indices of plugins in the Jenkins API response
indices = [0, 2, 7]

# EssentialsX plugin URL
ESSENTIALSX_URL = "https://ci.ender.zone/job/EssentialsX/lastSuccessfulBuild/artifact/jars/"

# Loop through the indices array
for index in indices:
    # Get the plugin name using the index
    if index == 0:
        plugin_name = "EssentialsX"
    elif index == 2:
        plugin_name = "EssentialsXChat"
    elif index == 7:
        plugin_name = "EssentialsXSpawn"

    # Get the plugin download URL
    response = requests.get("https://ci-api.essentialsx.net/job/EssentialsX/lastSuccessfulBuild/api/json")
    if response.status_code == 200:
        json_data = response.json()
        ESSENTIALSX_PLUGIN_NAME = json_data['artifacts'][index]['displayPath'].strip('"')
        download_plugin(plugin_name, f"{ESSENTIALSX_URL}{ESSENTIALSX_PLUGIN_NAME}")

# ViaBackwards + Version for cross-version compatibility
viaBackwardsURL = "https://github.com/ViaVersion/ViaBackwards/releases/latest"
viaBackwardsDownloadURL = "https://github.com/ViaVersion/ViaBackwards/releases"
download_plugin("viaVersion", getLatestJarURL(viaBackwardsURL, viaBackwardsDownloadURL, "viaBackwards-{text}.jar"))

viaVersionURL = "https://github.com/ViaVersion/ViaVersion/releases/latest"
viaVersionDownloadURL = "https://github.com/ViaVersion/ViaVersion/releases"
download_plugin("viaVersion", getLatestJarURL(viaVersionURL, viaVersionDownloadURL, "viaVersion-{text}.jar"))

# LuckPerms to handle permissions

luckPermsURL = "https://metadata.luckperms.net/data/all"
try:
    response = requests.get(luckPermsURL)
    response.raise_for_status()
    data = response.json()
    bukkitURL = data.get('downloads', {}).get('bukkit')
    download_plugin("LuckPerms", bukkitURL)
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    
# Right Click Harvest for QOL farming
RIGHT_CLICK_HARVEST_DOWNLOAD_URL = "https://dev.bukkit.org/projects/rightclickharvest/files/latest"
download_plugin("rightClickHarvest", RIGHT_CLICK_HARVEST_DOWNLOAD_URL)

# Sleep Most for QOL day-night cycles
SLEEP_MOST_DOWNLOAD_URL = "https://www.spigotmc.org/resources/sleep-most-1-8-1-20-x-the-most-advanced-sleep-plugin-available-percentage-animations.60623/download?version=528694"
download_plugin("sleepMost", SLEEP_MOST_DOWNLOAD_URL)

# Cristichi's Tree Capitator for QOL Tree chopping
CRIS_TREE_CAPITATOR_DOWNLOAD_URL = "https://dev.bukkit.org/projects/cristichis-tree-capitator/files/latest"
download_plugin("cris-tree-capitator", CRIS_TREE_CAPITATOR_DOWNLOAD_URL)

# Instant Restock for QOL Villager Trading
instantRestockURL = "https://github.com/spartacus04/InstantRestock/releases/latest"
instantRestockDownloadURL = "https://github.com/spartacus04/InstantRestock/releases"

download_plugin("instantRestock", getLatestJarURL(instantRestockURL, instantRestockDownloadURL, "InstantRestock-{text}.jar"))