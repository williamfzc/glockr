from fastapi import FastAPI
import uvicorn

from glockr.manager import GResourceManager


# --- API below ---

app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "from glockr server"}


@app.get("/res")
def res():
    return GResourceManager.show_all()


@app.post("/res/add")
def add(name: str, label: str = None):
    return GResourceManager.add(name, label).to_dict()


@app.post("/res/remove")
def remove(name: str):
    return GResourceManager.remove(name).to_dict()


@app.post("/res/acquire")
def acquire(name: str = None, label: str = None):
    """ acquire resource """
    if name:
        return GResourceManager.acquire_res(name).to_dict()
    if label:
        return GResourceManager.acquire_label(label).to_dict()
    return {
        'error': 'at least fill name or label'
    }


@app.post("/res/release")
def release(name: str = None, label: str = None):
    """ release resource """
    if name:
        return GResourceManager.release_res(name).to_dict()
    if label:
        return GResourceManager.release_label(label).to_dict()
    return {
        'error': 'at least fill name or label'
    }


def start_server():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9410,
        log_level="warning"
    )


if __name__ == '__main__':
    start_server()
