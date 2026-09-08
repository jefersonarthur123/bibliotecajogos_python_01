from pathlib import Path
from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Jogo
from app.schemas import JogoCreate, JogoUpdate, JogoResponse

router = APIRouter()

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ==========================================
# Rotas Web (Jinja2 + Bootstrap 5)
# ==========================================

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def listar_web(request: Request, db: Session = Depends(get_db)):
    jogos = db.query(Jogo).order_by(Jogo.id.asc()).all()
    return templates.TemplateResponse(request=request, name="jogos.html", context={"jogos": jogos})


@router.post("/jogos", response_class=RedirectResponse, status_code=status.HTTP_303_SEE_OTHER, tags=["Web"],
             summary="Adicionar jogo via Formulário Web")
def adicionar_web(
        titulo: Annotated[str, Form(description="Título do jogo")],
        plataforma: Annotated[str, Form(description="Plataforma do jogo")],
        db: Session = Depends(get_db),
):
    novo_jogo = Jogo(titulo=titulo, plataforma=plataforma, concluido=False)
    db.add(novo_jogo)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/jogos/{id}/concluir", response_class=RedirectResponse, status_code=status.HTTP_303_SEE_OTHER,
             tags=["Web"], summary="Alternar status do jogo via Formulário Web")
def alternar_status_web(id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if jogo:
        jogo.concluido = not jogo.concluido
        db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/jogos/{id}/apagar", response_class=RedirectResponse, status_code=status.HTTP_303_SEE_OTHER, tags=["Web"],
             summary="Apagar jogo via Formulário Web")
def apagar_web(id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if jogo:
        db.delete(jogo)
        db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# ==========================================
# Endpoints REST API (Swagger / JSON)
# ==========================================

@router.get("/api/jogos", response_model=list[JogoResponse], tags=["API REST - Jogos"], summary="Listar todos os jogos")
def api_listar_jogos(db: Session = Depends(get_db)):
    return db.query(Jogo).order_by(Jogo.id.asc()).all()


@router.get("/api/jogos/{id}", response_model=JogoResponse, tags=["API REST - Jogos"], summary="Buscar jogo por ID")
def api_buscar_jogo(id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if not jogo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo com ID {id} não encontrado",
        )
    return jogo


@router.post("/api/jogos", response_model=JogoResponse, status_code=status.HTTP_201_CREATED, tags=["API REST - Jogos"],
             summary="Cadastrar novo jogo")
def api_criar_jogo(jogo_in: JogoCreate, db: Session = Depends(get_db)):
    novo_jogo = Jogo(
        titulo=jogo_in.titulo,
        plataforma=jogo_in.plataforma,
        concluido=jogo_in.concluido,
    )
    db.add(novo_jogo)
    db.commit()
    db.refresh(novo_jogo)
    return novo_jogo


@router.put("/api/jogos/{id}", response_model=JogoResponse, tags=["API REST - Jogos"], summary="Atualizar jogo por ID")
def api_atualizar_jogo(id: int, jogo_in: JogoUpdate, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if not jogo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo com ID {id} não encontrado",
        )

    if jogo_in.titulo is not None:
        jogo.titulo = jogo_in.titulo
    if jogo_in.plataforma is not None:
        jogo.plataforma = jogo_in.plataforma
    if jogo_in.concluido is not None:
        jogo.concluido = jogo_in.concluido

    db.commit()
    db.refresh(jogo)
    return jogo


@router.patch("/api/jogos/{id}/concluir", response_model=JogoResponse, tags=["API REST - Jogos"],
              summary="Alternar status zerado/jogando")
def api_alternar_status(id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if not jogo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo com ID {id} não encontrado",
        )

    jogo.concluido = not jogo.concluido
    db.commit()
    db.refresh(jogo)
    return jogo


@router.delete("/api/jogos/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["API REST - Jogos"],
               summary="Excluir jogo por ID")
def api_deletar_jogo(id: int, db: Session = Depends(get_db)):
    jogo = db.query(Jogo).filter(Jogo.id == id).first()
    if not jogo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo com ID {id} não encontrado",
        )
    db.delete(jogo)
    db.commit()