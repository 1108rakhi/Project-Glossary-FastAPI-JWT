from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from models import model
from databases import database
from schemas import schema
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from routers.users import decode_token

router = APIRouter()

def check_name(authorization : str , role_access: str = 'admin'):
    if not authorization:
        raise HTTPException(status_code=401, detail='Invalid authorization')
    
    role_check = decode_token(authorization)
    return role_check.get('sub')

#creating glossaries
@router.post('/glossary', response_model=schema.GlossaryResponse)
def create_glossary(create:schema.CreateGlossary, db : Session=Depends(database.get_db),current_user:str = Depends(check_name)):
    new_term = model.Glossary(
        term = create.term,
        description = create.description,
        created_by = current_user
        
    )
    db.add(new_term)
    db.commit()
    db.refresh(new_term)
    return new_term


@router.get('/glossary', response_model=list[schema.GlossaryResponse])
def get_glossary(id:int|None = Query(None), db:Session=Depends(database.get_db)):
    glossary = db.query(model.Glossary)
    if id:
        glossary = glossary.filter(model.Glossary.id==id)
    all_terms = glossary.all()
    return all_terms


# updating glossaries
@router.put('/glossary/{id}', response_model=schema.GlossaryResponse)
def update_glossary(id: int, update:schema.UpdateGlossary, db:Session = Depends(database.get_db),current_user:str = Depends(check_name)):
    upd_glossary = db.query(model.Glossary).filter(model.Glossary.id == id).first()
    if not upd_glossary:
        raise HTTPException(status_code=404, detail='Term not found')
    upd_glossary.term = update.term
    upd_glossary.description = update.description
    upd_glossary.updated_by = current_user
    db.commit()
    db.refresh(upd_glossary)
    return upd_glossary

@router.delete('/glossary/{id}')
def delete_glossary(id: int, db: Session = Depends(database.get_db)):
    del_glossary = db.query(model.Glossary).filter(model.Glossary.id == id).first()
    if not del_glossary:
        raise HTTPException(status_code= 404, detail='Term does not exist')
    db.delete(del_glossary)
    db.commit()
    # db.refresh(del_glossary)
    return {'message':'term deleted successfully'}


