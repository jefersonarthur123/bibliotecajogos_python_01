from pydantic import BaseModel, ConfigDict, Field

class JogoBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255, description="Título do jogo")
    plataforma: str = Field(..., min_length=1, max_length=100, description="Plataforma (ex: PC, PS5, Xbox, Switch)")
    concluido: bool = Field(default=False, description="Indica se o jogo foi concluído/zerado")

class JogoCreate(JogoBase):
    pass

class JogoUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=255)
    plataforma: str | None = Field(default=None, min_length=1, max_length=100)
    concluido: bool | None = Field(default=None)

class JogoResponse(JogoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)