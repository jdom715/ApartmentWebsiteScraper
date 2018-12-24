# coding=utf-8
class CommandLineArguments:
    def __init__(self, google_credentials_file_path: str):
        self._google_credentials_file_path = google_credentials_file_path

    def get_google_credentials_file_path(self) -> str:
        return self._google_credentials_file_path
