
from app.common.database.objects import DBActivity

import app

def create(
    user_id: int,
    mode: int,
    text: str,
    args: str,
    links: str
) -> DBActivity:
    with app.session.database.managed_session() as session:
        session.add(
            ac := DBActivity(
                user_id,
                mode,
                text,
                args,
                links
            )
        )
        session.commit()
        session.refresh(ac)

    return ac

# TODO: fetch_many
