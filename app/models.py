"""Database schema setup with line-by-line explanations."""  # Module docstring.

from sqlalchemy import Column, Integer, String, MetaData, Table  # Import table utilities.

metadata = MetaData()  # Create metadata container.

monitors = Table(  # Define the monitors table.
    "monitors",  # Table name.
    metadata,  # Attach metadata.
    Column("id", Integer, primary_key=True),  # Primary key column.
    Column("name", String(200), nullable=False),  # Monitor name.
    Column("url", String(500), nullable=False),  # Monitor URL.
    Column("interval_seconds", Integer, nullable=False),  # Polling interval.
)  # End table definition.
