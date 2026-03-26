from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, MetaData, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, registry, relationship

from domain.entities import Profile, User


metadata_obj = MetaData()
mapper_registry = registry(metadata=metadata_obj)


user_table = Table(
    "entity_user",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("created_date", DateTime, nullable=False),
    Column("updated_date", DateTime, nullable=False)
)


profile_table = Table(
    "entity_profile",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey(user_table.c.id), default=uuid4, nullable=False),
    Column("name", String(255), nullable=False),
    Column("last_name", String(255), nullable=True),
    Column("avatar", String, nullable=True),
    Column("description", Text, nullable=True),
    Column("readme", Text, nullable=True),
    Column("created_date", DateTime, nullable=False),
    Column("updated_date", DateTime, nullable=False)
)


mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "created_date": user_table.c.created_date,
        "updated_date": user_table.c.updated_date
    }
)


mapper_registry.map_imperatively(
    Profile,
    profile_table,
    properties={
        "user": relationship(
            User,
            backref=backref("entity_profile", uselist=False),
            lazy="selectin"
        ),
        "created_date": profile_table.c.created_date,
        "updated_date": profile_table.c.updated_date
    }
)