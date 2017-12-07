import datetime
import subprocess
import sys

simc_build = "<a href=\\\"https://github.com/simulationcraft/simc/commit/c56773bf9e4845bb68b68dccb8ce6015ee67375a\\\" target=\\\"blank\\\">c56773b</a>"

fight_styles = [
  ( "patchwerk", "0.08" ),
  ( "beastlord", "0.2" )
]

profiles = [
  ( "death_knight", "blood",         ),
  ( "death_knight", "frost",         ),
  ( "death_knight", "unholy",        ),
  ( "demon_hunter", "havoc",         ),
  #( "demon_hunter", "vengance",      ),
  ( "druid",        "balance",       ),
  ( "druid",        "feral",         ),
  #( "druid",        "guardian",      ),
  ( "hunter",       "beast_mastery", ),
  ( "hunter",       "marksmanship",  ),
  ( "hunter",       "survival",      ),
  ( "mage",         "arcane",        ),
  ( "mage",         "fire",          ),
  ( "mage",         "frost",         ),
  ( "monk",         "brewmaster",    ),
  ( "monk",         "windwalker",    ),
  ( "paladin",      "protection",    ),
  ( "paladin",      "retribution",   ),
  ( "priest",       "shadow",        ),
  ( "rogue",        "assassination", ),
  ( "rogue",        "outlaw",        ),
  ( "rogue",        "subtlety",      ),
  ( "shaman",       "elemental",     ),
  ( "shaman",       "enhancement",   ),
  ( "warlock",      "affliction",    ),
  ( "warlock",      "demonology",    ),
  ( "warlock",      "destruction",   ),
  ( "warrior",      "arms",          ),
  ( "warrior",      "fury",          ),
  #( "warrior",      "protection",    )
]

colours = {
  "death_knight": "#C41F3B",
  "demon_hunter": "#A330C9",
  "druid": "#FF7D0A",
  "hunter": "#ABD473",
  "mage": "#69CCF0",
  "monk": "#00FF96",
  "paladin": "#F58CBA",
  "priest": "#FFFFFF",
  "rogue": "#FFF569",
  "shaman": "#0070DE",
  "warlock": "#9482C9",
  "warrior": "#C79C6E",
}

start = datetime.datetime.utcnow()

for fight_style in fight_styles:
  for profile in profiles:
    with open("automator_input.py", "w") as ofile:
      ofile.write("graph_title = \"" + profile[0].title() + " - " + profile[1].title() + " - " + fight_style[0].title() + "\"\n")
      ofile.write("graph_subtitle = \"UTC " + start.strftime("%Y-%m-%d %H:%M") + " SimC build: " + simc_build + "\"\n")
      ofile.write("graph_colours = [\"" + colours[profile[0]] + "\"]\n")
      ofile.write("simc_settings = {}\n")
      ofile.write("simc_settings[\"class\"] = \"" + profile[0] + "\"\n")
      ofile.write("simc_settings[\"spec\"] = \"" + profile[1] + "\"\n")
      ofile.write("simc_settings[\"fight_styles\"] = [\"" + fight_style[0] + "\"]\n")
      ofile.write("simc_settings[\"target_error\"] = \"" + fight_style[1] + "\"\n")

    print("")

    command = "python bloodyrelics.py"
    if sys.platform == 'win32':
      # call bloodytrinkets in the background
      startupinfo = subprocess.STARTUPINFO()
      startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

      result = subprocess.run(
        command,
        stdout=None,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        startupinfo=startupinfo
      )
      while result.returncode != 0:
        print(result)
        print("I keep trying")
        result = subprocess.run(
          command,
          stdout=None,
          stderr=subprocess.STDOUT,
          universal_newlines=True,
          startupinfo=startupinfo
        )

    else:
      result = subprocess.run(
        command,
        stdout=None,
        stderr=subprocess.STDOUT,
        universal_newlines=True
      )
      while result.returncode != 0:
        result = subprocess.run(
          command,
          stdout=None,
          stderr=subprocess.STDOUT,
          universal_newlines=True
        )
end = datetime.datetime.utcnow()
print( "Done after " + str( end - start ))


## Add this to settings to automate the process
# import automator_input
# graph_title = automator_input.graph_title
# graph_subtitle = automator_input.graph_subtitle
# graph_colours = automator_input.graph_colours
# simc_settings["class"] = automator_input.simc_settings["class"]
# simc_settings["spec"]  = automator_input.simc_settings["spec"]
# simc_settings["fight_styles"] = automator_input.simc_settings["fight_styles"]
# simc_settings["target_error"] = automator_input.simc_settings["target_error"]
