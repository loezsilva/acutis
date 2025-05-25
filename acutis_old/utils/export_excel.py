import pandas as pd
import os
from io import BytesIO
from exceptions.errors_handler import errors_handler
from services.factories import file_service_factory

def export_excel(data, nome_file):
    s3_client = file_service_factory()
    df = pd.DataFrame(data)
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")

    output.seek(0)

    object_name = f"{nome_file}.xlsx"

    try:
        s3_client.upload_fileobj(output, object_name, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        public_url = s3_client.get_public_url(object_name)
        return {"url": public_url}

    except Exception as e:
        raise errors_handler(e)
