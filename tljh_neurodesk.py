from tljh.hooks import hookimpl
import subprocess

@hookimpl
def tljh_config_post_install(config):
    """
    Set JupyterLab to be default
    """
    config['user_environment'] = config.get('user_environment', {})
    config['user_environment']['default_app'] = config['user_environment'].get('default_app', 'jupyterlab')

@hookimpl
def tljh_post_install():
    """
    Setup the neurodesk-notebook
    """
    
    # create the dockerspawner config file
    f = open("/opt/tljh/config/jupyterhub_config.d/dockerspawner_tljh_config.py", "w")

    # add the details to use docker spawner with the neurodesk image
    contents = [
        "c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'",
        "c.DockerSpawner.image_whitelist = ['vnmd/neurodesktop:2023-11-28', 'jupyter/datascience-notebook:r-4.0.3', 'jupyter/datascience-notebook:r-3.6.3']",
        "from jupyter_client.localinterfaces import public_ips",
        "c.JupyterHub.hub_ip = public_ips()[0]",
        "c.DockerSpawner.name_template = '{prefix}-{username}-{servername}'"
    ]

    # add to our config file and close
    f.write("\n".join(contents))
    f.close()

    subprocess.call("sudo systemctl start docker", shell=True)

    # finally we need to download the docker image so it's ready
    subprocess.call("sudo docker pull vnmd/neurodesktop:2023-11-28", shell=True)
        
    # and the restart TLJH and rebuild jupyterlab
    subprocess.call("sudo tljh-config reload", shell=True)
    

@hookimpl
def tljh_extra_apt_packages(): return ["docker.io"]

@hookimpl
def tljh_extra_hub_pip_packages(): return ["dockerspawner", "jupyter_client"]