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

# @frappe.whitelist()
# def site_power_custom():

#     site_name = "Sơn Thủy"
#     dateFrom = "2023-02-01 00:00:00"
#     dateTo = "2023-02-27 23:00:00"
#     # #######
#     powerMonthlyArr  = []
#     sum = 0
#     # dateStringStart = datetime.datetime(year, month, day, 00, 00, 00)
#     # dateStringEnd = datetime.datetime(year, month, day, 23, 59, 59)
#     queryString = f"""SELECT power.site_name, power.power_per_hour, power.`from`, power.`to`, site.site_design_power, task.reduction_power 
#                     FROM `tabSite Power Per Hour` AS power 
#                     INNER JOIN `tabSite` AS site ON site.name = power.site_name
#                     INNER JOIN `tabTask` AS task ON task.site = power.site_name
#                     WHERE power.site_name = "{site_name}" AND power.`from` > "{dateFrom}" AND power.`to` < "{dateTo}" 
#                     ORDER BY power.`from` ASC
#                     """
#     # queryString = f"""SELECT * FROM `tabTask` AS task where task.site = "{site_name}" limit 100"""
#     # return queryString
#     # return queryString
#     docArr = frappe.db.sql(queryString)
#     for element in docArr:
#         sum = sum + element[1]
#         jsonObjDay = {
#             "site_name": element[0],
#             "power": element[1],
#             "from": element[2],
#             "to": element[3],
#             "site_design_power": element[4],
#             "reduction_power": element[5]
#         }
#         powerMonthlyArr.append(jsonObjDay)
#     response = {
#         "length": len(powerMonthlyArr),
#         "powerSum": sum,
#         "body": powerMonthlyArr
#     }
#     return response 


# @frappe.whitelist()
# def site_power_detail(dateFrom, dateTo, site_name):

#     # #######
#     powerMonthlyArr  = []
#     sum = 0
#     queryString = f"""select site_name, power_per_hour, `from`, `to` from `tabSite Power Per Hour`  where site_name = "{site_name}" and `from` > "{dateFrom}" and `to` < "{dateTo}" order by `from` asc"""
#     docArr = frappe.db.sql(queryString)
#     for element in docArr:
#         sum = sum + element[1]
#         jsonObjDay = {
#             "site_name": element[0],
#             "power": element[1],
#             "from": element[2],
#             "to": element[3]
#         }
#         powerMonthlyArr.append(jsonObjDay)
#     response = {
#         "length": len(powerMonthlyArr),
#         "powerSum": sum,
#         "body": powerMonthlyArr
#     }
#     return response 


@frappe.whitelist()
def cron():
    # #site list query
    # queryString = f"""select site_label from `tabSite`"""
    # siteList = frappe.db.sql(queryString)
    # siteListParsed = []
    # i = 0
    # while i < len(siteList):
    #     siteListParsed.append(siteList[i][0])
    #     i = i + 1
    # #today date time
    # today = date.today()
    # todayStart = str(today) + " 00:00:00"
    # todayEnd = str(today) + " 23:59:59"

    # ####site power details####
    # powerMonthlyArr = []
    # for site in siteListParsed:
    #         # return {"dateFrom":"2023-02-07 00:00:00","dateTo":"2023-02-07 18:00:00","site_name": {site}}
    #         site_data = site_power_detail(todayStart,todayEnd,site)
    #         for element in site_data["body"]:
    #             powerMonthlyArr.append(element)
    # ####site power total of each site list######
    # powerSum = []
    # for site in siteListParsed:
    #     site_test = site_power_custom(todayStart, todayEnd, site)
    #     powerSum.append({"site_name": site, "power_total": site_test["powerSum"], "date": today})
  

    # today = datetime.date.today()

    try:
        frappe.sendmail(
            recipients=["phuongtung.tran0801+23@gmail.com", "luonghuuphuloc@gmail.com"],
            # recipients=[
            # "phuongtung.tran0801+23@gmail.com",
            # "luonghuuphuloc@gmail.com",
            # "duongsonba1203@gmail.com",
            # "baonguyen2409@gmail.com",
            # "philh@pec.vn",
            # "phamxuantien1196@gmail.com",
            # "nhuquynhtrinhthi.99@gmail.com",
            # "nguyencongthong1407@gmail.com",
            # "nt.hieu.1911@gmail.com",
            # "thangpvh@pec.vn",
            # "hoanl@pec.vn",
            # "cuongtt@pec.vn"
            # ],
            subject="Plink Sites's Power Daily Report",
            message=html_template,
            delayed= False,
            attachments=[]
        )
    except Exception as e:
        return ("Error"+str(e))
    return "No Err Found"


@frappe.whitelist()
def sendEmailReport(emailList):
    emailListArr = emailList[1:-1].split(", ")
    try:
        frappe.sendmail(
            recipients=emailListArr,
            subject="Plink Sites's Power Daily Report",
            message=html_template,
            delayed= False,
            attachments=[]
        )
    except Exception as e:
        return ("Error"+str(e))
    return emailListArr
    
