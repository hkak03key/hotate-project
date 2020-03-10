import googleapiclient.discovery
import google.auth
import datetime
import json
import pandas as pd
import pytz
import requests
import sys

def create_credentials():
    credentials, _ = google.auth.default()
    return credentials


def get_today_events(calendar_service, calendar_id):
    datetime_today_native = datetime.datetime.combine(datetime.date.today(), datetime.time())
    # warning: tzはカレンダーから取得するべき
    datetime_today = pytz.timezone('Asia/Tokyo').localize(datetime_today_native)
    today = datetime_today.isoformat()
    today_last = (datetime_today + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)).isoformat()
    # warning: 1日のeventは100個を超えないという暗黙の仮定
    return calendar_service.events().list(calendarId=calendar_id, timeMin=today, timeMax=today_last,
                                        maxResults=100).execute().get("items")


def get_today_message_format():
    credentials=create_credentials()
    gsht_svc = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials, cache_discovery=False)

    spreadsheet_id = "1MpynE2Ieadi_NBVittyUH8sXYfJqTwOb7UFuQCg36go"
    sht_range = "msg_list!A:C"

    response=gsht_svc.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                    range=sht_range).execute()

    df_master = pd.DataFrame(data=response["values"][1:], columns=response["values"][0]) \
            .assign(date= lambda df: pd.to_datetime(df["date"], format='%Y/%m/%d'))

    today = datetime.date.today()

    df_candidate = df_master[df_master["date"].dt.date == today]

    if not len(df_candidate):
        today_timings = ["default", "weekday" if (today.weekday() >= 0 and today.weekday() < 5) else "weekend"]
        df_candidate = df_master[df_master["timing"].isin(today_timings)]

    ret_msgfmt = df_candidate.sample(1)["message"].values[0].replace("\\n", "\n") \
        if len(df_candidate) \
        else "やほ～！今日は、\n{places}\nで出勤だよ～！遊びに来てね～～！"

    return ret_msgfmt


def create_attendance_message(events):
    if not events or len(events) == 0:
        return None

    places = ""
    for event in events:
        places += "「" + event.get("summary") + "」"

    ret_msg = get_today_message_format().format(places=places)
    return ret_msg


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
    return r


def post_attendance():
    calendar_id = "go1v09pqgsfc586u5ugeco97j4@group.calendar.google.com"
    credentials, pj_id = google.auth.default()
    calendar_service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials, cache_discovery=False)
    events = get_today_events(calendar_service, calendar_id)
    msg = create_attendance_message(events)
    if not msg:
        return "today is not attended.", 200
    r = call_functions(pj_id, "asia-northeast1", "post_sns", "post", {"msg": msg})
    r.raise_for_status()
    return r.text, r.status_code


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    result = post_attendance()
    return result

