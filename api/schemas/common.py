from enum import Enum
from typing import Any, List, Optional

from sqlmodel import SQLModel, Field


class MathematicalSign(str, Enum):
    eq: str = 'eq'
    gt: str = 'gt'
    gte: str = 'gte'
    lt: str = 'lt'
    lte: str = 'lte'


class OrderingOption(str, Enum):
    ascending: str = 'ascending'
    descending: str = 'descending'


class AggregationOption(str, Enum):
    count: str = 'count'
    sum: str = 'sum'
    avg: str = 'avg'
    var: str = 'var'
    stddev: str = 'stddev'
    max: str = 'max'
    min: str = 'min'
    median: str = 'median'
    mode: str = 'mode'


class FilteringQuery(SQLModel):
    column: Enum
    mathematical_sign: MathematicalSign
    value: Any


class OrderingQuery(SQLModel):
    by: List[Enum]
    option: OrderingOption = Field(default=OrderingOption.ascending)


class GroupedColumn(SQLModel):
    column: Enum
    aggregation_option: AggregationOption


class GroupingQuery(SQLModel):
    by: List[Enum]
    columns: List[GroupedColumn]


class RetrieveModelsQuery(SQLModel):
    offset: int = Field(default=0, gte=0)
    limit: int = Field(default=100, gt=0, lte=100)
    columns: Optional[List[Enum]] = Field(default=None)
    filtering: Optional[str] = Field(default=None)
    ordering: Optional[str] = Field(default=None)
    grouping: Optional[str] = Field(default=None)


class RetrieveModelQuery(SQLModel):
    columns: List[Enum] = Field(default=None)
