import os
def oauthCred():
    GOOGLE_LOGIN_CLIENT_ID = os.environ.get("<your-id-ending-with>.apps.googleusercontent.com_GOOGLE_CLIENT_ID", None)
    GOOGLE_LOGIN_CLIENT_SECRET = os.environ.get("<your-secret>_GOOGLE_CLIENT_SECRET", None)

    GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

    OAUTH_CREDENTIALS={
            'google': {
                'id': GOOGLE_LOGIN_CLIENT_ID,
                'secret': GOOGLE_LOGIN_CLIENT_SECRET
            }
    }
    return OAUTH_CREDENTIALS

