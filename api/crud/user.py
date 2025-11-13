from fastapi import HTTPException
from sqlmodel import SQLModel, Session, select

from api.models.accounts import UserGroup, User
from api.schemas.user import UserColumn


def update_user(session: Session, target: str, updated_model: SQLModel):
    db_user = session.exec(select(User).where(getattr(User, 'name') == target)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f'User {target} not found')
    updated_model_data = updated_model.dict(exclude_unset=True)
    for key, value in updated_model_data.items():
        if key == UserColumn.group:
            db_group = session.exec(select(UserGroup).where(UserGroup.name == value)).first()
            if not db_group:
                raise HTTPException(status_code=404, detail=f'Group {value} not found')
            setattr(db_user, key, db_group)
        else:
            setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user
