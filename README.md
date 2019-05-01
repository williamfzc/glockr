# glockr

[![PyPI version](https://badge.fury.io/py/glockr.svg)](https://badge.fury.io/py/glockr)
[![Maintainability](https://api.codeclimate.com/v1/badges/913f98606870d82e0b24/maintainability)](https://codeclimate.com/github/williamfzc/glockr/maintainability)

global lockable resources for all

## goal

Resources lock for everything.

Highly inspired by [Jenkins's lockable resources plugin](https://wiki.jenkins.io/display/JENKINS/Lockable+Resources+Plugin).

And, make it works locally.

## usage

### CLI

Start your backend firstly:

```bash
pip install glockr
python -m glockr.server
```

Or, directly use docker:

```bash
docker pull williamfzc/glockr
docker run --rm -p 9410:9410 williamfzc/glockr
```

You can use CLI now:

```bash
python -m glockr.client
```

And you will see the help:

```bash
$ python3 -m glockr.client

Type:        GClient
String form: <__main__.GClient object at 0x10d2f0d30>
File:        ~/github_workspace/glockr/glockr/client.py

Usage:       client.py
             client.py acquire-label
             client.py acquire-name
             client.py add
             client.py release-label
             client.py release-name
             client.py remove
             client.py show-all
```

New a resource object, named '123', label 'abc':

```bash
in:
python -m glockr.client add 123 abc

out:
{'result': True, 'reason': ''}
```

Acquire it by name!

```bash
in:
python -m glockr.client acquire-name 123

out:
{'result': True, 'reason': ''}
```

After acquirement, resource has been locked!

```bash
in:
python -m glockr.client acquire-name 123

out:
{'result': False, 'reason': 'res 123 status: BUSY'}
```

Label can be used to require locks on multiple resources concurrently.

New a resource object, named '456', label 'abc'.

```bash
python -m glockr.client acquire-label abc
```

Then, lock label 'abc'. By doing this, '123' and '456' (because they have label 'abc') will be locked.

JSON response can be easily handled by other programs.

### program (WIP)

Based on C/S, glockr supports different language clients.
