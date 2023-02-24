import frappe
from datetime import date

@frappe.whitelist()
def site_power_custom(dateFrom, dateTo, site_name):


    # #######
    powerMonthlyArr  = []
    sum = 0
    # dateStringStart = datetime.datetime(year, month, day, 00, 00, 00)
    # dateStringEnd = datetime.datetime(year, month, day, 23, 59, 59)
    queryString = f"""select site_name, power_per_hour, `from`, `to` from `tabSite Power Per Hour`  where site_name = "{site_name}" and `from` > "{dateFrom}" and `to` < "{dateTo}" order by `from` asc"""
    # return queryString
    docArr = frappe.db.sql(queryString)
    for element in docArr:
        sum = sum + element[1]
        jsonObjDay = {
            "site_name": element[0],
            "power": element[1],
            "from": element[2],
            "to": element[3]
        }
        powerMonthlyArr.append(jsonObjDay)
    response = {
        "length": len(powerMonthlyArr),
        "powerSum": sum,
        "body": powerMonthlyArr
    }
    return response 


@frappe.whitelist()
def site_power_detail(dateFrom, dateTo, site_name):

    # #######
    powerMonthlyArr  = []
    sum = 0
    queryString = f"""select site_name, power_per_hour, `from`, `to` from `tabSite Power Per Hour`  where site_name = "{site_name}" and `from` > "{dateFrom}" and `to` < "{dateTo}" order by `from` asc"""
    docArr = frappe.db.sql(queryString)
    for element in docArr:
        sum = sum + element[1]
        jsonObjDay = {
            "site_name": element[0],
            "power": element[1],
            "from": element[2],
            "to": element[3]
        }
        powerMonthlyArr.append(jsonObjDay)
    response = {
        "length": len(powerMonthlyArr),
        "powerSum": sum,
        "body": powerMonthlyArr
    }
    return response 


queryString = f"""select site_label from `tabSite`"""
siteList = frappe.db.sql(queryString)
siteListParsed = []
i = 0
while i < len(siteList):
    siteListParsed.append(siteList[i][0])
    i = i + 1
#today date time
today = date.today()
todayStart = str(today) + " 00:00:00"
todayEnd = str(today) + " 23:59:59"

####site power details####
powerMonthlyArr = []
for site in siteListParsed:
        # return {"dateFrom":"2023-02-07 00:00:00","dateTo":"2023-02-07 18:00:00","site_name": {site}}
        site_data = site_power_detail(todayStart,todayEnd,site)
        for element in site_data["body"]:
            powerMonthlyArr.append(element)
####site power total of each site list######
powerSum = []
for site in siteListParsed:
    site_test = site_power_custom(todayStart, todayEnd, site)
    powerSum.append({"site_name": site, "power_total": site_test["powerSum"], "date": today})


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
th, td {{padding-top: 10px;padding-bottom: 20px;padding-left: 30px;padding-right: 40px;}}
</style>
</head>
<body>
<!-- Header -->
<header class="w3-display-container w3-content w3-wide" style="max-width:1600px;min-width:500px" id="home">
  <div class="w3-display-bottomleft w3-padding-large w3-opacity">
    <h1 class="w3-xxlarge">REPORT</h1>
  </div>
</header>

<!-- Page content -->
<div class="w3-content" style="max-width:1100px">

  <!-- About Section -->
  <div class="w3-row w3-padding-64" id="about">
    <div class="w3-col m6 w3-padding-large">
      <h1 class="w3-center">Site Power Daily</h1><br>
      <h5 class="w3-center">{today}</h5>
      <p class="w3-large">This email was sent automatically by PLINK Smart Technology Joint Stock Company. Below is the daily total sites power report.</p>
    </div>
  </div>
  
  <hr>
  """
html_template += """
  <div class="w3-row w3-padding-64" id="menu">
    <div class="w3-col l6 w3-padding-large">
"""
html_template += "<table><thead><tr><th colspan=\"5\">Site Name</th><th>Total Power (kWh)</th></tr></thead><tbody>"
for data in powerSum:
  html_template += "<tr><td colspan=\"5\">{site_name}</td><td>{power}</td></tr>".format(
            site_name=data['site_name'],
            power=data['power_total'] / 1000
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