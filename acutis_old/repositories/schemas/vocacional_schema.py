from enum import Enum

class ImageEtapaVocacional(str, Enum):
    """Enum for ImageEtapaVocacional."""

    ETAPA_PRE_CADASTRO = "https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/step1.png"
    ETAPA_CADASTRO = "https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/step2.png"
    ETAPA_FICHA_VOCACIONAL = "https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/step3.png"
    
