from main import app
from builder import db
from models import UsersImports
import logging
import csv

with app.app_context():
    try:
        nome_arquivo_csv = "20240411_175029.csv"
        contador_linhas = 0
        emails_existentes = set(
            usuario.email
            for usuario in UsersImports.query.with_entities(UsersImports.email)
        )

        usuarios_para_importar = []

        with open(
            nome_arquivo_csv, "r", newline="", encoding="utf-8"
        ) as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for row in leitor_csv:
                contador_linhas += 1
                print(f"Linha: {contador_linhas}")

                if row["Email"] not in emails_existentes:
                    usuarios_para_importar.append(
                        UsersImports(
                            nome=f"{row['Nome']} {row['Sobrenome']}",
                            email=row["Email"].replace('"', ""),
                            data_criacao=row["Data da criação"],
                            phone=row["Celular (WhatsApp)"]
                            or row["CELULAR"]
                            or row["Número de telefone"],
                        )
                    )

                    if len(usuarios_para_importar) >= 3000:
                        db.session.bulk_save_objects(usuarios_para_importar)
                        db.session.commit()
                        usuarios_para_importar = []

        if usuarios_para_importar:
            db.session.bulk_save_objects(usuarios_para_importar)
            db.session.commit()

    except Exception as ex:
        logging.error(str(ex), str(type(ex)))
