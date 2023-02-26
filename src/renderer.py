import httplib2
import os
import datetime

from apiclient import discovery
from google.oauth2 import service_account
from collections import defaultdict


class SheetsRenderer:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id

    def render(self, scores, names):
        service = self._create_service()
        data = self._prepare_data(scores, names)
        self._render(data, service)

    def _render(self, data, service):
        try:
            service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                body=data,
                range="Sheet1",
                valueInputOption="USER_ENTERED",
            ).execute()
        except OSError as e:
            print(f"Update spreadsheet: {e=}")

    def _prepare_data(self, scores, names) -> dict:
        values = [
            ["", "", names[0], ""],
            ["Date", "Easy", "Medium", "Hard"],
        ]

        for name in names[1:]:
            values[0].extend(["", name, ""])
            values[1].extend(["Easy", "Medium", "Hard"])
        score_lines = self._parse_scores(scores, len(names))

        for line in score_lines:
            values.append(line)

        return {"values": values}

    def _parse_scores(self, scores, users: int):
        row_date = scores[0][0]
        result = [[self._format_date(row_date)]]
        cache = defaultdict(list)
        for idx, score in enumerate(scores):
            values = self._parse_score(cache, score)
            cache[score[1]].append([score[2], score[3], score[4]])
            if score[0] != row_date:
                while len(result[-1]) < users * 3 + 1:
                    result[-1].append("-")
                row = [self._format_date(score[0]), values[0], values[1], values[2]]
                result.append(row)
                row_date = score[0]
            else:
                result[-1].extend([values[0], values[1], values[2]])

        while len(result[-1]) < users * 3 + 1:
            result[-1].append("-")

        return result

    def _parse_score(self, cache, score):
        current = [score[2], score[3], score[4]]
        if len(cache[score[1]]) == 0:
            return current
        previous = cache[score[1]][-1]

        for idx in range(len(previous)):
            diff = current[idx] - previous[idx]
            if diff > 0:
                current[idx] = f"{current[idx]} (+{diff})"
        return current

    def _format_date(self, iso_date: str) -> str:
        date = datetime.datetime.fromisoformat(iso_date)
        return f"{date: %d %b, %Y}"

    def _create_service(self) -> service_account:
        try:
            scopes = [
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/spreadsheets",
            ]
            secret_file = os.path.join(os.getcwd(), "../cfg/service_secret.json")
            credentials = service_account.Credentials.from_service_account_file(
                secret_file, scopes=scopes
            )
            service = discovery.build("sheets", "v4", credentials=credentials)
            return service
        except Error as e:
            print(f"Create service: {e=}")
