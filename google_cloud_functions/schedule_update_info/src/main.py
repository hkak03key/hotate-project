import googleapiclient.discovery
import google.auth
import datetime
import json
import locale
import pytz
import requests
import sys

import google_calendar as gcal

locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")


def get_id_token(audience):
    r = requests.get(
            "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience={}".format(audience),
            headers={"Metadata-Flavor": "Google"})
    return r.text


def call_functions(pj_id, region, func_name, method, data):
    url = "https://{}-{}.cloudfunctions.net/{}".format(region, pj_id, func_name)
    headers = {
        "Authorization": "bearer {}".format(get_id_token(url)),
        "content-type": "application/json",
    }
    r = requests.request(method, url, headers=headers, data=json.dumps(data))
    return r.text, r.status_code


def interpret_status(event_item, threshold_sec=60):
    if event_item["status"] == "cancelled":
        return "cancelled"
    updated = datetime.datetime.fromisoformat(event_item["updated"].rstrip("Z"))
    created = datetime.datetime.fromisoformat(event_item["created"].rstrip("Z"))
    life_sec = (updated - created).seconds
    if life_sec >= threshold_sec:
        return "updated"
    return "created"


def date_str_to_datetime(date_str):
    return pytz.timezone("Asia/Tokyo").localize(
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        ) if date_str else None


def helper_get_event_items(calendar_id, date_start, date_end=None):
    items = sum([e.get("items") for e in
                    gcal.generate_gcalendar_events(
                        calendar_id, 
                        {
                            "timeMin": date_start.isoformat(),
                            "timeMax": ((date_end if date_end else date_start)
                                + datetime.timedelta(days=1)
                                - datetime.timedelta(seconds=1)
                                ).isoformat(),
                        }
                    )],
                [])
    return items


def create_message(infos):
    ret_msg = "やほ～！出勤情報が更新されたよ〜！\n----\n"
  
    def _helper_create_msg(infos, key):
        _ret_msg = "";
        for date, places in infos[key].items():
            _ret_msg += "・" + date.strftime("%m/%d（%a）") + "、".join(places) + "\n"
        return _ret_msg

    for k, v in {"attendance": "○出勤", "absence": "○出勤→欠勤"}.items():
        if len(infos[k]):
            ret_msg += v + "\n"
            ret_msg += _helper_create_msg(infos, k)
            ret_msg += "\n"

    ret_msg += "遊びに来てね〜！！";
    return ret_msg;


def post_schedule_update_info():
    _, pj_id = google.auth.default()
    calendar_id = "go1v09pqgsfc586u5ugeco97j4@group.calendar.google.com"
    with gcal.GCalendarSyncGoogleDataStoreTokenManager(
            "schedule_update_info", "google_calendar_sync_token") as gcal_sync_token_mngr:
        gcal_sync = gcal.GCalendarSync(calendar_id, gcal_sync_token_mngr)
        updated_dates = list(set([date_str_to_datetime(i["start"].get("date"))
                            for i in gcal_sync.get_event_items()
                        ]))
        if not len(updated_dates):
            return "not updated.", 200

        updated_dates.sort()

        infos = {"attendance": {}, "absence": []}
        [infos["attendance"].update({date: places}) if len(places) else infos["absence"].push(date)
            for date, places in
                {date: [i["summary"] for i in helper_get_event_items(calendar_id, date)]
                    for date in updated_dates
                }.items()
            ]
        msg = create_message(infos)
        if not msg:
            return "today is not attended.", 200
        return call_functions(pj_id, "asia-northeast1", "post_sns", "post", {"msg": msg})


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    try:
        result = post_schedule_update_info()
        return result
    except Exception as e:
        return "{} {}".format(type(e), e), 500

if __name__ == "__main__":
    print(post_schedule_update_info())

