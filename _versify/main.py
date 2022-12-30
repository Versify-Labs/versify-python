import logging
import os
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

import pymongo
from fastapi import (Body, Cookie, Depends, FastAPI, Header, HTTPException,
                     Path, Query, Request, status)
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from pydantic.utils import deep_update
from pymongo.collection import DeleteResult, InsertOneResult, UpdateResult
from pymongo.results import InsertOneResult, UpdateResult
from fastapi.middleware.cors import CORSMiddleware

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "cD8A6WFjMANXtFvp8HcrEvEuE5sluz1v09d25e094faa6ca2556c818166b7a956"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


"""
Mock database
"""

fake_accounts_db = [
    {
        "id": "acct_1",
        "name": "Acme",
    },
    {
        "id": "acct_2",
        "name": "Versify",
    },
]
fake_contacts_db = [
    {
        "id": "cont_1",
        "account": "acct_1",
        "name": "Jane",
        "email": "jane@example.com"
    },
    {
        "id": "cont_2",
        "account": "acct_1",
        "name": "John",
        "email": "john@example.com"
    },
    {
        "id": "cont_3",
        "account": "acct_2",
        "name": "Troy",
        "email": "troy@example.com"
    }
]
fake_users_db = {
    "john@example.com": {
        "active": True,
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    },
    "alice@example.com": {
        "active": False,
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Wonderland",
        "password_hash": "fakehashedsecret2"
    },
}


"""
Versify Services Classes
"""


class Versify:
    def __init__(self, db_url=None) -> None:

        # TODO: Remove
        if not db_url:
            db_url = 'versifydevelopmentclust.y5nxv.mongodb.net'

        # Connect to MongoDB Atlas
        db_url = db_url or os.environ.get('MONGO_DB_URL')
        if not db_url:
            raise ValueError('MONGO_DB_URL not set')

        self.connection_str = f"mongodb+srv://{db_url}/?authSource=$external&authMechanism=MONGODB-AWS&retryWrites=true&w=majority"
        self.cluster = pymongo.MongoClient(self.connection_str)

        # Get db collections
        self.account_collection = self.cluster['Accounts']['Accounts']
        self.contact_collection = self.cluster['Contacts']['Contacts']
        self.user_collection = self.cluster['Accounts']['Users']

    def create_account(self, body: Dict[str, Any]) -> InsertOneResult:
        return self.account_collection.insert_one(body)

    def list_accounts(self) -> List[Dict[str, Any]]:
        return list(self.account_collection.find())

    def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        return self.account_collection.find_one({'_id': account_id})

    def update_account(self, account_id: str, body: Dict[str, Any]) -> UpdateResult:
        return self.account_collection.update_one({'_id': account_id}, {'$set': body})

    def delete_account(self, account_id: str) -> DeleteResult:
        return self.account_collection.delete_one({'_id': account_id})

    def create_contact(self, body: Dict[str, Any]) -> InsertOneResult:
        return self.contact_collection.insert_one(body)

    def list_contacts(self) -> List[Dict[str, Any]]:
        return list(self.contact_collection.find())

    def get_contact(self, contact_id: str) -> Optional[Dict[str, Any]]:
        return self.contact_collection.find_one({'_id': contact_id})

    def update_contact(self, contact_id: str, body: Dict[str, Any]) -> UpdateResult:
        return self.contact_collection.update_one({'_id': contact_id}, {'$set': body})

    def delete_contact(self, contact_id: str) -> DeleteResult:
        return self.contact_collection.delete_one({'_id': contact_id})

    def create_user(self, body: Dict[str, Any]) -> InsertOneResult:
        return self.user_collection.insert_one(body)

    def list_users(self) -> List[Dict[str, Any]]:
        return list(self.user_collection.find())

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.user_collection({'_id': user_id})

    def update_user(self, user_id: str, body: Dict[str, Any]) -> UpdateResult:
        return self.user_collection.update_one({'_id': user_id}, {'$set': body})

    def delete_user(self, user_id: str) -> DeleteResult:
        return self.user_collection.delete_one({'_id': user_id})

    def close(self) -> None:
        self.cluster.close()


