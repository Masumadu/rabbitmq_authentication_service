

class SharedResponse:
    def signin_unverified_account(self):
        return {
                "status": "error",
                "error": "account unverified"
            }

    def signin_valid_details(self):
        return {
            "access_token": "",
            "refresh_token": ""
        }

    def signin_invalid_details(self):
        return {
            "status": "error",
            "error": "user verification failure. invalid credentials"
        }

    def account_verification_valid_token(self):
        return {
                "status": "success",
                "msg": "account verification successful"
            }

    def account_verification_invalid_token(self):
        return {
            "status": "error",
            "msg": "account verification unsuccessful"
        }
