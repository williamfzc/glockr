from fastapi import FastAPI
import uvicorn
import fire
import os

from glockr.manager import GResourceManager
from glockr import config

# --- API below ---

# TODO API for updating resource?

app = FastAPI()

os.putenv('GLOCKR_PORT', config.PORT)


@app.get(config.ROUTER['heartbeat'])
def heartbeat():
    return {"hello": "from glockr server"}


@app.get(config.ROUTER['show_all'])
def show_all():
    return GResourceManager.show_all()


@app.post(config.ROUTER['add'])
def add(name: str, label: str = None):
    return GResourceManager.add(name, label).to_dict()


@app.post(config.ROUTER['remove'])
def remove(name: str):
    return GResourceManager.remove(name).to_dict()


@app.post(config.ROUTER['acquire'])
def acquire(name: str = None, label: str = None):
    """ acquire resource """
    if name:
        return GResourceManager.acquire_res(name).to_dict()
    if label:
        return GResourceManager.acquire_label(label).to_dict()
    return {
        'error': 'at least fill name or label'
    }


@app.post(config.ROUTER['release'])
def release(name: str = None, label: str = None):
    """ release resource """
    if name:
        return GResourceManager.release_res(name).to_dict()
    if label:
        return GResourceManager.release_label(label).to_dict()
    return {
        'error': 'at least fill name or label'
    }


def start_server(port: int = None):
    # TODO how to sync this change to client ??
    if not port:
        port = config.PORT

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )


def main():
    fire.Fire({
        'start': start_server,
    })


if __name__ == '__main__':
    main()
