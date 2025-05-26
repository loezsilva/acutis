import re

from acutis_api.exception.errors.bad_request import HttpBadRequestError


def validate_password(password: str) -> str:
    pattern = r'\s'
    if re.search(pattern, password):
        raise HttpBadRequestError('A senha não pode conter espaços em branco.')

    return password


def format_string(
    text: str | None,
    lower: bool = True,
    only_digits: bool = False,
    is_url: bool = False,
) -> str | None:
    if not text:
        return None

    if only_digits:
        text = ''.join(filter(str.isdigit, text))
    # Substituir "ç" por "c"
    text = re.sub('[ç]', 'c', text)

    # Remover acentos
    text = re.sub('[áàãâä]', 'a', text)
    text = re.sub('[éèêë]', 'e', text)
    text = re.sub('[íìîï]', 'i', text)
    text = re.sub('[óòõôö]', 'o', text)
    text = re.sub('[úùûü]', 'u', text)

    # Remover pontos e sinais
    text = re.sub('[.!?,:;ºª]', '', text)
    text = re.sub('[_]', ' ', text)

    if is_url:
        text = text.replace(' ', '-')

    if not lower:
        return text

    return text.lower()


def format_name(full_name: str) -> str | None:
    if not full_name:
        return None

    split_name = re.findall(r'\S+', full_name)

    LEN_CONST = 2

    if len(split_name) > LEN_CONST:
        first_name = split_name[0]
        surname = split_name[-1]

        middle_part = [part[0] for part in split_name[1:-1]]
        middle_name = ' '.join(middle_part)

        formatted_name = f'{first_name} {middle_name} {surname}'
        return formatted_name
    else:
        return full_name
