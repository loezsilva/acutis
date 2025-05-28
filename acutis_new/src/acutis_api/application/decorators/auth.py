import functools
import uuid # Added for UUID conversion
from flask import abort
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from sqlalchemy.orm import Session

# Assuming these are the correct import paths based on typical project structure
from acutis_api.domain.database import get_session
from acutis_api.domain.entities.lead import Lead
# Perfil entity might not be directly queried if we get profile names via PermissaoLead
# from acutis_api.domain.entities.perfil import Perfil 
from acutis_api.domain.entities.permissao_lead import PermissaoLead
from acutis_api.domain.entities.enums.perfil_enum import PerfilEnum


def permission_required(*allowed_profiles_input: str | PerfilEnum): # Type hint for clarity
    """
    Decorator factory that checks if a lead has any of the allowed profiles.
    Profiles can be passed as string names or PerfilEnum members.
    """
    # Convert all allowed_profiles_input to their string values at the factory level
    # This simplifies the wrapper as it will only deal with a set of strings.
    processed_allowed_profiles = set()
    for profile_input in allowed_profiles_input:
        if isinstance(profile_input, PerfilEnum):
            processed_allowed_profiles.add(profile_input.value)
        elif isinstance(profile_input, str):
            processed_allowed_profiles.add(profile_input)
        else:
            # This case should ideally not happen if type hints are followed
            # or could raise a TypeError during decorator definition.
            # For robustness, convert to string or log a warning.
            processed_allowed_profiles.add(str(profile_input))

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_lead_id_str = get_jwt_identity()

            if not current_lead_id_str: # Should not happen if verify_jwt_in_request succeeds
                abort(401) # Unauthorized - no identity in token

            try:
                # Convert the string ID from JWT to a UUID object for querying
                lead_id = uuid.UUID(current_lead_id_str)
            except ValueError:
                # If the JWT identity is not a valid UUID string
                abort(400) # Bad Request - invalid identity format

            with get_session() as session: # type: Session
                try:
                    lead = session.query(Lead).filter(Lead.id == lead_id).first()

                    if not lead:
                        # Lead not found for the given ID in JWT
                        abort(403) # Forbidden (or 401/404 depending on policy)

                    lead_profile_names = set()
                    # Ensure relationships are loaded or queried correctly
                    # Assuming 'permissoes_lead' and 'perfil' are correctly configured relationships
                    for permissao_lead in lead.permissoes_lead:
                        if permissao_lead.perfil and permissao_lead.perfil.nome:
                            lead_profile_names.add(permissao_lead.perfil.nome)
                    
                    # Check for intersection
                    if not processed_allowed_profiles.intersection(lead_profile_names):
                        abort(403) # Forbidden - lead does not have any of the required profiles

                except Exception as e:
                    # Consider logging the exception e for debugging
                    # print(f"Error during permission check: {e}") # For debugging
                    abort(500) # Internal server error if DB query or other logic fails

            return f(*args, **kwargs)
        return wrapper
    return decorator
