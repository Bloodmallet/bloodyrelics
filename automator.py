import datetime
import subprocess
import sys

simc_build = "43201b2"

fight_styles = [ 
  ( "patchwerk", "0.08" ), 
  ( "beastlord", "0.2" ) 
]

profiles = [
  #( "death_knight", "blood",         ),
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
  #( "monk",         "brewmaster",    ),
  ( "monk",         "windwalker",    ),
  #( "paladin",      "protection",    ),
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


start = datetime.datetime.utcnow()

for fight_style in fight_styles:
  for profile in profiles:
    with open("automator_input.py", "w") as ofile:
      ofile.write("graph_title = \"" + profile[0].title() + " - " + profile[1].title() + " - " + fight_style[0].title() + "\"\n")
      ofile.write("graph_subtitle = \"UTC " + start.strftime("%Y-%m-%d %H:%M") + " SimC build: " + simc_build + "\"\n")
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
# simc_settings["class"] = automator_input.simc_settings["class"]
# simc_settings["spec"]  = automator_input.simc_settings["spec"]
# simc_settings["fight_styles"] = automator_input.simc_settings["fight_styles"]
# simc_settings["target_error"] = automator_input.simc_settings["target_error"]
