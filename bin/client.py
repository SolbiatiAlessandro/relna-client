import sys
try: import utils
except: 
    sys.path.append("./bin")
    sys.path.append("../")
    import utils
import os
import logging
import requests

def prepare_payload(
        trainer_folder_name,
        payload_folder_name="payload",
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
    zip python code and build package
    """
    logging.warning("relna:client:prepare_payload: preparing payload from {} to {}".format(trainer_folder_name, payload_folder_name))
    try: os.mkdir(payload_folder_name)
    except: pass
    utils.zip_trainer(
            trainer_folder_name,
            zip_name=os.path.join(payload_folder_name, "trainer.zip"),
            TRAINER_FILES=TRAINER_FILES)
    utils.build_package(
            trainer_folder_name,
            package_name=payload_folder_name)
    logging.warning("relna:client:prepare_payload: payload prepared succesfully at  {}".format(payload_folder_name))

def fork_request(
        trainerID='5',
        local=True,
        destination_dir="."
        ):
    """
    get zipped code bytes data from postgresql,
    save it in destination_dir
    """
    trainerID = str(trainerID)
    logging.warning("relna:client:fork forking trainer {}".format(trainerID))
    TRAINER_ZIP = "trainer.zip"
    if local: url = "http://127.0.0.1:5000/fork"
    else: url = "https://relna-241818.appspot.com/fork"
    response = utils.post_request(url, {'trainerID':trainerID})
    zipped_code_bytes = response.content
    with open(TRAINER_ZIP, "wb") as f:
        f.write(zipped_code_bytes)
    try: os.mkdir(destination_dir)
    except: pass
    utils.unzip_trainer(
            zipped_trainer_filename=TRAINER_ZIP,
            destination_dir=destination_dir)
    os.remove("trainer.zip")
    logging.warning("relna:client:fork trainer {}, fork successful".format(trainerID))

def ship_request(
        zipped_code_path,
        trainer_pkg_path,
        local=True,
        python_model='template_model',
        gym='RoboschoolHumanoid',
        expert_policy='v1',
        ):
    """
    already prepared payload
    send ship request ro relna server
    """
    logging.warning("relna:client:ship shipping trainer {}".format(
        trainer_pkg_path))
    if local: url = "http://127.0.0.1:5000/ship"
    else: url = "https://relna-241818.appspot.com/ship"
    with open(zipped_code_path,'rb') as zf:
        zipped_code_binary = bytes(zf.read())
    with open(trainer_pkg_path,'rb') as pf:
        trainer_pkg_binary = bytes(pf.read())
    requests.post(url, data={
        'zipped_code_binary': zipped_code_binary,
        'trainer_pkg_binary' : trainer_pkg_binary,
        'python_model' : python_model,
        'gym' : gym,
        'expert_policy' : expert_policy
        }, files={
            'trainer':open(trainer_pkg_path,"rb"),
            'code':open(zipped_code_path,"rb")
            }
        
        )
    logging.warning("relna:client:ship ship request sent succesfully")
