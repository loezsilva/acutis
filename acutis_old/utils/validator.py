from validate_docbr import CPF, CNPJ

from exceptions.error_types.http_bad_request import BadRequestError


def cpf_cnpj_validator(cpf_cnpj: str, document_type: str) -> str:
    cpf_cnpj = "".join(filter(str.isdigit, cpf_cnpj))

    if document_type not in ["cpf", "cnpj"]:
        return cpf_cnpj

    if document_type == "cpf":
        cpf = CPF()
        if not cpf.validate(cpf_cnpj):
            raise BadRequestError("CPF inválido!")

    if document_type == "cnpj":
        cnpj = CNPJ()
        if not cnpj.validate(cpf_cnpj):
            raise BadRequestError("CNPJ inválido!")

    return cpf_cnpj
