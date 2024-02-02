# tljh-neurodesk

Tells TLJH to use [DockerSpawner](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/) to spin up [vnmd/neurodesktop](https://hub.docker.com/r/vnmd/neurodesktop/tags) containers for each user. 


## Install

Include `--plugin tljh-neurodesk` in your TLJH install script. For example, here user `neurodesk` with password `password` installs TLJH with `tljh-neurodesk`:
```
#!/bin/bash

curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
  | sudo python3 - \
    --admin neurodesk:password --plugin git+https://github.com/Neurodesk/tljh-neurodesk
```


## Attribution

This plugin was inspired by https://github.com/pennchildlanglab/tljh-datascience which was inspired by [this Ideonate post](https://ideonate.com/DockerSpawner-in-TLJH/) and the [Rxns stack plugin](https://github.com/sustainable-processes/tljh-rxns)

## To-do

- figure out how to include jupyterlab plugins (probably just a docker image based on the neurodesk-notebook is the easiest)
- we could prob do this without using subprocesses --  maybe require dockerspawner in the setup.py and then import it; and then just install docker.io via additional apt packages. 


