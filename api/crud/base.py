from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import SQLModel, Session, select, func

from api.schemas.common import MathematicalSign, AggregationOption, FilteringQuery, OrderingQuery, OrderingOption, GroupingQuery
from api.schemas.user import UserColumn


def _filter_models(model: type[SQLModel], statement, filtering_queries: List[FilteringQuery]):
    for filtering_query in filtering_queries:
        if filtering_query.mathematical_sign == MathematicalSign.eq:
            statement = statement.where(getattr(model, filtering_query.column) == filtering_query.value)
        elif filtering_query.mathematical_sign == MathematicalSign.gt:
            statement = statement.where(getattr(model, filtering_query.column) > filtering_query.value)
        elif filtering_query.mathematical_sign == MathematicalSign.gte:
            statement = statement.where(getattr(model, filtering_query.column) >= filtering_query.value)
        elif filtering_query.mathematical_sign == MathematicalSign.lt:
            statement = statement.where(getattr(model, filtering_query.column) < filtering_query.value)
        elif filtering_query.mathematical_sign == MathematicalSign.lte:
            statement = statement.where(getattr(model, filtering_query.column) <= filtering_query.value)
        else:
            raise ValueError('Invalid filtering query was given')
    return statement


def _order_models(model: type[SQLModel], statement, ordering_query: OrderingQuery):
    if ordering_query.option == OrderingOption.ascending:
        statement = statement.order_by(*[getattr(model, column) for column in ordering_query.by])
    elif ordering_query.option == OrderingOption.descending:
        statement = statement.order_by(*[getattr(model, column) for column in ordering_query.by].desc())
    return statement


def _group_models(model: type[SQLModel], statement, grouping_query: GroupingQuery):
    agg_funcs = []
    for grouped_column in grouping_query.columns:
        if grouped_column.aggregation_option == AggregationOption.count:
            agg_funcs.append(func.count(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.sum:
            agg_funcs.append(func.sum(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.avg:
            agg_funcs.append(func.avg(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.var:
            agg_funcs.append(func.var(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.stddev:
            agg_funcs.append(func.stddev(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.max:
            agg_funcs.append(func.max(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.min:
            agg_funcs.append(func.min(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.median:
            agg_funcs.append(func.median(getattr(model, grouped_column.column)).alias(grouped_column.column))
        elif grouped_column.aggregation_option == AggregationOption.mode:
            agg_funcs.append(func.mode(getattr(model, grouped_column.column)).alias(grouped_column.column))
        else:
            raise ValueError('Invalid grouping_query was given')
    statement = statement.group_by(
        *[getattr(model, column) for column in grouping_query.by],
        *agg_funcs
    )
    return statement


def create_model(session: Session, model: type[SQLModel], created_model_body: SQLModel):
    db_model = model.from_orm(created_model_body)
    session.add(db_model)
    session.commit()
    return db_model


def retrieve_models(
        session: Session, model: type[SQLModel], offset: int, limit: int, columns: Optional[List[UserColumn]],
        filtering_queries: Optional[List[FilteringQuery]],
        ordering_query: Optional[OrderingQuery],
        grouping_query: Optional[GroupingQuery]
    ):
    if columns is None:
        statement = select(model)
    else:
        statement = select(*[getattr(model, column) for column in columns])
    if filtering_queries is not None:
        statement = _filter_models(model, statement, filtering_queries)
    if ordering_query is not None:
        statement = _order_models(model, statement, ordering_query)
    if grouping_query is not None:
        statement = _group_models(model, statement, grouping_query)
    statement = statement.offset(offset).limit(limit)
    if columns is None:
        models = session.exec(statement).all()
    else:
        models = [model(**record._asdict()) for record in session.exec(statement).all()]
    return models


def retrieve_model(session: Session, model: type[SQLModel], index_col: str, target: str):
    db_model = session.exec(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    return db_model


def update_model(session: Session, model: type[SQLModel], index_col: str, target: str, updated_model_body: SQLModel):
    db_model = session.exec(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    updated_model_data = updated_model_body.dict(exclude_unset=True)
    for key, value in updated_model_data.items():
        setattr(db_model, key, value)
    session.commit()
    return db_model


def delete_model(session: Session, model: type[SQLModel], index_col: str, target: str):
    db_model = session.exec(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    session.delete(db_model)
    session.commit()
    return {'ok': True}
