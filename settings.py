## File contains all settings for 
## Bloodytrinkets
## 

import datetime

simc_build = "43201b2"

#
graph_colours = [
  "#4572a7", 
]

output_screen = False
# "json", "highchart"
output_types = ["json", "highchart"]

simc_settings = {}
simc_settings["simc"]         = "../simc.exe"
simc_settings["fight_styles"] = ["patchwerk", "helterskelter"]
simc_settings["iterations"]   = "250000"
simc_settings["target_error"] = "0.08"
simc_settings["threads"]      = ""
simc_settings["tier"]         = "T20M"

graph_title = "Shaman - Elemental - Patchwerk"
graph_subtitle = "UTC " + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " SimC build: " + simc_build
simc_settings["class"] = "shaman"
simc_settings["spec"]  = "elemental"


# You want to use a custom profile? Set c_profile to True and add a relative 
# path and name
simc_settings["c_profile"]      = False
simc_settings["c_profile_path"] = "example_dir/"
simc_settings["c_profile_name"] = "example_name.simc"

simc_settings["ptr"] = False
