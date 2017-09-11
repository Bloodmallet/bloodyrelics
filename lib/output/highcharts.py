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

  # data handle for all series
  series = []

  ## handle all normal itemlevels data for series
  series_ilevel_data = []

  for crucible_name in ordered_crucible_names:

    series_ilevel_data.append( int( crucibles_list[ crucible_name ] ) )

    series_ilevel = {
      "name": 1,
      "color": settings.graph_colours[0],
      "data": series_ilevel_data
    }

  # add dictionary to series
  series.append(series_ilevel)


  highcharts_data = {
    "chart": {
      "type": "bar"
    },
    "title": {
      "text": settings.graph_title
    },
    "subtitle": {
      "text": settings.graph_subtitle
    },
    "xAxis": {
      "categories": categories
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
        "enabled": False,
        "style": {
          "fontWeight": "bold",
          "color": "'''(Highcharts.theme && Highcharts.theme.textColor) || 'white''''" 
        },
        "formatter": """'''function() {
            /* I need to figure out how to get the mean value here,
            ** to allow the percent diff to mean as label
            ** console.log(this); */
            return;
          }'''"""
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
                s += '<br/><span style=\"color: ' + this.points[i].series.color + '; font-weight: bold;\">' + this.points[i].series.name +'</span>: ' + cumulative_amount;
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
          "color": "'''(Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white''''"
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


