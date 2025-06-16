from typing import List

from fastapi import APIRouter, Depends, Query, Body
from sqlmodel import Session

from api.crud.base import retrieve_models, retrieve_model, create_model, delete_model
from api.crud.user import update_user
from api.dependencies import get_session
from api.models.accounts import User
from api.schemas.user import RetrievedUser, CreatedUserBody, UpdatedUserBody, RetrieveUsersQuery
from .common import filtering_queries_to_schemas, ordering_query_to_schema, grouping_query_to_schema

router = APIRouter()


@router.get('/list/', response_model=List[RetrievedUser])
async def get_users(
    session: Session = Depends(get_session), retrieve_users_query: RetrieveUsersQuery = Query(RetrieveUsersQuery())
) -> List[RetrievedUser]:
    filtering_queries = filtering_queries_to_schemas(retrieve_users_query.filtering)
    ordering_query = ordering_query_to_schema(retrieve_users_query.ordering)
    grouping_query = grouping_query_to_schema(retrieve_users_query.grouping)
    return retrieve_models(
        session, User, retrieve_users_query.columns, retrieve_users_query.offset, retrieve_users_query.limit,
        filtering_queries, ordering_query, grouping_query
    )


@router.get('/{target}', response_model=RetrievedUser)
async def get_user(
    target: str, session: Session = Depends(get_session)
) -> RetrievedUser:
    return retrieve_model(session, User, 'name', target)


@router.post('/list/', response_model=RetrievedUser)
async def create_user(
    created_user_body: CreatedUserBody = Body(CreatedUserBody()), session: Session = Depends(get_session)
) -> RetrievedUser:
    return create_model(session, User, created_user_body)


@router.put('/{target}', response_model=RetrievedUser)
async def update_user(
    target: str, updated_user_body: UpdatedUserBody = Body(UpdatedUserBody()), session: Session = Depends(get_session)
) -> RetrievedUser:
    return update_user(session, target, updated_user_body)


@router.delete('/{target}')
async def delete_user(target: str, session: Session = Depends(get_session)) -> dict:
    return delete_model(session, User, 'name', target)
