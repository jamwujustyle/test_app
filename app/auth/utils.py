from fastapi.responses import Response
from ..config.settings import get_settings
import resend


settings = get_settings()


def set_auth_cookies(response: Response, tokens: dict) -> Response:
    response.set_cookie(
        "access_token",
        value=tokens["access_token"],
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 10000000,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        "refresh_token",
        value=tokens["refresh_token"],
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 10000000,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax",
        path="/",
    )

    return response


def clear_auth_cookies(response: Response) -> Response:

    response.delete_cookie(
        "access_token",
        path="/",
        secure=settings.SECURE_COOKIES,
        samesite="lax",
    )

    response.delete_cookie(
        "refresh_token",
        path="/",
        secure=settings.SECURE_COOKIES,
        samesite="lax",
    )

    return response


async def send_verification_email(email: str, code: str):
    """Send verification code via email."""
    try:
        subject = f"Verify your email for {settings.SITE_NAME}"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Welcome to {settings.SITE_NAME}!</h2>
            <p>Your verification code is:</p>
            <h1 style="color: #4CAF50; letter-spacing: 5px;">{code}</h1>
            <p>This code will expire in 15 minutes.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </div>
        """

        resend.api_key = settings.RESEND_API_KEY

        resend.Emails.send(
            {
                "from": settings.FROM_EMAIL,
                "to": email,
                "subject": subject,
                "html": html_content,
            }
        )

        print(f"✅ Verification email sent to {email} with code: {code}")
        return True

    except Exception as ex:
        print(f"❌ Email send failed: {ex}")
        return False
