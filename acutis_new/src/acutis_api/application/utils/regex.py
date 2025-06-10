import re


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
    text = re.sub('[çÇ]', 'c', text)

    # Remover acentos
    text = re.sub('[áàãâä]', 'a', text)
    text = re.sub('[éèêë]', 'e', text)
    text = re.sub('[íìîï]', 'i', text)
    text = re.sub('[óòõôö]', 'o', text)
    text = re.sub('[úùûü]', 'u', text)

    # Remover pontos e sinais
    text = re.sub('[.!?,:;ºª]', '', text)
    text = re.sub('_', ' ', text)

    if is_url:
        text = text.replace(' ', '-')

    if not lower:
        return text

    return text.lower()
