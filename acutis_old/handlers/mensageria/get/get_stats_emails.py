from sendgrid import SendGridAPIClient
from config import SENDGRID_API_KEY
from flask import jsonify, request
from exceptions.errors_handler import errors_handler


class GetStatsEmails:
    def __init__(self) -> None:
        self.__sg = SendGridAPIClient(SENDGRID_API_KEY)

    def execute(self):

        data_request = request.args

        initial_date = data_request.get("initial_date")
        final_date = data_request.get("final_date")
        aggregated_by = data_request.get("aggregated_by") # day | month

        stats = self.__get_stats(initial_date, final_date, aggregated_by)

        return stats

    def __get_stats(self, initial_date, final_date, aggregated_by):
        try:
            response = self.__sg.client.stats.get(
                query_params={
                    "start_date": initial_date,
                    "end_date": final_date,
                    "aggregated_by": aggregated_by,
                }
            )
            return response.to_dict

        except Exception as er:
            return errors_handler(er)
