from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app

def test_invalid_input():
    with patch("app.main.Retriever") as R:
        R.return_value.collection.count.return_value=0
        with TestClient(app) as c: assert c.post("/query",json={"question":""}).status_code==422

def test_happy_path():
    with patch("app.main.Retriever") as R, patch("app.api.routes.query.generate",return_value=("Grounded answer [Source 1]",["doc.pdf (page 1, chunk 0)"])):
        r=MagicMock(); r.collection.count.return_value=1; r.search.return_value=[{"text":"x","source":"doc.pdf","page":1,"chunk":0}]; R.return_value=r
        with TestClient(app) as c:
            res=c.post("/query",json={"question":"What is this document about?"}); assert res.status_code==200; assert "answer" in res.json()
