# CAHRIM

The content of this folder have been released in October 2020 according the CARESSES release plan.

## Contractor Notes

I've refactored this repo to facilitate build and execution within a docker environment. This is mainly to deal with the Pepper-Python 2.7 dependencies. Quite a lot of python libraries have stopped supporting Python 2.7 as it's soon to be deprecated. What support remains is legacy and shaky at best.

Particularly to watch are the Choregraphe and pynaoqi dependnencies, given the situation around Aldebaran support of the pepper I think it's probably best to load these to a project repository where they can be maintained.

As long as the Docker images are maintained the system should be able to run without these external resources, it will just be an issue if the image needs to be rebuilt.

I will try and get the image to a fully functional state. Future work on the project should focus on migrating the code base however with the pepper stuck at Python 2.7 that doesn't seem trivial.

## Installation

```
docker pull richardw347/caress:latest
```

```
docker run -it richardw347/caress:latest
```

### Notes

#### Socket Communication

see socket_handlers.py:

* Looks like character-based protocol for message passing between components of the system. That's a critical issue to resolve in progressing the project to the future. Message definitions form a contract between sender and receiver text-based protocols do nothing to preserver the contract!
* Also there's not much error handling in the socket communications, replacing these with a modern IPC library is a must

#### Google API Client

As per this issue <https://github.com/grpc/grpc/issues/23190> the default install for the api client installs an incompatible version of the RSA library it is necessary to uninstall it and install v4.0.

```
pip uninstall rsa
pip install -v rsa==4.0
```

## Changelog

* Added requirements.txt for all python dependencies
* Added Dockerfile with system and pepper dependencies
