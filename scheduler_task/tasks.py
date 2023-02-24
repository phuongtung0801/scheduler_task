import frappe
import string
import random
import json
from frappe.utils.pdf import get_pdf
from datetime import date

from dateutil.relativedelta import relativedelta
from frappe.utils import get_path

import sys
from pathlib import Path
parent_dir_path = str(Path(__file__).resolve().parents[2])
sys.path.append(parent_dir_path + "/power_stuffs/power_stuffs/")
sys.path.append(parent_dir_path + "/scheduler_task/scheduler_task/")

from api_backend_gateway import *
from html_template_script import html_template

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


@frappe.whitelist()
def cron():
    #site list query
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
  

    today = datetime.date.today()

    html = """
            
            <body>"""
    html += f"""<h1>Plink Site's Power Daily Report {today}</h1>"""
    html += "<br>"
    html += "<br>"
    html += "<br>"
    html += "<table><thead><tr><th colspan=\"5\">Site Name</th><th>Total Power (kWh)</th></tr></thead><tbody>"
    for data in powerSum:
        html += "<tr><td colspan=\"5\">{site_name}</td><td>{power}</td></tr>".format(
            site_name=data['site_name'],
            power=data['power_total'] / 1000
        )
    html += "</tbody></table>"

    html += "</body>"
    
    text_file = open('/home/phuongtung0801/frappe-bench-prod/apps/scheduler_task/scheduler_task/indextung3.html','w')
    text_file.writelines(html_template)
    text_file.close()
    
    html2 = """
    <html>
    <body>
    <p><strong>This text is bold.</strong></p>
    <p><span style="font-size: 16px;">This text is size 16.</span></p>
    <p><span style="color: red;">This text is red.</span></p>
    <br>
    </body>
    </html>
            """

    try:
        frappe.sendmail(
            recipients=["phuongtung0801+23@gmail.com", "phuongtung.tran0801+23@gmail.com"],
            subject="Plink Sites's Power Daily Report",
            message=html_template,
            delayed= False,
            attachments=[]
        )
    except Exception as e:
        return ("Error"+str(e))
    return "No Err Found"
    
