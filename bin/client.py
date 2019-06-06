import sys
try: import utils
except: 
    sys.path.append("./bin")
    sys.path.append("../")
    import utils
import os
import logging

def prepare_payload(
        trainer_folder_name,
        payload_folder_name="payload"
        ):
    """
    zip python code and build package
    """
    logging.warning("relna:client:prepare_payload: preparing payload from {} to {}".format(trainer_folder_name, payload_folder_name))
    try: os.mkdir(payload_folder_name)
    except: pass
    utils.zip_trainer(
            trainer_folder_name,
            zip_name=os.path.join(payload_folder_name, "trainer.zip"))
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
    zipped_code_bytes = utils.post_request(url, {'trainerID':trainerID})
    with open(TRAINER_ZIP, "wb") as f:
        f.write(zipped_code_bytes)
    try: os.mkdir(destination_dir)
    except: pass
    utils.unzip_trainer(
            zipped_trainer_filename=TRAINER_ZIP,
            destination_dir=destination_dir)
    os.remove("trainer.zip")
    logging.warning("relna:client:fork trainer {}, fork successful".format(trainerID))
