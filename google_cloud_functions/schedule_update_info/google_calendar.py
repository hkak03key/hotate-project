from abc import ABCMeta, abstractmethod
import os
import googleapiclient.discovery
import google.auth
from google.cloud import datastore
import datetime
import pytz

def _create_credentials():
    credentials, _ = google.auth.default()
    return credentials


def _create_service(credentials):
    return googleapiclient.discovery.build('calendar', 'v3', credentials=credentials, cache_discovery=False)


def generate_gcalendar_events(calendar_id, params):
    prm = params.copy()
    prm.update({"calendarId": calendar_id})
    page_token = None
    gcal_svc = _create_service(_create_credentials())
    while True:
        if page_token:
            prm.update({"pageToken": page_token})

        events = gcal_svc.events().list(**prm).execute()
        yield events

        page_token = events.get("nextPageToken")
        if not page_token:
            break


class GCalendarSync():
    def __init__(self, calendar_id, gcal_sync_token_mngr):
        self._calendar_id = calendar_id
        self._gcal_sync_token_mngr = gcal_sync_token_mngr

    def get_events(self):
        sync_token = self._gcal_sync_token_mngr.sync_token
        params = {
                "calendarId": self._calendar_id,
                "showDeleted": True,
            }

        if sync_token:
            params.update({"syncToken": sync_token})
        else:
            datetime_today_native = datetime.datetime.combine(datetime.date.today(), datetime.time())
            # warning: tzはカレンダーから取得するべき
            datetime_today = pytz.timezone("Asia/Tokyo").localize(datetime_today_native)
            params.update({"timeMin": datetime_today.isoformat()})

        for i in generate_gcalendar_events(self._calendar_id, params):
            self._gcal_sync_token_mngr.sync_token = i.get("nextSyncToken")
            yield i

    def get_event_items(self):
        for e in self.get_events():
            for i in e["items"]:
                yield i


class GCalendarSyncTokenManager(metaclass=ABCMeta):
    def __init__(self):
        self.sync_token = None

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        if (not ex_type) and self.sync_token:
            self.save_sync_token()

    @abstractmethod
    def save_sync_token(self):
        pass

    @abstractmethod
    def delete_sync_token(self):
        pass


class GCalendarSyncLocalTokenManager(GCalendarSyncTokenManager):
    def __init__(self, filepath):
        super().__init__()

        self._filepath = filepath
        if not os.path.isfile(self._filepath):
            return None

        with open(self._filepath) as f:
            self.sync_token = f.read()

    def save_sync_token(self):
        with open(self._filepath, mode="w") as f:
            f.write(self.sync_token)

    def delete_sync_token(self):
        os.remove(self._filepath)
        self.sync_token = None


class GCalendarSyncGoogleDataStoreTokenManager(GCalendarSyncTokenManager):
    def __init__(self, kind, name):
        super().__init__()
        self._ds_client = datastore.Client()
        self._ds_key = self._ds_client.key(kind, name)
        self._entity_key = "value"
        entity = self._ds_client.get(self._ds_key)
        self.sync_token = entity.get(self._entity_key) if entity else None

    def save_sync_token(self):
        entity = datastore.Entity(key=self._ds_key)
        entity[self._entity_key] = self.sync_token
        self._ds_client.put(entity)

    def delete_sync_token(self):
        self._ds_client.delete(self._ds_key)

