import hashlib
import base64
from datetime import datetime
import os

from fastapi import APIRouter, Depends, status, HTTPException, Header, Body
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.user.models import user
from app.user.schemas import UserCreate, UserRead

router = APIRouter(
    prefix="",
    tags=["user"]
)

async def decode_auth_header(auth: str = Header(...)) -> str:
    if not auth.startswith('Basic '):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Authentication Failed"
            }
        )

    encoded_credentials = auth.split(" ")[1]  
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
    user_id, _, password = decoded_credentials.partition(':')

    return user_id, password


async def get_by_user_id(user_id: str, session: AsyncSession = Depends(get_async_session)) -> UserRead:
    query = select(user).filter(user.c.user_id == user_id, user.c.deleted == False)
    result = await session.execute(query)

    return result.first()


async def get_password_hash(password: str) -> str:
    # Generate a random salt
    salt = os.urandom(16)
    # Combine password and salt, and then hash
    salted_password = password.encode('utf-8') + salt
    password_hash = hashlib.sha256(salted_password).hexdigest()
    stored_password = salt.hex() + '$' + password_hash

    return stored_password


def verify_password(stored_password: str, provided_password: str) -> bool:
    # Split the stored password into salt and hash
    salt_hex, stored_hash = stored_password.split('$')
    salt = bytes.fromhex(salt_hex)
    # Hash the provided password with the retrieved salt
    salted_password = provided_password.encode('utf-8') + salt
    provided_password_hash = hashlib.sha256(salted_password).hexdigest()
    # Compare hashes
    return provided_password_hash == stored_hash


# Create an account
@router.post("/signup", status_code=status.HTTP_200_OK)
async def add_user(new_user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    if not new_user.user_id or not new_user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Account creation failed",
                "cause": "required user_id and password"
            }
        )
    
    db_user = await get_by_user_id(new_user.user_id, session)
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Account creation failed",
                "cause": "already same user_id is used"
            }
        )

    password_hash = await get_password_hash(new_user.password)
    stmt = insert(user).values(
        user_id=new_user.user_id,
        nickname=new_user.user_id,
        password_hash=password_hash,
        comment="",
        created_at=datetime.now()
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "message": "Account successfully created",
        "user": {
            "user_id": new_user.user_id,
            "nickname": new_user.user_id
        }
    }


#return the user information
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_specific_operations(user_id: str, credentials: tuple = Depends(decode_auth_header), session: AsyncSession = Depends(get_async_session)):
    auth_user_id, password = credentials

    # Ensure user_id in URL matches user_id in Authorization header
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Authentication Failed"
            }
        )
    
    # Fetch user from the database
    db_user = await get_by_user_id(auth_user_id, session)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No User found"
            }
        )

    # Validate password
    is_valid = verify_password(db_user.password_hash, password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Authentication Failed"
            }
        )

    res_user = {"user_id": db_user.user_id, "nickname": db_user.nickname}
    if db_user.comment is not None:
        res_user["comment"] = user.comment

    return {
        "message": "User details by user_id",
        "user": res_user
    }



# Update user information
@router.patch("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_specific_operations(user_id: str, nickname: str = Body(...), comment: str = Body(...), password: str = Body(...), credentials: tuple = Depends(decode_auth_header), session: AsyncSession = Depends(get_async_session)):
    if nickname is None and comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "User updation failed",
                "cause": "required nickname or comment"
            }
        )

    if password is not "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "User updation failed",
                "cause": "not updatable user_id and password"
            }
        )

    auth_user_id, password = credentials

    # Fetch user from the database
    db_user = await get_by_user_id(auth_user_id, session)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No User found"
            }
        )

    # Validate password
    is_valid = verify_password(db_user.password_hash, password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Authentication Failed"
            }
        )

    # Ensure user_id in URL matches user_id in Authorization header
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "No Permission for Update"
            }
        )

    if nickname is None:
        nickname = db_user.user_id

    stmt = (
        update(user)
        .values(
            nickname=nickname,
            comment=comment
        )
        .where(user.c.user_id == user_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "message": "User successfully updated",
        "recipe": [
            {
                "nickname": nickname,
                "comment": comment
            }
        ]
    }


# Delete an account
@router.post("/close", status_code=status.HTTP_200_OK)
async def get_specific_operations(user_id: str, credentials: tuple = Depends(decode_auth_header), session: AsyncSession = Depends(get_async_session)):
    auth_user_id, password = credentials

    # Fetch user from the database
    db_user = await get_by_user_id(auth_user_id, session)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No User found"
            }
        )

    # Validate password
    is_valid = verify_password(db_user.password_hash, password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Authentication Failed"
            }
        )

    # Update a DB - mark the record deleted:
    stmt = (
        update(user)
        .values(deleted=True)
        .where(user.c.user_id == db_user.user_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "message": "Account and user successfully removed"
    }

