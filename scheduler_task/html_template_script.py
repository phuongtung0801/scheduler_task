import frappe
from datetime import date
import datetime

@frappe.whitelist()
def count_site_connection(dateFrom, dateTo):
    queryString = f"""
        SELECT site_name, COUNT(DISTINCT site_name) as counting
        FROM `tabAlarm Check List`
        WHERE
            start_at BETWEEN "{dateFrom}" AND "{dateTo}"
        GROUP BY site_name
            """
    # return queryString
    docArr = frappe.db.sql(queryString)
    res = []
    for element in docArr:
        res.append({
           "site_name": element[0],
           "count": element[1]
        })
    return res 

@frappe.whitelist()
def connection_count_template():

  #today date time
  today = date.today()
  # today = datetime.date(2023, 4, 2)
  todayStart = str(today) + " 00:00:00"
  todayEnd = str(today) + " 23:59:59"
  
  count_list = count_site_connection(todayStart, todayEnd)
  
  return count_list


def site_connection(dateFrom, dateTo):
    queryString = f"""
        SELECT * FROM `tabAlarm Check List`
        WHERE
            start_at BETWEEN "{dateFrom}" AND "{dateTo}"
        ORDER BY site_name ASC
            """
    # return queryString
    docArr = frappe.db.sql(queryString)
    res = []
    for element in docArr:
        res.append({
           "site_name": element[9],
           "inverter": element[16],
           "lost_connection_time": element[10]
        })
    return res 

@frappe.whitelist()
def connection_template():

  #today date time
  today = date.today()
  # today = datetime.date(2023, 4, 2)
  todayStart = str(today) + " 00:00:00"
  todayEnd = str(today) + " 23:59:59"
  
  site_connection_list = site_connection(todayStart, todayEnd)
  
  return site_connection_list


@frappe.whitelist()
#sum(power.power_per_hour) as total_power,
def site_power_custom(dateFrom, dateTo):
    queryString = f"""SELECT
            site.name,
            site.site_design_power,
            site.site_real_power,
            COALESCE(SUM(power.power_per_hour), 0) AS total_power,
            task.reduction_power
            FROM `tabSite` AS site
            LEFT JOIN `tabSite Power Per Hour` AS power ON site.name = power.site_name AND power.from BETWEEN "{dateFrom}" AND "{dateTo}"
            LEFT JOIN (
                SELECT site, reduction_power
                FROM `tabTask`
                WHERE `tabTask`.exp_start_date BETWEEN "{dateFrom}" AND "{dateTo}"
                GROUP BY site
            ) AS task ON power.site_name = task.site
            GROUP BY site.name;
            """
    # return queryString
    docArr = frappe.db.sql(queryString)
    res = []
    for element in docArr:
        res.append({
           "name": element[0],
           "site_design_power": element[1],
           "site_real_power": element[2],
           "total_power": element[3],
           "reduction_power": element[4]
        })
    return res 

@frappe.whitelist()
def power_template():

  #today date time
  today = date.today()
  # today = datetime.date(2023, 4, 2)
  todayStart = str(today) + " 00:00:00"
  todayEnd = str(today) + " 23:59:59"
  
  site_power_list = site_power_custom(todayStart, todayEnd)
  
  return site_power_list



####POWER VARIABLE#####
# today = datetime.date(2023, 4, 2)
today = date.today()
site_power_list = power_template()
total_power = 0
total_income = 0
for data in site_power_list:
   total_power += data['total_power'] / 1000
   total_income += data['total_power'] * 1938 / 1000

####CONNECTION VARIABLE#####
# today = datetime.date(2023, 4, 2)
today = date.today()
site_connection_list = connection_template()


####COUNT CONNECTION VARIABLE#####
# today = datetime.date(2023, 4, 2)
today = date.today()
count_list = connection_count_template()







################HTML TEMPLATE######################
html_template = f"""
<!DOCTYPE html>
<html>
<head>
<title>W3.CSS Template</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<style>
body {{font-family:Georgia, Serif;}}
h1, h2, h3, h4, h5, h6 {{
  font-family: "Playfair Display";
  letter-spacing: 5px;
}}
table {{
    padding: 10px;
    border-spacing: 0;
  }}
  td, th {{
    padding: 10px;
    text-align: center;
    border: 1px solid rgb(192, 192, 192);
  }}
  .no-center {{
    text-align: left; /* align the text to the left to exclude it from the center align */
  }}
</style>
</head>
<body>
<!-- Header -->
<header class="w3-display-container w3-content w3-wide" style="max-width:1600px;min-width:500px" id="home">
  <div class="w3-display-bottomleft w3-padding-large w3-opacity">
    <h1 class="w3-xxlarge no-center">REPORT</h1>
  </div>
</header>

<!-- Page content -->
<div class="w3-content" style="max-width:1100px">

  <!-- About Section -->
  <div class="w3-row w3-padding-64" id="menu">
    <div class="w3-col m6 w3-padding-medium">
      <h1 class="w3-center">Site daily information</h1><br>
      <h5 class="w3-center">Report is taken in {today}</h5>
      <h5 class="w3-center">from 00:00:00 to 23:59:59</h5>
      <p class="w3-large no-center">This email was sent automatically by PLINK Smart Technology Joint Stock Company. Below is the daily sites detail power report.</p>
    </div>
  </div>
  <hr>
  """

