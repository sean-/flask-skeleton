from sqlalchemy import Table

from skeleton.database import metadata

# Note the conflicting variable and table name. autoload works well for basic
# models but should be reserved for cases of laziness.
H1 = Table('h1', metadata, autoload=True, schema='mod1')
