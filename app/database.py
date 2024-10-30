from sqlalchemy.dialects.postgresql import JSONB, INTEGER, BIGINT, VARCHAR, TIMESTAMP, BOOLEAN, TEXT
from sqlalchemy import create_engine, Column, DECIMAL, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from tools import os, logging

Base = declarative_base()
DBTYPE = os.getenv('DB_TYPE')
LOGIN = os.getenv('DB_LOGIN')
PASS = os.getenv('DB_PASS')
IP = os.getenv('DB_IP')
PORT = os.getenv('DB_PORT')
DBNAME = os.getenv('DB_NAME')
DATABASE_URL = f'{DBTYPE}://{LOGIN}:{PASS}@{IP}:{PORT}/{DBNAME}'


class Offers(Base):
    __tablename__ = 'offers'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    cian_id = Column(BIGINT, nullable=False, unique=True, index=True)
    price = Column(DECIMAL(15, 2), nullable=False)
    category = Column(VARCHAR(255), nullable=True)
    views_count = Column(INTEGER, nullable=True)
    photos_count = Column(INTEGER, nullable=True)
    floor_number = Column(INTEGER, nullable=True)
    floors_сount = Column(INTEGER, nullable=True)
    publication_at = Column(INTEGER, nullable=True)
    price_changes = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    address = relationship("Addresses", back_populates="offer", uselist=False)
    realty_inside = relationship("Realty_inside", back_populates="offer", uselist=False, cascade="all, delete-orphan")
    realty_outside = relationship("Realty_outside", back_populates="offer", uselist=False, cascade="all, delete-orphan")
    realty_details = relationship("Realty_details", back_populates="offer", uselist=False, cascade="all, delete-orphan")
    offers_details = relationship("Offers_details", back_populates="offer", uselist=False, cascade="all, delete-orphan")
    developer = relationship("Developers", back_populates="offer", uselist=False, cascade="all, delete-orphan")


class Addresses(Base):
    __tablename__ = 'addresses'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    cian_id = Column(BIGINT, ForeignKey('offers.cian_id'), index=True)
    county = Column(VARCHAR(255), nullable=True, index=True)
    district = Column(VARCHAR(255), nullable=True, index=True)
    street = Column(VARCHAR(255), nullable=True, index=True)
    house = Column(VARCHAR(255), nullable=True)
    metro = Column(VARCHAR(255), nullable=True)
    travel_type = Column(VARCHAR(255), nullable=True)
    travel_time = Column(INTEGER, nullable=True)
    address = Column(JSONB, nullable=True)
    coordinates = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    offer = relationship("Offers", back_populates="address", uselist=False)


