import zipfile
import logging
import os
import requests
from shutil import copyfile, copytree, rmtree

def zip_trainer(
        trainer_folder_name,
        zip_name="trainer.zip",
        TRAINER_FILES = [
            'README.md',
            'setup.py',
            'trainer/model.py',
            'trainer/task.py',
            'trainer/__init__.py',
            'trainer/GCSproxy.py'
            ]
        ):
    """
    a trainer must have

    - README.md
    - setup.py
    - trainer/
        - model.py
        - task.py
    """
    logging.warning("relna:utils:zip_trainer: writing zipfile to {}".format(zip_name))
    zf = zipfile.ZipFile(zip_name, mode='w')
    for filename in TRAINER_FILES:
        zf.write(os.path.join(trainer_folder_name, filename),
                arcname=filename)
    zf.close()

def unzip_trainer(
        zipped_trainer_filename="trainer.zip", 
        destination_dir="."):
    destination_dir = os.path.join(
            destination_dir,
            "relna_trainer"
            )
    logging.warning("relna:utils:unzip_trainer: unzip trainer from {} to {}".format(
                zipped_trainer_filename, destination_dir))
    zip_ref = zipfile.ZipFile(zipped_trainer_filename, 'r')
    zip_ref.extractall(destination_dir)
    zip_ref.close()

def build_package(
        trainer_folder_name,
        package_name="trainer.tar.gz"):
    """
    """
    logging.warning("relna:utils:build_package: building package of {} to {}".format(trainer_folder_name, package_name))
    pkg_destination_folder = os.path.join(package_name)
    # copying setup.py and trainer to current folder
    # (package will not be built correctly otherwise

    copyfile(os.path.join(trainer_folder_name, 'setup.py'), 'setup.py')
    copytree(os.path.join(trainer_folder_name, 'trainer'), 'trainer')
    #os.system("cp {} .".format(os.path.join(trainer_folder_name, 'setup.py')))
    #os.system("cp -r {} .".format(os.path.join(trainer_folder_name, 'trainer')))
    # following commands builds the package
    os.system("python setup.py\
            sdist -d {}".format(pkg_destination_folder))
    logging.warning("[relna:utils:buikd_package] generated pakage {}".format(
        pkg_destination_folder))

    #clean local folder
    os.remove("./setup.py")
    rmtree("./trainer")
    rmtree("./trainer.egg-info")

def post_request(
        url = 'https://relna-241818.appspot.com/',
        values = {}
        ):
    """
    POST request to relna server
    """
    logging.warning("relna-client:bin:utils:post_request opening connectino with {}".format(url))
    logging.warning("relna-client:bin:utils:post_request posting request to server {}".format(values.keys()))
    response = requests.post(url, values)
    logging.warning("relna-client:bin:utils:post_request request successful")
    return response

