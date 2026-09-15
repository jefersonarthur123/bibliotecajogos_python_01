from fastapi.testclient import TestClient


# =========================
# TESTES WEB
# =========================

def test_web_lista_vazia(client: TestClient):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert "Biblioteca de Jogos" in resposta.text


def test_web_fluxo_completo(client: TestClient):
    # Criar jogo
    resposta = client.post(
        "/jogos",
        data={
            "titulo": "Minecraft",
            "plataforma": "PC"
        }
    )

    assert resposta.status_code == 200
    assert "Minecraft" in resposta.text

    # Concluir jogo
    resposta = client.post("/jogos/1/concluir")

    assert resposta.status_code == 200
    assert "Minecraft" in resposta.text

    # Apagar jogo
    resposta = client.post("/jogos/1/apagar")

    assert resposta.status_code == 200
    assert "Minecraft" not in resposta.text


def test_web_atualizar_jogo(client: TestClient):
    # Criar jogo
    resposta = client.post(
        "/jogos",
        data={
            "titulo": "Minecraft",
            "plataforma": "PC"
        }
    )

    assert resposta.status_code == 200

    # Abrir tela de edição
    resposta = client.get("/jogos/1/editar")

    assert resposta.status_code == 200
    assert 'value="Minecraft"' in resposta.text
    assert 'value="PC"' in resposta.text

    # Atualizar jogo
    resposta = client.post(
        "/jogos/1/editar",
        data={
            "titulo": "Minecraft Java",
            "plataforma": "PC"
        }
    )

    # O POST redireciona para /
    # e o conftest.py segue automaticamente o redirect
    assert resposta.status_code == 200
    assert "Minecraft Java" in resposta.text


def test_web_editar_jogo_inexistente(client: TestClient):
    resposta = client.get("/jogos/999/editar")

    assert resposta.status_code == 404


def test_web_concluir_jogo_inexistente(client: TestClient):
    resposta = client.post("/jogos/999/concluir")

    assert resposta.status_code == 404


def test_web_apagar_jogo_inexistente(client: TestClient):
    resposta = client.post("/jogos/999/apagar")

    assert resposta.status_code == 404


# =========================
# TESTES DA API
# =========================

def test_api_crud_completo(client: TestClient):
    # CREATE
    resposta = client.post(
        "/api/jogos",
        json={
            "titulo": "God of War",
            "plataforma": "PS5",
            "concluido": False
        }
    )

    assert resposta.status_code == 201

    jogo = resposta.json()

    assert jogo["titulo"] == "God of War"
    assert jogo["plataforma"] == "PS5"
    assert jogo["concluido"] is False

    jogo_id = jogo["id"]

    # READ - lista
    resposta = client.get("/api/jogos")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1

    # READ - específico
    resposta = client.get(f"/api/jogos/{jogo_id}")

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "God of War"

    # UPDATE
    resposta = client.put(
        f"/api/jogos/{jogo_id}",
        json={
            "titulo": "God of War Ragnarok",
            "plataforma": "PS5",
            "concluido": True
        }
    )

    assert resposta.status_code == 200

    jogo_atualizado = resposta.json()

    assert jogo_atualizado["titulo"] == "God of War Ragnarok"
    assert jogo_atualizado["concluido"] is True

    # DELETE
    resposta = client.delete(f"/api/jogos/{jogo_id}")

    assert resposta.status_code == 204

    # Confirmar que foi apagado
    resposta = client.get(f"/api/jogos/{jogo_id}")

    assert resposta.status_code == 404


def test_api_jogo_inexistente(client: TestClient):
    resposta = client.get("/api/jogos/999")

    assert resposta.status_code == 404


def test_api_criar_jogo_invalido(client: TestClient):
    resposta = client.post(
        "/api/jogos",
        json={
            "titulo": "",
            "plataforma": "PC"
        }
    )

    assert resposta.status_code == 422


def test_api_atualizacao_parcial(client: TestClient):
    # Criar
    resposta = client.post(
        "/api/jogos",
        json={
            "titulo": "Minecraft",
            "plataforma": "PC",
            "concluido": False
        }
    )

    assert resposta.status_code == 201

    jogo_id = resposta.json()["id"]

    # PATCH apenas concluído
    resposta = client.patch(
        f"/api/jogos/{jogo_id}/concluir"
    )

    assert resposta.status_code == 200
    assert resposta.json()["concluido"] is True


def test_api_atualizar_jogo_inexistente(client: TestClient):
    resposta = client.put(
        "/api/jogos/999",
        json={
            "titulo": "Teste",
            "plataforma": "PC",
            "concluido": False
        }
    )

    assert resposta.status_code == 404


def test_api_deletar_jogo_inexistente(client: TestClient):
    resposta = client.delete("/api/jogos/999")

    assert resposta.status_code == 404