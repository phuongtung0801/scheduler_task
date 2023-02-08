import frappe
import string
import random
from frappe.utils.pdf import get_pdf
import jinja2
import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
from frappe.utils import get_path


@frappe.whitelist()
def site_power_custom2(dateFrom, dateTo, site_name):

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


    powerMonthlyArr = []
    for site in siteListParsed:
            # return {"dateFrom":"2023-02-07 00:00:00","dateTo":"2023-02-07 18:00:00","site_name": {site}}
            site_data = site_power_custom2(todayStart,todayEnd,site)
            for element in site_data["body"]:
                powerMonthlyArr.append(element)

    html = "<body><h1>Plink Sites's Power Daily Report</h1>"
    html += """<p>This report is sent daily.</p>"""
    html += "<table><thead><tr><th>Site Name</th><th>Power</th><th>From</th><th>To</th></tr></thead><tbody>"
    for data in powerMonthlyArr:
        html += "<tr><td>{site_name}</td><td>{power}</td><td>{from_date}</td><td>{to_date}</td></tr>".format(
            site_name=data['site_name'],
            power=data['power'],
            from_date=data['from'],
            to_date=data['to']
        )
    html += "</tbody></table></body>"
    html += "<style>h1{text-align: center}table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding-top: 10px;padding-bottom: 20px;padding-left: 30px;padding-right: 40px;}</style>"
    
    # Generate the PDF from the HTML
    pdf_content = get_pdf(html)
    #open the file
    text_file = open('/home/phuongtung0801/frappe-bench-prod/apps/scheduler_task/scheduler_task/indextung3.html','w')
    text_file.writelines(html)
    text_file.close()

    # pdfkit.from_string(pdf_content, '/home/phuongtung0801/frappe-bench-prod/apps/scheduler_task/scheduler_task/indextung.pdf')
    with open("/home/phuongtung0801/frappe-bench-prod/apps/scheduler_task/scheduler_task/indextung11.pdf", "wb") as f:
        f.write(pdf_content)

    try:
        frappe.sendmail(
            recipients=["phuongtung0801+23@gmail.com"],
            subject="Plink Sites's Power Daily Report",
            message="Hi, this is the daily sites's power report.",
            attachments=[{
                "fname": "plink_sitespower_daily_report.pdf",
                "fcontent": pdf_content
            }]
        )
    except Exception as e:
        return ("Error"+str(e))
    return "No Err Found"
    
# frappe.schedule("*/5 * * * *", send_scheduled_email)


# def cron():
#     print("Hello World")