#####POWER REPORT######
html_template += """
      <div class="w3-col m6 w3-padding-medium">
      <h4 class="w3-center">POWER REPORT</h4>
      </div>
"""
html_template += """
  <div class="w3-row w3-padding-64" id="menu">
    <div class="w3-col l6 w3-padding-medium">
"""
html_template += """<table style="width: 100%;">
                      <thead><tr>
                        <th colspan=\"5\">Site Name</th>
                        <th colspan=\"5\">Site Design Power</th>
                        <th colspan=\"5\">Today Power (kWh)</th>
                        <th colspan=\"5\">Today Income (VND)</th>
                        <th colspan=\"5\">Average Run Time</th>
                        <th colspan=\"5\">Reduction Power</th>
                      </tr></thead><tbody>"""
for data in site_power_list:
  html_template += """<tr>
                      <td colspan=\"5\">{site_name}</td>
                      <td colspan=\"5\">{site_design_power}</td>
                      <td colspan=\"5\">{power}</td>
                      <td colspan=\"5\">{total_income}</td>
                      <td colspan=\"5\">{avg_run_time}</td>
                      <td colspan=\"5\">{reduction_power}</td>
                      </tr>""".format(
            site_name=data['name'],
            power=format((data['total_power'] / 1000), '.1f'),
            site_design_power=format(data['site_design_power'],'.1f'),
            total_income = '{:,.1f}'.format((data['total_power'] * 1938 / 1000), '.1f'),
            avg_run_time = format(((data['total_power'] / 1000 ) / data['site_design_power']), '.1f'),
            reduction_power=data['reduction_power']
        )
html_template +=f"""<tr><td colspan=\"5\"><b>Total Power</b></td>
                        <td colspan=\"10\"><b>{format(total_power, '.1f')} (kWh)</b></td>
                        <td colspan=\"5\"><b>Total Income</b></td>
                        <td colspan=\"10\"><b>{'{:,.1f} VNĐ'.format(total_income, '.1f')}</b></td>
                    </tr>"""  
html_template += """"""
html_template += "</tbody></table>"
html_template += """
   </div>
  </div>
"""


#####COUNT CONNECTION REPORT######
html_template += """
      <div class="w3-col m6 w3-padding-medium">
      <h4 class="w3-center">CONNECTION LOST REPORT</h4>
      </div>
"""

html_template += """
      <div class="w3-col m6 w3-padding-medium">
      <h5 class="w3-left">Count lost connection</h5>
      </div>
"""
html_template += """
  <div>
    <div class="w3-col l6 w3-padding-medium">
"""
html_template += """<table style="width: 100%;">
                      <thead><tr>
                        <th colspan=\"5\">Site Name</th>
                        <th colspan=\"5\">Number of lost connections</th>
                      </tr></thead><tbody>"""
for data in count_list:
  html_template += """<tr>
                      <td colspan=\"5\">{site_name}</td>
                      <td colspan=\"5\">{count}</td>
                      </tr>""".format(
            site_name=data['site_name'],
            count=data["count"]
        )
html_template += """"""
html_template += "</tbody></table>"
html_template += """
   </div>
  </div>
"""



#####CONNECTION REPORT######

html_template += """
  <div>
    <div class="w3-col l6 w3-padding-medium">
"""
html_template += """
      <h5 class="w3-left">Connection lost detail</h5>
"""
html_template += """<table style="width: 100%;">
                      <thead><tr>
                        <th colspan=\"5\">Site Name</th>
                        <th colspan=\"5\">Inverter</th>
                        <th colspan=\"5\">Lost connection time</th>
                      </tr></thead><tbody>"""
for data in site_connection_list:
  html_template += """<tr>
                      <td colspan=\"5\">{site_name}</td>
                      <td colspan=\"5\">{inverter}</td>
                      <td colspan=\"5\">{lost_connection_time}</td>
                      </tr>""".format(
            site_name=data['site_name'],
            inverter=data["inverter"],
            lost_connection_time=data["lost_connection_time"]
        )
html_template += """"""
html_template += "</tbody></table>"
html_template += """
   </div>
  </div>
"""




html_template += """
  <!-- Menu Section -->
  <div class="w3-row w3-padding-64" id="menu">
    <div class="w3-col l6 w3-padding-large">
      <h1 class="w3-center">Have a nice day.</h1><br>
    </div>
  </div>
<!-- End page content -->
</div>
</body>
</html>
"""
