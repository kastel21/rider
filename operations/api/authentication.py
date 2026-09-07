"""JWT auth that can resolve a user by username when the token user_id is stale."""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class RiderJWTAuthentication(JWTAuthentication):
    """
    Standard SimpleJWT lookup by user_id, then username claim.

    Android may mint or reuse a token whose user_id does not match MSSQL
    (local SQLite ids before import). Cloud-issued tokens include username
    so apply-sync still authenticates after a rider signs in again.
    """

    def get_user(self, validated_token):
        try:
            return super().get_user(validated_token)
        except (AuthenticationFailed, InvalidToken):
            username = validated_token.get("username")
            if not username:
                raise
            user = self.user_model.objects.filter(username=str(username)).first()
            if user is None or not user.is_active:
                raise
            return user
