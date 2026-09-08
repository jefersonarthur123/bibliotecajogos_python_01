from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Jogo(Base):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    plataforma: Mapped[str] = mapped_column(String(100), nullable=False)
    concluido: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)