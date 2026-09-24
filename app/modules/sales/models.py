from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoVenta(str, Enum):
    TIENDA_FISICA = "TIENDA_FISICA"
    EN_LINEA = "EN_LINEA"


class EstadoVenta(str, Enum):
    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    CANCELADA = "CANCELADA"


class EstadoPago(str, Enum):
    PENDIENTE = "PENDIENTE"
    PAGADO = "PAGADO"
    REEMBOLSADO = "REEMBOLSADO"


class MetodoPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"


class Sale(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True)

    cliente_id: Mapped[int | None] = mapped_column(
        ForeignKey("clientes.id"),
        nullable=True,
    )

    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey("sucursales.id"),
        nullable=False,
    )

    pedido_id: Mapped[int | None] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=True,
    )

    tipo: Mapped[TipoVenta] = mapped_column(
        SQLEnum(
            TipoVenta,
            name="tipo_venta",
            create_type=False,
        ),
        nullable=False,
    )

    estado: Mapped[EstadoVenta] = mapped_column(
        SQLEnum(
            EstadoVenta,
            name="estado_venta",
            create_type=False,
        ),
        default=EstadoVenta.PENDIENTE,
        nullable=False,
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

    detalles: Mapped[list["SaleDetail"]] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan",
    )

    pagos: Mapped[list["Payment"]] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan",
    )

    ticket: Mapped["Ticket | None"] = relationship(
        back_populates="venta",
        uselist=False,
        cascade="all, delete-orphan",
    )

    factura: Mapped["Invoice | None"] = relationship(
        back_populates="venta",
        uselist=False,
        cascade="all, delete-orphan",
    )


class SaleDetail(Base):
    __tablename__ = "detalle_ventas"

    id: Mapped[int] = mapped_column(primary_key=True)

    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id", ondelete="CASCADE"),
        nullable=False,
    )

    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"),
        nullable=False,
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    venta: Mapped["Sale"] = relationship(
        back_populates="detalles",
    )


class Payment(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(primary_key=True)

    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id", ondelete="CASCADE"),
        nullable=False,
    )

    metodo: Mapped[MetodoPago] = mapped_column(
        SQLEnum(
            MetodoPago,
            name="metodo_pago",
            create_type=False,
        ),
        nullable=False,
    )

    estado: Mapped[EstadoPago] = mapped_column(
        SQLEnum(
            EstadoPago,
            name="estado_pago",
            create_type=False,
        ),
        default=EstadoPago.PENDIENTE,
        nullable=False,
    )

    monto: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    referencia: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    venta: Mapped["Sale"] = relationship(
        back_populates="pagos",
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)

    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    numero: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    venta: Mapped["Sale"] = relationship(
        back_populates="ticket",
    )


class Invoice(Base):
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(primary_key=True)

    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    rfc: Mapped[str] = mapped_column(
        String(13),
        nullable=False,
    )

    tipo_persona: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    nombre_razon_social: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    direccion: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    codigo_postal: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    cfdi: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    correo_electronico: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    venta: Mapped["Sale"] = relationship(
        back_populates="factura",
    )