# File for handling all Highcharts

import datetime
# Library to look for files and create them if needed
import settings
import lib.simc_support.wow_lib as wow_lib

# cruweight^128826^190462^2.5^252191^2.75^190567^0^252207^0^252091^3.25^238052^2.75^190514^0^253111^0^ilvl^1^252875^3.75^190529^3.1^190449^2^190520^0.7^252922^1.75^190457^0.7^190503^0^190467^0.1^253093^3.5^252906^4^253070^3.75^252888^3.25^252799^3.75^252088^3.25^end

##
## @brief      Generates crucible weigths strings.
##
## @param      crucibles_list  The normalised crucible dictionary {type s:{name
##                             s:{dps s}}}
## @param      filename        The filename
##
## @return     True if writing to file was successfull
##
def print_crucibles( crucibles_list, filename ):


  crucible_string = "cruweight^"
  crucible_string += wow_lib.get_weapon_id( settings.simc_settings[ "class" ], settings.simc_settings[ "spec" ] ) + "^"

  for cr_type in crucibles_list:
    for crucible in crucibles_list[ cr_type ]:
      cr_id = False
      cr_value = "0"
      # check for itemlevel values
      if "itemlevel" in crucible:
        # add itemlevel value only once (from +1)
        if "+1" in crucible:
          cr_id = "ilvl"
        else:
          cr_id = False
      else:
        # get id of trait
        cr_id = wow_lib.get_crucible_spell_id( settings.simc_settings[ "class" ], settings.simc_settings[ "spec" ], crucible )

      if cr_id:
        cr_value = crucibles_list[ cr_type ][ crucible ]
        crucible_string += cr_id + "^" + cr_value + "^"

  crucible_string += "end"


  # write raw file
  with open(filename + "_weight.html", "w") as ofile:
    ofile.write(crucible_string)

  return True
