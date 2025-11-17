from __future__ import annotations

from uuid import UUID

from fastapi import Header, HTTPException, status


def get_current_user_id(authorization: str | None = Header(default=None)) -> UUID:
    """Temporary auth dependency until the real JWT service is wired."""

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
        )

    token = authorization.split(" ", 1)[1].strip()
    try:
        return UUID(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
        ) from exc


__all__ = ["get_current_user_id"]
