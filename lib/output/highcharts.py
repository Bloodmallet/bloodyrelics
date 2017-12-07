# File for handling all Highcharts

import datetime
import json
# Library to look for files and create them if needed
import os
import settings



##
## @brief      Generates js output for http://www.highcharts.com/ bars of
##             http://www.stormearthandlava.com/elemental-shaman-hub/elemental-trinket-sims/
##
## @param      trinket_list           The normalised trinkets dictionary
##                                    {trinket_name s:{ilevel s:{dps s}}}
## @param      ordered_crucible_names The ordered trinket names
## @param      filename               The filename
## TODO        Rewrite                Rewrite this whole function to use actual data types and
##                                    and convert that into json itself.
##
## @return     True if writing to file was successfull
##
def print_highchart( crucibles_list, ordered_crucible_names, filename ):

  categories = []
  for name in ordered_crucible_names:
    categories.append( name )

  # massage category names into wowhead links
  if settings.add_tooltips:
    new_categories_list = []

    import lib.simc_support.wow_lib as Wow_lib

    for i in range( len( categories ) ):
      trait_id = ""
      try:
        trait_id = Wow_lib.get_crucible_spell_id( settings.simc_settings[ "class" ], settings.simc_settings[ "spec" ], categories[ i ] )
      except Exception as e:
        pass
        #raise e
      else:
        # if a trait spell ID was found, replace the category name with the link
        categories[ i ] = "<a href=\"http://www.wowhead.com/spell={item_id}\">{item_name}</a>".format( item_id=trait_id, item_name=categories[ i ] )

  # data handle for all series
  series = []

  ## handle all normal itemlevels data for series
  series_light_shadow = []
  series_artifact = []

  for crucible_name in ordered_crucible_names:
    for trait_type in crucibles_list:

      if crucible_name in crucibles_list[trait_type]:
        if trait_type == "light and shadow":
          series_light_shadow.append( int( crucibles_list[ trait_type ][ crucible_name ] ) )
          series_artifact.append( 0 )
        else:
          series_light_shadow.append( 0 )
          series_artifact.append( int( crucibles_list[ trait_type ][ crucible_name ] ) )

  series_light_shadow_values = {
    "name": 1,
    "color": "#343434",
    "data": series_light_shadow,
    "showInLegend": False
  }

  series_artifact_values = {
    "name": 1,
    "color": settings.graph_colours[0],
    "data": series_artifact,
    "showInLegend": False
  }

  # add dictionary to series
  series.append(series_light_shadow_values)
  series.append(series_artifact_values)


  highcharts_data = {
    "chart": {
      "type": "bar"
    },
    "title": {
      "text": settings.graph_title,
      "useHTML": True
    },
    "subtitle": {
      "text": settings.graph_subtitle,
      "useHTML": True
    },
    "xAxis": {
      "categories": categories,
      "labels": {
        "useHTML": True,
      },
    },
    "yAxis": {
      "min": 0,
      "title": {
        "text": '\\u0394 Damage per second'
      },
      "labels": {
        "enabled": False
      },
      "stackLabels": {
        "enabled": True,
        "style": {
          "fontWeight": "bold",
          "color": "'''(Highcharts.theme && Highcharts.theme.textColor) || 'black''''"
        },
        "formatter": """'''function() {
          return Intl.NumberFormat().format(this.total);
        }'''""",
      }
    },
    "legend": {
      "align": "right",
      "x": 0,
      "verticalAlign": "bottom",
      "y": 0,
      "floating": False,
      "backgroundColor": "'''(Highcharts.theme && Highcharts.theme.background2) || 'white''''",
      "borderColor": '#CCC',
      "borderWidth": 1,
      "shadow": False,
      "reversed": True
    },
    "tooltip": {
      "headerFormat": "<b>{point.x}</b>",
      "formatter": """'''function() {
        var s = '<b>'+ this.x +'</b>';
        var cumulative_amount = 0;
        for (var i = this.points.length - 1 ; i >= 0 ; i--) {
            cumulative_amount += this.points[i].y;
            if (this.points[i].y !== 0){
                s += '<br/><span style=\"color: ' + this.points[i].series.color + '; font-weight: bold;\">' + this.points[i].series.name +'</span>: ' + Intl.NumberFormat().format(cumulative_amount);
            }
        }
        return s;
      }'''""",
      "shared": True,
      "backgroundColor": "#eee",
      "borderColor": "#bbb",
      "style": {
        "color": "black"
      }
    },
    "plotOptions": {
      "series": {
        "borderColor": "#151515",
        "events": {
          "legendItemClick": "'''function() { return false; }'''"
        }
      },
      "bar": {
        "stacking": "normal",
        "dataLabels": {
          "enabled": False,
          "color": "'''(Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white''''",
          "align": "right"
        },
        "point": {
          "events": {
            "click": """'''function (event) {
                var chart = this.series.yAxis;
                chart.removePlotLine('helperLine');
                chart.addPlotLine({
                    value: this.stackY,
                    color: '#000',
                    width: 2,
                    id: 'helperLine',
                    zIndex: 5,
                    label: {
                      text: this.series.name + ' ' + this.category,
                      align: 'left',
                      verticalAlign: 'bottom',
                      rotation: 0,
                      y: -5
                    }
                });
              }'''"""
          }
        }
      }
    },
    "series": series
  }

  # write raw file
  with open(filename + "_raw.js", "w") as ofile:
    ofile.write("Highcharts.chart('" + filename[10:] + "', \n")
    json.dump(highcharts_data, ofile, indent=4, sort_keys=True)
    ofile.write(");")

  # create result file without quotes in inappropriate places
  with open(filename + "_raw.js", "r") as old:
    with open(filename + ".js", "w") as new:
      for line in old:
        # get rid of quotes for key ("key": "value")
        if "\":" in line:
          newline = line.split("\":")[0].replace("\"", "")
          line = newline + ":" + line.split("\":")[1]
        # get rid of quotes around our functions
        if "\"'''" in line or "'''\"" in line:
          newline = line.replace("\"'''", "\\n").replace("'''\"", "\\n").replace("\\n", "")
          new.write(newline)
        elif "\\\\u" in line:
          newline = line.replace("\\\\u", "\\u")
          new.write(newline)
        else:
          new.write(line)
  # delete raw file
  os.remove(filename + "_raw.js")
  return True


