from sqlalchemy import Column, String, Integer, TIMESTAMP, BigInteger, ForeignKey, Enum, Text, Table, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table
user_product_association = Table(
    'user_product', Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.user_id')),
    Column('product_id', BigInteger, ForeignKey('products.product_id'))
)

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    zip_code = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    # Relationship with login_activities table
    login_activities = relationship("LoginActivity", back_populates="user", cascade="all, delete-orphan")

    # Relationship with subscriptions table
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

    # Relationship with Product Table
    products = relationship(
        "Product",
        secondary=user_product_association,
        back_populates="users"
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')>"

class LoginActivity(Base):
    __tablename__ = "login_activities"

    login_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    login_at = Column(TIMESTAMP, nullable=False)
    login_status = Column(Enum("success", "failed", name="login_status_enum"), nullable=False)
    ip_address = Column(String(50))
    device_info = Column(String(255))

    # Relationship with users table
    user = relationship("User", back_populates="login_activities")

class Newsletter(Base):
    __tablename__ = "newsletters"

    newsletter_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(Enum("food_recall", "expiration_notice", name="newsletter_type_enum"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False
    )


class Subscription(Base):
    __tablename__ = "subscriptions"
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(BigInteger, primary_key=True, autoincrement=True)
    zip_code = Column(String(10), nullable=False)
    email = Column(String(255), nullable=False)
    state = Column(String(100), nullable=False)
    subscription_type = Column(
        Enum("food_recall", "expiration_notice", name="subscription_type_enum"),
        nullable=False
    )
    subscribed_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    status = Column(
        Enum("active", "unsubscribed", name="subscription_status_enum"),
        default="active", nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="subscriptions")

class Product(Base):
    __tablename__ = "products"
    product_id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=False)
    recall = Column(Boolean, default=False)

    # Relationship with User Table
    users = relationship(
        "User",
        secondary=user_product_association,
        back_populates="products"
    )

    def __repr__(self):
        return f"<ProductInfo(code={self.code}, name={self.name}, brand={self.brand}, recall={self.recall})>"