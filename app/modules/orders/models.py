from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoPedido(str, Enum):
    RECOGER = "RECOGER"
    ENVIO = "ENVIO"


class EstadoPedido(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"


class Order(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"),
        nullable=False,
    )

    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey("sucursales.id"),
        nullable=False,
    )

    tipo: Mapped[TipoPedido] = mapped_column(
        SQLEnum(
            TipoPedido,
            name="tipo_pedido",
            create_type=False,
        ),
        nullable=False,
    )

    estado: Mapped[EstadoPedido] = mapped_column(
        SQLEnum(
            EstadoPedido,
            name="estado_pedido",
            create_type=False,
        ),
        default=EstadoPedido.PENDIENTE,
        nullable=False,
    )

    direccion_entrega: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    descuento: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    notas: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    cliente: Mapped["Client"] = relationship(
        back_populates="pedidos",
    )

    sucursal: Mapped["Branch"] = relationship(
        back_populates="pedidos",
    )