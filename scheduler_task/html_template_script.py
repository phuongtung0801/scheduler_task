import frappe
from datetime import date

@frappe.whitelist()
def site_power_custom(dateFrom, dateTo):
    queryString = f"""SELECT
            site.name,
            site.site_design_power,
            site.site_real_power,
            sum(power.power_per_hour) as total_power,
            task.reduction_power
        FROM `tabSite Power Per Hour` AS power 
            INNER JOIN `tabSite` AS site ON site.name = power.site_name
            LEFT JOIN 
            (
                SELECT
                    site,
                    reduction_power
                FROM `tabTask`
                WHERE
                    (`tabTask`.exp_start_date between "{dateFrom}" AND "{dateTo}")
                GROUP BY site
            ) AS task ON power.site_name = task.site
        WHERE
             (power.from between "{dateFrom}" AND "{dateTo}")
        GROUP BY power.site_name
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
  todayStart = str(today) + " 00:00:00"
  todayEnd = str(today) + " 23:59:59"
  
  site_power_list = site_power_custom(todayStart, todayEnd)
  
  return site_power_list


today = date.today()
site_power_list = power_template()

html_template = f"""
<!DOCTYPE html>
<html>
<head>
<title>W3.CSS Template</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<style>
body {{font-family: "Times New Roman", Georgia, Serif;}}
h1, h2, h3, h4, h5, h6 {{
  font-family: "Playfair Display";
  letter-spacing: 5px;
}}
table {{
    padding: 10px;
  }}
  td, th {{
    padding: 10px;
    text-align: center;
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
  <div class="w3-row w3-padding-64" id="about">
    <div class="w3-col m6 w3-padding-large">
      <h1 class="w3-center">Site Power Daily</h1><br>
      <h5 class="w3-center">Report is taken in {today}</h5>
      <p class="w3-large no-center">This email was sent automatically by PLINK Smart Technology Joint Stock Company. Below is the daily total sites power report.</p>
    </div>
  </div>
  
  <hr>
  """
html_template += """
  <div class="w3-row w3-padding-64" id="menu">
    <div class="w3-col l6 w3-padding-large">
"""
html_template += """<table>
                      <thead><tr>
                        <th colspan=\"5\">Site Name</th>
                        <th colspan=\"5\">Site Design Power</th>
                        <th colspan=\"5\">Total Power (kWh)</th>
                        <th colspan=\"5\">Total Income (VND)</th>
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
            power=data['total_power'] / 1000,
            site_design_power=data['site_design_power'],
            total_income = data['total_power'] * 1938 / 1000,
            avg_run_time = format(((data['total_power'] / 1000 ) / data['site_design_power']), '.4f'),
            reduction_power=data['reduction_power']
        )
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