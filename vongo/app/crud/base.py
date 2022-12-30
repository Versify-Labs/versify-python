from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.db.base_class import Base
from app.db.session import SessionLocal
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo.database import Database

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

session = SessionLocal()


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        # db_name = model.db_name
        # collection_name = model.collection_name
        db_name = 'Dev'
        collection_name = 'Users'
        self.collection = session.get_collection(db_name, collection_name)

    def get(self, id: Any) -> Optional[ModelType]:
        return self.collection.find_one({'_id': id})

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:

        return self.collection.find({}).skip(skip).limit(limit)

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.collection.insert_one(db_obj)  # type: ignore
        return db_obj

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.collection.find_one_and_update(
            filter={'_id': db_obj.id},
            update={'$set': db_obj},
            upsert=True
        )
        return db_obj

    def remove(self, *, id: int) -> ModelType:
        obj = self.collection.find_one_and_delete({'_id': id})
        return obj
