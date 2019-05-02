# glockr

[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI version](https://badge.fury.io/py/glockr.svg)](https://badge.fury.io/py/glockr)
[![Maintainability](https://api.codeclimate.com/v1/badges/913f98606870d82e0b24/maintainability)](https://codeclimate.com/github/williamfzc/glockr/maintainability)
[![Build Status](https://travis-ci.org/williamfzc/glockr.svg?branch=master)](https://travis-ci.org/williamfzc/glockr)

global lockable resources for all

## goal

Resources lock for everything.

Highly inspired by [Jenkins's lockable resources plugin](https://wiki.jenkins.io/display/JENKINS/Lockable+Resources+Plugin).

And, make it works locally.

## usage

Python 3.6+

### backend

> g lock r s = global lockable resource server

Start your backend firstly:

```bash
pip install glockr

# default use port 29410
glockrs start
```

Or, directly use docker:

```bash
docker pull williamfzc/glockr
docker run --rm -p 29410:29410 williamfzc/glockr
```

Based on [FastAPI](https://github.com/tiangolo/fastapi), All the API of glockr can be easily viewed and executed via [http://127.0.0.1:29410/docs](http://127.0.0.1:29410/docs). 

![backend](./pic/backend_ui.png)

You can also use it as UI to manage your resource directly.

### CLI

> g lock r c = global lockable resource client

Make sure glockr backend has been started.

```bash
glockrc heartbeat
```

And you will see the help:

```bash
➜  glockr git:(master) glockrc
Type:        GClient
String form: <glockr.client.GClient object at 0x7f506abcee48>

Usage:       glockrc 
             glockrc acquire-label
             glockrc acquire-name
             glockrc add
             glockrc heartbeat
             glockrc release-label
             glockrc release-name
             glockrc remove
             glockrc show-all
```

JSON response can be easily handled by other programs.

#### add a new resource

New a resource object, named "123", label "abc":

```bash
in:
glockrc add 123 abc

out:
{"result": True, "reason": ""}
```

#### acquire a resource

Acquire it by name!

```bash
in:
glockrc acquire-name 123

out:
{"result": True, "reason": ""}
```

After acquirement, resource has been locked!

```bash
in:
glockrc acquire-name 123

out:
{"result": False, "reason": "res 123 status: BUSY"}
```

#### acquire multiple resources with `label`

Label can be used to require locks on multiple resources concurrently.

New a resource object, named "456", label "abc". Then, lock label "abc". By doing this, "123" and "456" (because they have label "abc") will be locked.

```bash
in:
glockrc release-name 123
glockrc add 456 abc
glockrc acquire-label abc
glockrc show-all

out:
{"123": {"name": "123", "label": "abc", "status": "BUSY"}, "456": {"name": "456", "label": "abc", "status": "BUSY"}}
```

#### backup and restore your data

Note: **glockr server only save your data in python runtime! And once server were stopped, your data will gone and you have to add them again.**

But, you can use `download` and `upload` to sync your data easily.

```bash
in:
glockrc download ./data1.json

out:
{"123": {"name": "123", "label": "abc", "status": "BUSY"}, "456": {"name": "456", "label": "abc", "status": "BUSY"}}
```

Your data will be saved in `./data1.json`. And, you can use them to init your server:

```bash
in:
glockrc upload ./data1.json

out:
{"result":true,"reason":""}
{"result":true,"reason":""}
```

One by one, your data has been uploaded!

### program (WIP)

Based on C/S, glockr supports different language clients.