"""
Versify Metadata Classes
"""


class Tags(Enum):
    ACCOUNT = 'Account'
    CONTACT = 'Contact'
    USER = 'User'


class BodyParams:
    CREATE_ACCOUNT = Body(
        ...,
        title="Account",
        description="Account to create",
        example={
            "name": "Acme"
        }
    )
    CREATE_CONTACT = Body(
        ...,
        title="Contact",
        description="Contact to create",
        example={
            "email": "jane@example.com",
            "first_name": "Jane",
            "last_name": "Doe"
        }
    )
    CREATE_USER = Body(
        ...,
        title="User",
        description="User to create",
        example={
            "name": "Acme",
            "first_name": "Jane",
            "last_name": "Doe"
        }
    )
    UPDATE_ACCOUNT = Body(
        ...,
        title="Account",
        description="Account to update",
        example={
            "name": "Acme",
        }
    )
    UPDATE_CONTACT = Body(
        ...,
        title="Contact",
        description="Contact to update",
        example={
            "email": "jane@example.com",
            "first_name": "Jane",
            "last_name": "Doe"
        }
    )
    UPDATE_USER = Body(
        ...,
        title="User",
        description="User to update",
        example={
            "avatar": "https://example.com/avatar.png",
            "first_name": "Jane",
            "last_name": "Doe"
        }
    )


class CookieParams:
    SESSION_ID = Cookie(
        ...,
        title="Session ID",
        description="ID of the session",
        example="sess_1"
    )


