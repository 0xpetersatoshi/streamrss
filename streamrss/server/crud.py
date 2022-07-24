from ast import pattern
from sqlalchemy.orm import Session
from streamrss.server import models, schemas


def create_rule(db: Session, rule: schemas.RulesCreate):
    db_rule = models.Rules(pattern=rule.pattern, tag=rule.tag)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule