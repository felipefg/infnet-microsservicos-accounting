from enum import Enum
from uuid import UUID
from typing import List

from pydantic import BaseModel


class OrderStatus(str, Enum):
    created = 'created'
    approved = 'approved'
    cancelled = 'cancelled'
    done = 'done'


class Order(BaseModel):
    order_id: UUID
    client_id: int
    item_ids: List[int]
    status: OrderStatus = OrderStatus.created
