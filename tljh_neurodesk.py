from tljh.hooks import hookimpl as hook
import os, shutil

image = "vnmd/neurodesktop"

@hook
def tljh_post_install():  # Setup the neurodesk-notebook
    os    .system("sudo systemctl start docker\n" +
                 f"sudo docker pull {image}")

    if os.path.isdir("/etc/apparmor.d"):
        os.chdir(__import__("CVMFS").__path__[0])
        shutil.copyfile("apparmor", "/etc/apparmor.d/CVMFS")
        os.system("""sudo apparmor_parser -r /etc/apparmor.d/CVMFS
            docker compose up -d""")

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
    c.DockerSpawner.image = image
    c.DockerSpawner.extra_host_config = {
        "security_opt": ["apparmor=unconfined"],
        "cap_add": ["SYS_ADMIN"]
    }
    c.DockerSpawner.extra_create_kwargs = {"user": "root"}
    c.DockerSpawner.volumes = {
        "{prefix}-{username}": "/home/jovyan",
        "/storage/{username}": "/storage/{username}",
        "/storage-{username}": "/data",
        "/cvmfs": "/cvmfs"
    }
    c.DockerSpawner.environment = {
    "CHOWN_HOME": "yes",
    "CHOWN_EXTRA": "/home/jovyan",
    "CHOWN_EXTRA_OPTS": "-R",
    "NB_UID": 1001,
    "NB_GID": 100,
}

@hook
def my_hook(spawner):
    username = spawner.user.name
    uid = getpwnam(username).pw_uid
    spawner.environment['NB_UID'] = uid
    gid = getpwnam(username).pw_gid
    spawner.environment['NB_GID'] = gid
    print(spawner.environment)
