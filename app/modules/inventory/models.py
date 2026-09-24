from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoMovimientoInventario(str, Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    AJUSTE = "AJUSTE"


class Inventory(Base):
    __tablename__ = "inventarios"

    id: Mapped[int] = mapped_column(primary_key=True)

    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"),
        nullable=False,
    )

    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey("sucursales.id"),
        nullable=False,
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    stock_minimo: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    stock_maximo: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    movimientos: Mapped[list["InventoryMovement"]] = relationship(
        back_populates="inventario",
        cascade="all, delete-orphan",
    )


class InventoryMovement(Base):
    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(primary_key=True)

    inventario_id: Mapped[int] = mapped_column(
        ForeignKey("inventarios.id", ondelete="CASCADE"),
        nullable=False,
    )

    tipo: Mapped[TipoMovimientoInventario] = mapped_column(
        SQLEnum(
            TipoMovimientoInventario,
            name="tipo_movimiento_inventario",
            create_type=False,
        ),
        nullable=False,
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    motivo: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    inventario: Mapped["Inventory"] = relationship(
        back_populates="movimientos",
    )