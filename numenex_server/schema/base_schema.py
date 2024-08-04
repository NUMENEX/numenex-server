import uuid
from datetime import datetime


class DatabaseMixin:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
