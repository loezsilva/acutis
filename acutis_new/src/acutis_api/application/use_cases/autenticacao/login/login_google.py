from flask import url_for


class LoginGoogleUseCase:
    def __init__(self, google):
        self._google = google

    def execute(self):
        redirect_uri = url_for(
            'autenticacao_bp.google_callback', _external=True
        )
        return self._google.authorize_redirect(redirect_uri)