class HeaderParams:
    AUTHORIZATION = Header(
        ...,
        title="Authorization",
        description="Authorization header",
        example="Bearer ey......",
    )
    CONTENT_TYPE = Header(
        ...,
        title="Content Type",
        description="Content type header",
        example="application/json",
    )
    USER_AGENT = Header(
        ...,
        title="User Agent",
        description="User agent header",
        example="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    )
    X_REQUEST_ID = Header(
        ...,
        title="Request ID",
        description="Request ID header",
        example="req_1",
    )


class PathParams:
    ACCOUNT_ID = Path(
        ...,
        title="Account ID",
        description="ID of the account",
        example="acct_1"
    )
    CONTACT_ID = Path(
        ...,
        title="Contact ID",
        description="ID of the contact",
        example="cont_1"
    )
    USER_ID = Path(
        ...,
        title="User ID",
        description="ID of the user",
        example="user_1"
    )


class QueryParams:
    ACTIVE = Query(
        default=None,
        title="Active",
        description="Whether the item is active",
        example=True
    )
    EMAIL = Query(
        default=None,
        title="Email",
        description="Email of the item to return",
        example="jane@example.com"
    )
    LIMIT = Query(
        default=10,
        ge=1,
        le=100,
        title="Limit amount",
        description="Number of items to return",
        example=10
    )
    SKIP = Query(
        default=0,
        ge=0,
        title="Skip amount",
        description="Number of items to skip",
        example=10
    )
    Q = Query(
        default=None,
        title="Search query",
        description="Query to filter items",
        example="Acme",
        min_length=1,
        max_length=100
    )


"""
Versify API Dependencies
"""


class ListQueryParams:
    def __init__(
        self,
        limit: int = 100,
        skip: int = 0,
        q: Union[str, None] = None
    ):
        self.limit = limit
        self.skip = skip
        self.q = q


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_from_db(db, email: str):
    if email in db:
        user_dict = db[email]
        return User(**user_dict)


def authenticate_user(fake_db, email: str, password: str):
    user = get_user_from_db(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def log_request(
    request: Request,
    user_agent: str = HeaderParams.USER_AGENT,
    x_request_id: str = HeaderParams.X_REQUEST_ID,
):
    logging.info(
        f"{request.method} {request.url} {user_agent} {x_request_id}"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_from_db(fake_users_db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_user_for_account(
    current_user: User = Depends(get_current_active_user),
    account_id: str = PathParams.ACCOUNT_ID
):
    # Check if the user is a member of the account
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    role = None
    for account in current_user.accounts:
        if account.id == account_id:
            for teammate in account.team:
                if teammate.email == current_user.email:
                    role = teammate.role
    if not role:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


"""
Versify API
"""

__version__ = "v2"

app = FastAPI(
    title="Versify API",
    version=__version__,
    openapi_url="/openapi.json",
    docs_url="/docs",
    # dependencies=[Depends(log_request)],
)
versify = Versify(db_url="")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://.*\.versifylabs\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post(
    path="/accounts",
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.ACCOUNT],
    summary="Create an account",
    description="Create an account",
    response_model=Account,
    response_description="The created account",
    # dependencies=[Depends(verify_auth_token)],
)
async def create_account(
    authorization: str = HeaderParams.AUTHORIZATION,
    account_body: AccountInput = BodyParams.CREATE_ACCOUNT,
    token: str = Depends(oauth2_scheme),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    account_body_encoded = jsonable_encoder(account_body)
    account_output = versify.create_account(account_body_encoded)
    return account_output


@app.get(
    path="/accounts",
    status_code=status.HTTP_200_OK,
    tags=[Tags.ACCOUNT],
    summary="List accounts",
    description="List accounts with optional filters and pagination parameters",
    response_model=List[Account],
    response_description="The list of accounts",
    # dependencies=[Depends(verify_auth_token)],
)
async def list_accounts(
    authorization: str = HeaderParams.AUTHORIZATION,
    active: Optional[bool] = QueryParams.ACTIVE,
    email: Union[EmailStr, None] = QueryParams.EMAIL,
    # commons: ListQueryParams = Depends()
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if email:
        return [account for account in fake_accounts_db if account['email'] == email]
    # return fake_accounts_db[commons.skip: commons.skip + commons.limit]
    return []


@app.get(
    path="/accounts/{account_id}",
    status_code=status.HTTP_200_OK,
    tags=[Tags.ACCOUNT],
    summary="Get an account",
    description="Get an account by ID",
    response_model=Account,
    response_description="The account",
    # dependencies=[Depends(verify_auth_token)],
)
async def get_account(
    authorization: str = HeaderParams.AUTHORIZATION,
    account_id: str = PathParams.ACCOUNT_ID
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if account_id not in [account['id'] for account in fake_accounts_db]:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id}


@app.put(
    path="/accounts/{account_id}",
    status_code=status.HTTP_200_OK,
    tags=[Tags.ACCOUNT],
    summary="Update an account",
    description="Update an account by ID",
    response_model=Account,
    response_description="The updated account",
    # dependencies=[Depends(verify_auth_token)],
)
async def update_account(
    authorization: str = HeaderParams.AUTHORIZATION,
    account_id: str = PathParams.ACCOUNT_ID,
    account_body: AccountInput = BodyParams.UPDATE_ACCOUNT
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if account_id not in [account['id'] for account in fake_accounts_db]:
        raise HTTPException(status_code=404, detail="Account not found")
    account_body_encoded = jsonable_encoder(account_body)
    account_output = versify.update_account(account_id, account_body_encoded)
    return account_output


@app.post(
    path="/accounts/{account_id}/contacts",
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.CONTACT],
    summary="Create a contact",
    description="Create a contact for an account by ID",
    response_model=Contact,
    response_description="The created contact",
    # dependencies=[Depends(verify_auth_token)],
)
async def create_account_contact(
    authorization: str = HeaderParams.AUTHORIZATION,
    account_id: str = PathParams.ACCOUNT_ID,
    contact_body: Contact = BodyParams.CREATE_CONTACT
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if account_id not in [account['id'] for account in fake_accounts_db]:
        raise HTTPException(status_code=404, detail="Account not found")
    contact_body_encoded = jsonable_encoder(contact_body)
    contact_body_encoded['account'] = account_id
    contact_output = versify.create_contact(contact_body_encoded)
    return contact_output


@app.get(
    path="/accounts/{account_id}/contacts",
    status_code=status.HTTP_200_OK,
    tags=[Tags.CONTACT],
    summary="List contacts",
    description="List contacts with optional filters and pagination parameters",
    response_model=List[Contact],
    response_description="The list of contacts",
    # dependencies=[Depends(verify_auth_token)],
)
async def list_account_contacts(
    authorization: str = HeaderParams.AUTHORIZATION,
    account_id: str = PathParams.ACCOUNT_ID,
    active: Union[bool, None] = QueryParams.ACTIVE,
    email:  Union[EmailStr, None] = QueryParams.EMAIL,
    commons: ListQueryParams = Depends(),
    # dependencies=[Depends(verify_auth_token)],
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if account_id not in [account['id'] for account in fake_accounts_db]:
        raise HTTPException(status_code=404, detail="Account not found")
    filter = {
        'account': account_id,
        'active': active
    }
    if active is not None:
        filter['active'] = active
    if email:
        filter['email'] = email
    if commons.q:
        filter['email'] = commons.q
    return fake_contacts_db[commons.skip: commons.skip + commons.limit]


@app.get(
    path="/accounts/{account_id}/contacts/{contact_id}",
    status_code=status.HTTP_200_OK,
    tags=[Tags.CONTACT],
    summary="Get a contact",
    description="Get a contact for an account by ID",
    response_model=Contact,
    response_description="The contact",
    # dependencies=[Depends(verify_auth_token)],
)
async def get_account_contact(
    authorization: str = HeaderParams.AUTHORIZATION,
    account_id: str = PathParams.ACCOUNT_ID,
    contact_id: str = PathParams.CONTACT_ID,
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if account_id not in [account['id'] for account in fake_accounts_db]:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account": account_id, "contact": contact_id}


@app.put(
    path="/accounts/{account_id}/contacts/{contact_id}",
    status_code=status.HTTP_200_OK,
    tags=[Tags.CONTACT],
    summary="Update a contact",
    description="Update a contact for an account by ID",
    response_model=Contact,
    response_description="The updated contact",
    # dependencies=[Depends(verify_auth_token)],
)
async def update_account_contact(
    authorization: str = HeaderParams.AUTHORIZATION,
    account_id: str = PathParams.ACCOUNT_ID,
    contact_id: str = PathParams.CONTACT_ID,
    contact_body: Contact = BodyParams.UPDATE_CONTACT
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if account_id not in [account['id'] for account in fake_accounts_db]:
        raise HTTPException(status_code=404, detail="Account not found")
    contact_body_encoded = jsonable_encoder(contact_body)
    contact_output = versify.update_contact(contact_id, contact_body_encoded)
    return contact_output


@app.post(
    path="/token",
    response_model=Token,
    tags=[Tags.USER],
    summary="Login for access token",
    description="Login for access token",
    response_description="The access token",
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    path="/users/me",
    status_code=status.HTTP_200_OK,
    tags=[Tags.USER],
    summary="Get current user",
    description="Get current user by ID",
    # response_model=User,
    response_description="The current user",
    # dependencies=[Depends(verify_auth_token)],
)
async def get_user_me(
    # authorization: str = HeaderParams.AUTHORIZATION,
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_active_user)
):
    print(token)
    print(current_user)
    return current_user


@app.get(
    path="/users/{user_id}",
    status_code=status.HTTP_200_OK,
    tags=[Tags.USER],
    summary="Get a user",
    description="Get a user by ID",
    response_model=User,
    response_description="The user",
    # dependencies=[Depends(verify_auth_token)],
)
async def get_user(
    authorization: str = HeaderParams.AUTHORIZATION,
    user_id: str = PathParams.USER_ID
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user_id": user_id}