class Realty_inside(Base):
    __tablename__ = 'realty_inside'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    cian_id = Column(BIGINT, ForeignKey('offers.cian_id'), index=True)
    repair_type = Column(VARCHAR(255), nullable=True, index=True)
    total_area = Column(DECIMAL(11, 2), nullable=True, index=True)
    living_area = Column(DECIMAL(11, 2), nullable=True)
    kitchen_area = Column(DECIMAL(11, 2), nullable=True)
    ceiling_height = Column(DECIMAL(11, 2), nullable=True)
    balconies = Column(INTEGER, nullable=True)
    loggias = Column(INTEGER, nullable=True)
    rooms_count = Column(INTEGER, nullable=True)
    separated_wc = Column(INTEGER, nullable=True)
    combined_wc = Column(INTEGER, nullable=True)
    windows_view = Column(VARCHAR(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    offer = relationship("Offers", back_populates="realty_inside", uselist=False)


class Realty_outside(Base):
    __tablename__ = 'realty_outside'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    cian_id = Column(BIGINT, ForeignKey('offers.cian_id'), index=True)
    build_year = Column(INTEGER, nullable=True, index=True)
    entrances = Column(INTEGER, nullable=True)
    material_type = Column(VARCHAR(255), nullable=True)
    parking_type = Column(VARCHAR(255), nullable=True)
    garbage_chute = Column(BOOLEAN, nullable=True)
    lifts_count = Column(INTEGER, nullable=True)
    passenger_lifts = Column(INTEGER, nullable=True)
    cargo_lifts = Column(INTEGER, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    offer = relationship("Offers", back_populates="realty_outside", uselist=False)


class Realty_details(Base):
    __tablename__ = 'realty_details'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    cian_id = Column(BIGINT, ForeignKey('offers.cian_id'), index=True)
    realty_type = Column(VARCHAR(255), nullable=True, index=True)
    project_type = Column(VARCHAR(255), nullable=True)
    heat_type = Column(VARCHAR(255), nullable=True)
    gas_type = Column(VARCHAR(255), nullable=True)
    is_apartment = Column(BOOLEAN, nullable=True)
    is_penthouse = Column(BOOLEAN, nullable=True)
    is_mortgage_allowed = Column(BOOLEAN, nullable=True)
    is_premium = Column(BOOLEAN, nullable=True)
    is_emergency = Column(BOOLEAN, nullable=True)
    renovation_programm = Column(BOOLEAN, nullable=True)
    finish_date = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    offer = relationship("Offers", back_populates="realty_details", uselist=False)


class Offers_details(Base):
    __tablename__ = 'offers_details'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    cian_id = Column(BIGINT, ForeignKey('offers.cian_id'), index=True)
    agent_name = Column(VARCHAR(255), nullable=True)
    deal_type = Column(VARCHAR(255), nullable=True)
    flat_type = Column(VARCHAR(255), nullable=True)
    sale_type = Column(VARCHAR(255), nullable=True)
    is_duplicate = Column(BOOLEAN, nullable=True)
    description = Column(TEXT, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    offer = relationship("Offers", back_populates="offers_details", uselist=False)


class Developers(Base):
    __tablename__ = 'developers'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    cian_id = Column(BIGINT, ForeignKey('offers.cian_id'), index=True)
    name = Column(VARCHAR(255), nullable=True)
    review_count = Column(INTEGER, nullable=True)
    total_rate = Column(DECIMAL(2, 1), nullable=True)
    buildings_count = Column(INTEGER, nullable=True)
    foundation_year = Column(INTEGER, nullable=True)
    is_reliable = Column(BOOLEAN, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text(
        'CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    offer = relationship("Offers", back_populates="developer", uselist=False)


class DatabaseManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, pool_pre_ping=True, future=True)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.create_tables()

    def create_tables(self):
        existing_tables = self.get_existing_tables()
        Base.metadata.create_all(self.engine)

        for table in Base.metadata.sorted_tables:
            if table.name not in existing_tables:
                self.apply_triggers(table)

    def get_existing_tables(self):
        with self.Session() as session:
            connection = session.connection()
            existing_tables = connection.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()
            return {table_name for (table_name,) in existing_tables}

    def apply_triggers(self, table):
        table_name = table.name

        if hasattr(table.c, 'updated_at'):
            trigger_sql = f"""
            CREATE TRIGGER updated_at_trigger
            BEFORE UPDATE ON {table_name}
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at();
            """
            with self.Session() as session:
                connection = session.connection()
                try:
                    connection.execute(text(trigger_sql))
                    session.commit()
                    logging.info(f"Trigger applied to table: {table_name}")
                except SQLAlchemyError as e:
                    session.rollback()
                    logging.error(
                        f"Error applying trigger to table {table_name}: {e}", exc_info=True)
        else:
            logging.info(
                f"No trigger applied to table {table_name} as it lacks updated_at column.")

    def insert(self, *instances):
        with self.Session() as session:
            try:
                session.add_all(instances)
                session.commit()
                logging.info("Insert successful")
            except (IntegrityError, SQLAlchemyError) as e:
                session.rollback()
                if isinstance(e, IntegrityError) and 'duplicate key value violates unique constraint' in str(e.orig):
                    key = str(e.orig).split('Key ')[1].split(')')[0]
                    logging.error(
                        f"Integrity error during insertion: Unique constraint violation for key {key}")
                else:
                    logging.error(f"Error during insertion: {e}", exc_info=True)

    def update(self, model_class, filter_conditions, update_values):
        with self.Session() as session:
            try:
                updated_rows = session.query(model_class).filter_by(
                    **filter_conditions).update(update_values)
                if updated_rows == 0:
                    logging.error(
                        "No records found to update with conditions: %s", filter_conditions)
                    return  # Возвращаемся, если нет обновлений
                session.commit()
                logging.info("Update successful")
            except SQLAlchemyError as e:
                session.rollback()
                logging.error(f"Error during update: {e}", exc_info=True)

    def select(self, model_class, filter_conditions=None, limit=None, order_by=None, distinct=False):
        with self.Session() as session:
            query = session.query(model_class)
            if distinct:
                query = query.distinct()
            if filter_conditions:
                query = query.filter_by(**filter_conditions)
            if order_by:
                query = query.order_by(order_by)
            if limit:
                query = query.limit(limit)
            return query.all()

    def close(self):
        self.Session.remove()


model_classes = {
    "offers": Offers,
    "addresses": Addresses,
    "realty_inside": Realty_inside,
    "realty_outside": Realty_outside,
    "realty_details": Realty_details,
    "offers_details": Offers_details,
    "developers": Developers,
}

DB = DatabaseManager(DATABASE_URL)
