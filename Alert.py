# -*- coding: UTF-8 -*-
import datetime
import json

import requests


def parse_time(*args):
    times = []
    for dates in args:
        eta_temp = dates
        fd = datetime.datetime.strptime(eta_temp, "%Y-%m-%dT%H:%M:%S.%fZ")
        eta = (fd + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S.%f")
        times.append(eta)
    return times


def alert(types, levels, times, instances, summary):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********告警通知**********\n告警类型: {0}\n告警级别: {1}\n故障时间: {2}\n故障实例: {3}\n故障总结：{4}".format(
                    types, levels, times[0], instances, summary)
            }
    })

    return params


def recive(types, levels, times, instances, summary):
    params = json.dumps({
        "msgtype": "text",
        "text":
            {
                "content": "**********恢复通知**********\n告警类型: {0}\n告警级别: {1}\n故障时间: {2}\n\n恢复时间: {3}\n故障实例: {4}\n故障总结：{5}".format(
                    types, levels, times[0], times[1], instances, summary)
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
