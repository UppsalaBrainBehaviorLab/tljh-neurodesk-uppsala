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
    Install docker, docker spawner, and setup the neurodesk-notebook
    """
    # first we'll install docker on ubuntu
    # inspired by https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04
    # and https://ideonate.com/DockerSpawner-in-TLJH/

    # use packages over https
    subprocess.call("sudo apt update && sudo apt install apt-transport-https ca-certificates curl software-properties-common", shell=True)

    # add gpg key
    subprocess.call("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -", shell=True)

    # add docker repo
    subprocess.call("sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable'", shell=True)

    # install docker
    subprocess.call("sudo apt update && sudo apt install -y docker-ce", shell=True)
    
    # then we'll install docker spawner
    # inspired by https://ideonate.com/DockerSpawner-in-TLJH/
    subprocess.call("sudo /opt/tljh/hub/bin/python3 -m pip install dockerspawner jupyter_client", shell=True)
    
    # then we'll tell TLJH to use docker spawner
    # and that the image to use is neurodesktop

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

    # finally we need to download the docker image so it's ready
    subprocess.call("sudo docker pull vnmd/neurodesktop:2023-11-28", shell=True)
        
    # and the restart TLJH and rebuild jupyterlab
    subprocess.call("sudo tljh-config reload", shell=True)
    
