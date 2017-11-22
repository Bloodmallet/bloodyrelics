## File to manage outputs


## Library needed to get date and calculationtime for program
import lib.output.crucible_weights as crucible_weights
import lib.output.highcharts as highcharts
import lib.output.json_print as json
import settings


##
## @brief      Creates a filename with current date.
##
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
##
## @return     Returns a filename which contains the current date
##
def __create_filename(fight_style):
  filename = "./results/crucible_"
  filename += settings.simc_settings["class"] + "_"
  filename += settings.simc_settings["spec"] + "_"
  filename += fight_style
  if settings.simc_settings["ptr"]:
    filename += "_ptr"
  return filename


##
## @brief      Reduces trinket dps to the actual gain those trinkets provide in
##             comparison to the baseline dps.
##
## @param      base_dps     Dictionary of the base-profile without crucible
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      sim_results  Dictionary of all simmed trinkets with all their dps
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
##
## @return     Dictionary of all simmed trinkets with all their normalised dps
##             values as strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0"
##             if the simmed itemlevel doesn't match available trinket itemlevel
##
def __normalise_crucibles(base_dps, sim_results):
  for trait_type in sim_results:
    for crucible in sim_results[trait_type]:
      if not sim_results[trait_type][crucible] == "0":
        sim_results[trait_type][crucible] = str(int(sim_results[trait_type][crucible]) - int(base_dps["baseline"]))

      if int(sim_results[trait_type][crucible]) < 1000:
        sim_results[trait_type][crucible] = "0"

  return sim_results


##
## @brief      Generates a list ordered by max dps value of highest itemlevel
##             trinkets [trinket_name s]
##
## @param      sim_results  Dictionary of all simmed trinkets with all their dps
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      ilevels      The ilevels list
##
## @return     Trinket list ordered ascending from lowest to highest dps for
##             highest available itemlevel
##
def __order_results(sim_results):
  current_best_dps = "-1"
  last_best_dps = "-1"
  name = ""
  crucible_list = []
  # gets highest dps value of all trinkets
  for trait_type in sim_results:

    for crucible in sim_results[trait_type]:

      crucible_dps = sim_results[trait_type][crucible]
      if int( last_best_dps ) < int( crucible_dps ):
        last_best_dps = crucible_dps
        name = crucible
  if settings.output_screen:
    print("Highest value found as trait, added to list as the first: " + name)
  crucible_list.append( name )

  for outer_outerline in sim_results:
    for outerline in sim_results[outer_outerline]:
      name = "error"
      current_best_dps = "-1"
      for trait_type in sim_results:
        for trait in sim_results[trait_type]:
          crucible_dps = sim_results[trait_type][trait]
          if int( current_best_dps ) <= int( crucible_dps ) and int( last_best_dps ) > int( crucible_dps ):
            current_best_dps = crucible_dps
            name = trait
          elif crucible_dps == "0" and not trait in crucible_list:
            current_best_dps = crucible_dps
            name = trait
      if not name == "error":
        crucible_list.append( name )
        last_best_dps = current_best_dps

  return crucible_list


def print_manager(base_dps_dict, sim_results, fight_style):

  filename = __create_filename(fight_style)

  for print_type in settings.output_types:
    print("")

    if print_type is "json":
      print("Initiating json output.")
      all_simulations = dict(sim_results)
      all_simulations["baseline"] = base_dps_dict["baseline"]

      if json.print_json(all_simulations, filename):
        print("Generating json file: Done")
      else:
        print("Generating json file: Failed")

    elif print_type is "highchart":
      print("Initiating highchart output")
      print("Ordering crucibles by dps.")
      ordered_crucible_names = __order_results(sim_results)

      if settings.output_screen:
        print(ordered_crucible_names)

      print("Normalising dps values.")
      normalised_sim_results = __normalise_crucibles(base_dps_dict, sim_results)

      if settings.output_screen:
        print(normalised_sim_results)

      if highcharts.print_highchart(normalised_sim_results, ordered_crucible_names, filename):
        print("Generating highchart file: Done")
      else:
        print("Generating highchart file: Failed")

      if crucible_weights.print_crucibles(normalised_sim_results, filename):
        print("Generating crucible weights file: Done")
      else:
        print("Generating crucible weights file: Failed")
  print("")
  return True
