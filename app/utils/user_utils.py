

# from sqlalchemy import text


# def set_user_schema(session, user_id: str):
#     schema_name = f"user_{user_id}"
#     session.execute(text(f"SET search_path TO {schema_name}"))

# def create_user_schema(user_id: str):
#     schema_name = f"user_{user_id}"
#     with engine.connect() as connection:
#         connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
#         connection.execute(text(f"""
#             CREATE TABLE IF NOT EXISTS {schema_name}.tasks (
#                 id SERIAL PRIMARY KEY,
#                 date DATE NOT NULL,
#                 todolist VARCHAR NOT NULL,
#                 status VARCHAR NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed')),
#                 user_id VARCHAR NOT NULL
#             )
#         """))