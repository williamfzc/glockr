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

base usage:

```bash
glockr acquire res <your_resource_name>
glockr release res <your_resource_name>
```

and support 'label':

```bash
glockr acquire label <your_resource_label_name>
glockr release label <your_resource_label_name>
```

JSON response can be easily handled.

### program (WIP)

Based on C/S, glockr supports different language clients.
