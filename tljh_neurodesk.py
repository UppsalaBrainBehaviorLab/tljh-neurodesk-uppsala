from tljh.hooks import hookimpl as hook

images = ["vnmd/neurodesktop", "jupyter/datascience-notebook"]

@hook
def tljh_post_install():  # Setup the neurodesk-notebook
    __import__("os").system("sudo systemctl start docker\n" +
                '\n'.join([f"sudo docker pull {img}" for img in images]))

@hook
def tljh_extra_apt_packages(): return ["docker.io"]

@hook
def tljh_extra_hub_pip_packages(): return ["dockerspawner", "jupyter_client"]

@hook
def tljh_custom_jupyterhub_config(c):
    from jupyter_client.localinterfaces import public_ips
    c.JupyterHub.hub_ip = public_ips()[0]
    c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
    c.DockerSpawner.name_template = "{prefix}-{username}-{servername}"
    c.DockerSpawner.image_whitelist = images
