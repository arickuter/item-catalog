from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Items, Base

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Soccer category
category1 = Categories(name="Soccer")

session.add(category1)
session.commit()

items1 = Items(title="Soccer ball", description="Limited edition ball", categories=category1)

session.add(items1)
session.commit()

################

# Basketball category
category1 = Categories(name="Basketball")

session.add(category1)
session.commit()

items1 = Items(title="Basket ball", description="Limited edition ball", categories=category1)

session.add(items1)
session.commit()

################

# Baseball category
category1 = Categories(name="Baseball")

session.add(category1)
session.commit()

items1 = Items(title="Baseball bat", description="Limited edition bat", categories=category1)

session.add(items1)
session.commit()

################

# Frisbee category
category1 = Categories(name="Frisbee")

session.add(category1)
session.commit()

items1 = Items(title="Frisbee", description="Limited edition frisbee", categories=category1)

session.add(items1)
session.commit()

################

# Snowboarding category
category1 = Categories(name="Snowboarding")

session.add(category1)
session.commit()

items1 = Items(title="Snowboard", description="Limited edition snowboard", categories=category1)

session.add(items1)
session.commit()

################

# Rock Climbing category
category1 = Categories(name="Rock Climbing")

session.add(category1)
session.commit()

items1 = Items(title="Rope", description="200ft of rope", categories=category1)

session.add(items1)
session.commit()

################

# Foosball category
category1 = Categories(name="Foosball")

session.add(category1)
session.commit()

items1 = Items(title="Table", description="Limited edition table", categories=category1)

session.add(items1)
session.commit()

################

# Skating category
category1 = Categories(name="Skating")

session.add(category1)
session.commit()

items1 = Items(title="Skateboard", description="Limited edition skateboard", categories=category1)

session.add(items1)
session.commit()

################

# Hockey category
category1 = Categories(name="Hockey")

session.add(category1)
session.commit()

items1 = Items(title="Hockey stick", description="Limited edition stick", categories=category1)

session.add(items1)
session.commit()

################

print "added menu items!"
