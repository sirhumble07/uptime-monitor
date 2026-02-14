"""Initialize the database schema with line-by-line explanations."""  # Module docstring.

from .db import get_engine  # Import engine helper.
from .models import metadata  # Import metadata with table definitions.

engine = get_engine()  # Create engine instance.

metadata.create_all(engine)  # Create tables if they do not exist.
