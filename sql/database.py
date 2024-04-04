from sqlalchemy import create_engine
from sql.models import metadata

from config import settings

engine = create_engine(url=settings.database_url, echo=True)

# with engine.connect() as conn:
#     res = conn.execute(text('select version()'))
#     print(res.first())
