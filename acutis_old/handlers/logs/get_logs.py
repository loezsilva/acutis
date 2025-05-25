import json
import math
from datetime import datetime, timedelta
from flask import request, jsonify

class LogsGetAll:
    def __init__(self) -> None:
        self.__http_request_args = request.args
        self.__page = self.__http_request_args.get("page", 1, type=int)
        self.__per_page = self.__http_request_args.get("per_page", 10, type=int)
        self.__data_inicial = self.__http_request_args.get("start_date")
        self.__end_date = self.__http_request_args.get("end_date")
        self.__cargo = self.__http_request_args.get("cargo")
        self.__user_name = self.__http_request_args.get("username")
        self.__route_filter = self.__http_request_args.get("route")
        self.__action = self.__http_request_args.get("action")

    def execute(self):
        logs = self.__read_logs()
        filtered_logs = self.__apply_filters(logs)
        paginated_logs = self.__paginate_logs(filtered_logs)
        return self.__format_response(paginated_logs)

    def __read_logs(self):
        logs = []
        with open("access_log.txt", "r") as log_file:
            for line in log_file:
                try:
                    log_entry = json.loads(line.strip())
                    if "response_data" in log_entry and isinstance(log_entry["response_data"], str):
                        log_entry["response_data"] = json.loads(log_entry["response_data"])
                    logs.append(log_entry)
                except json.JSONDecodeError:
                    pass
        return logs

    def __apply_filters(self, logs):
        options_action = {
            "Cadastro": "POST",
            "Visualizar": "GET",
            "Deletar": "DELETE",
            "Atualizar": "PUT"
        }

        filtered_logs = logs

        if self.__data_inicial and self.__end_date:
            start_date = datetime.strptime(self.__data_inicial, "%Y-%m-%d")
            end_date = datetime.strptime(self.__end_date, "%Y-%m-%d")
            filtered_logs = [
                log for log in filtered_logs
                if self.__filter_by_date(log, start_date, end_date)
            ]

        if self.__cargo:
            filtered_logs = [
                log for log in filtered_logs
                if log.get("cargo") == (self.__cargo)
            ]

        if self.__user_name:
            filtered_logs = [
                log for log in filtered_logs
                if log.get("username", "").lower().startswith(self.__user_name.lower())
            ]

        if self.__route_filter:
            filtered_logs = [
                log for log in filtered_logs
                if self.__route_filter.lower() in log.get("route", "").lower()
            ]

        if self.__action:
            filtered_logs = [
                log for log in filtered_logs
                if options_action.get(self.__action, "") == log.get("method")
            ]

        return sorted(
            filtered_logs,
            key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )

    def __filter_by_date(self, log, start_date, end_date):
        log_timestamp = datetime.strptime(log.get("timestamp"), "%Y-%m-%d %H:%M:%S")
        return start_date <= log_timestamp <= end_date + timedelta(days=1)

    def __paginate_logs(self, logs):
        total_items = len(logs)
        total_pages = math.ceil(total_items / self.__per_page)

        start_index = (self.__page - 1) * self.__per_page
        end_index = start_index + self.__per_page

        return {
            "logs": logs[start_index:end_index],
            "page": self.__page,
            "pages": total_pages,
            "total": total_items
        }

    def __format_response(self, paginated_logs):

        return {
            "logs": paginated_logs["logs"],
            "page": paginated_logs["page"],
            "total": paginated_logs["total"]
        }

