import requests
from getLatestPaperVersion import getPaperVersion


def main():
    papermc_version = getPaperVersion()

    # Get the latest build number for the specified PaperMC version
    version_url = f"https://papermc.io/api/v2/projects/paper/versions/{papermc_version}"
    version_response = requests.get(version_url)
    version_data = version_response.json()
    latest_build = version_data['builds'][-1]

    # Get the name of the latest downloadable file for the latest build
    build_url = f"https://papermc.io/api/v2/projects/paper/versions/{papermc_version}/builds/{latest_build}"
    build_response = requests.get(build_url)
    build_data = build_response.json()
    latest_download = build_data['downloads']['application']['name']

    # Construct the download URL for the latest build
    download_url = f"https://papermc.io/api/v2/projects/paper/versions/{papermc_version}/builds/{latest_build}/downloads/{latest_download}"

    # Print the version and build number
    print("-----------------")
    print(f"{papermc_version}#{latest_build}")
    print("-----------------")

    # Download the file
    response = requests.get(download_url)
    with open('minecraftspigot.jar', 'wb') as file:
        file.write(response.content)

if __name__ == "__main__":
    main()
