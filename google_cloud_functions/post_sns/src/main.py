from google.cloud import secretmanager_v1beta1 as secretmanager
import google.auth
import json
import requests
from requests_oauthlib import OAuth1Session
from flask import jsonify


def get_secrets(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    try:
        name = client.secret_version_path(project_id, secret_id, version_id)
        response = client.access_secret_version(name)
        payload = response.payload.data.decode('UTF-8')
        return json.loads(payload)
    except Exception as e:
        return None


def post_line(msg, secrets):
    if not secrets:
        return "secret not found"
    url = "https://api.line.me/v2/bot/message/broadcast";
    payload = {
        "messages": [{
            "type": "text",
            "text": msg,
        }]}

    headers = {
        "Content-Type" : "application/json; charset=UTF-8",
        'Authorization': "Bearer {}".format(secrets.get("CHANNEL_ACCESS_TOKEN")),
    }
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    return res


def post_twitter(msg, secrets):
    CK  = secrets.get("CONSUMER_API_KEY")
    CS  = secrets.get("CONSUMER_API_SECRET")
    AT  = secrets.get("ACCESS_TOKEN")
    ATS = secrets.get("ACCESS_TOKEN_SECRET")
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理
    
    url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント
    params = {"status" : msg}
    res = twitter.post(url, params = params) #post送信
    return res


def post(msg):
    _, project_id = google.auth.default()
    
    ret = {
        target: {
            "status_code": res.status_code if res else 500,
            "response": res.text if res else "secrets is not found."
        } for target, res in {
            i["target"]: i["post_func"](msg, i["secrets"]) if i["secrets"] else None
                for i in [{"target": target, "post_func": post_func, "secrets": get_secrets(project_id, target)}
                    for target, post_func in {
                        "LINE": post_line,
                        "twitter": post_twitter
                    }.items()
                ]
            }.items()
    }
    return ret


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    data = request.get_json()
    msg = data.get("msg")
    if not msg:
        return jsonify({"message": """Content-Type is required "application/json", and it needs "msg" key."""}), 400

    ret = post(msg)
    return jsonify(ret), max([ v["status_code"] for k, v in ret.items()])

