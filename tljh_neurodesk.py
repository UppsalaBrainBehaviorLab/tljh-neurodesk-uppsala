from tljh.hooks import hookimpl as hook
import os

images = ["vnmd/neurodesktop", "jupyter/datascience-notebook"]

@hook
def tljh_post_install():  # Setup the neurodesk-notebook
    os    .system("sudo systemctl start docker\n" +
      '\n'.join([f"sudo docker pull {img}" for img in images]))

    os.chdir(os.path.dirname(__file__) + "/CVMFS")
    os.replace("apparmor", "/etc/apparmor.d/CVMFS")
    os.system("""sudo apparmor_parser -r /etc/apparmor.d/CVMFS
    docker-compose up -d""")

@hook
def tljh_extra_apt_packages(): return ["docker.io", "docker-compose"]

@hook
def tljh_extra_hub_pip_packages(): return ["dockerspawner", "jupyter_client"]

@hook
def tljh_custom_jupyterhub_config(c):
    from jupyter_client.localinterfaces import public_ips
    c.JupyterHub.hub_ip = public_ips()[0]
    c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
    c.DockerSpawner.name_template = "{username}-{imagename}"
    c.DockerSpawner.allowed_images = images
    c.DockerSpawner.extra_create_kwargs = {"user": "root"}
    c.DockerSpawner.volumes = {
        "{prefix}-{username}": "/home/jovyan",
        "/cvmfs": "/cvmfs"
    }