# -*- coding: UTF-8 -*-
import datetime
import json

import requests


def parse_time(*args):
    times = []
    for dates in args:
        eta_temp = dates
        fd = datetime.datetime.strptime(eta_temp, "%Y-%m-%dT%H:%M:%S.%fZ")
        eta = (fd + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        times.append(eta)
    return times


def alert(types, levels, times, instances, summary):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"#F56C6C\">告警通知</font>\n"
                           "<font color=\"E6A23C\">**{0}**</font>\n"
                           "> **告警类型:** <font color=\"\\#909399\">{1}</font>\n"
                           "> **告警级别:** <font color=\"\\#909399\">{2}</font>\n"
                           "> **故障实例:** <font color=\"\\#909399\">{3}</font>\n"
                           "> **故障时间:** <font color=\"\\#909399\">{4}</font>".format(
                    summary, types, levels, instances, times[0])
            }
    })

    return params


def recive(types, levels, times, instances, summary):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"#67C23A\">恢复通知</font>\n"
                           "<font color=\"E6A23C\">**{0}**</font>\n"
                           "> **告警类型:** <font color=\"\\#909399\">{1}</font>\n"
                           "> **告警级别:** <font color=\"\\#909399\">{2}</font>\n"
                           "> **故障实例:** <font color=\"\\#909399\">{3}</font>\n"
                           "> **故障时间:** <font color=\"\\#909399\">{4}</font>\n"
                           "> **恢复时间:** <font color=\"\\#909399\">{5}</font>".format(
                    summary, types, levels, instances, times[0], times[1])
            }
    })

    return params


def webhook_url(params):
    headers = {"Content-type": "application/json"}
    """
    *****重要*****
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***"
    r = requests.post(url, params, headers)


def send_alert(json_re):
    for i in json_re['alerts']:
        if i['status'] == 'firing':
            webhook_url(alert(i['labels']['alertname'], i['labels']['level'], parse_time(i['startsAt']),
                              i['labels']['instance'], i['annotations']['summary']))
        elif i['status'] == 'resolved':
            webhook_url(
                recive(i['labels']['alertname'], i['labels']['level'], parse_time(i['startsAt'], i['endsAt']),
                       i['labels']['instance'], i['annotations']['summary']))
