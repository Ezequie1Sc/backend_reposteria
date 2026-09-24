from datetime import datetime, time
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Numeric,
    String,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DiaSemana(str, Enum):
    LUNES = "LUNES"
    MARTES = "MARTES"
    MIERCOLES = "MIERCOLES"
    JUEVES = "JUEVES"
    VIERNES = "VIERNES"
    SABADO = "SABADO"
    DOMINGO = "DOMINGO"


class Branch(Base):
    __tablename__ = "sucursales"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    codigo: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    direccion: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    ciudad: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    codigo_postal: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    latitud: Mapped[float | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    longitud: Mapped[float | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    horarios: Mapped[list["BranchSchedule"]] = relationship(
        back_populates="sucursal",
        cascade="all, delete-orphan",
    )

    empleados: Mapped[list["Employee"]] = relationship(
        back_populates="sucursal",
    )


class BranchSchedule(Base):
    __tablename__ = "horarios_sucursal"

    id: Mapped[int] = mapped_column(primary_key=True)

    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey("sucursales.id", ondelete="CASCADE"),
        nullable=False,
    )

    dia: Mapped[DiaSemana] = mapped_column(
        SQLEnum(
            DiaSemana,
            name="dia_semana",
            create_type=False,
        ),
        nullable=False,
    )

    hora_apertura: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    hora_cierre: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    sucursal: Mapped["Branch"] = relationship(
        back_populates="horarios",
    )


class Employee(Base):
    __tablename__ = "empleados"

    id: Mapped[int] = mapped_column(primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
    )

    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey("sucursales.id"),
        nullable=False,
    )

    numero_empleado: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    puesto: Mapped[str] = mapped_column(
        String(100),
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

    sucursal: Mapped["Branch"] = relationship(
        back_populates="empleados",
    )