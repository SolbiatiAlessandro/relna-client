import click
import bin.client
import logging
import os
import configparser
import urllib.request

DELIMITER = "="*30
def dprint(content):
    print(DELIMITER+"\n"+content+"\n"+DELIMITER)

def read_trainer_config(trainer_folder):
    """
    return trainer_metadata, you can access it like
            gym = trainer_metadata['gym'],
            expert_policy = trainer_metadata['expert_policy'],
            python_model = trainer_metadata['python_model'],
            train_steps = trainer_metadata['train_steps']
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(
            os.path.join(trainer_folder, "trainer.config")
            )
    trainer_metadata = config['TRAINER_METADATA']
    logging.warning("[relna.read_trainer_config] trainer has the following config")
    for field, value in trainer_metadata.items():
        logging.warning("- {} : {}".format(field, value))
    return trainer_metadata

def ship_workflow(
    trainer_folder = "./relna_trainer",
    payload_folder = "./payload"
        ):
    """
    1. file/folder name definition/ manipulation
    2. call clients.prepare_payload
    3. call clients.ship_request
    """
    logging.warning("relna-client:relna:ship reading trainer from {}".format(trainer_folder))
    trainer_files = []
    trainer_files += os.listdir(trainer_folder)
    trainer_files += [os.path.join("trainer",filename) for filename in os.listdir(os.path.join(trainer_folder, "trainer"))]
    logging.warning("[relna.ship] shipping trainer with the following files (in the zip)")
    for file_name in trainer_files: 
        logging.warning("- {}".format(file_name))
    bin.client.prepare_payload(
            trainer_folder,
            payload_folder_name=payload_folder,
            TRAINER_FILES=trainer_files)
    
    trainer_metadata = read_trainer_config(trainer_folder)

    bin.client.ship_request(
            zipped_code_path=os.path.join(payload_folder, "trainer.zip"),
            trainer_pkg_path=os.path.join(payload_folder, "trainer-0.1.tar.gz"),
            local=False,
            gym = trainer_metadata['gym'],
            expert_policy = trainer_metadata['expert_policy'],
            python_model = trainer_metadata['python_model'],
            train_steps = trainer_metadata['train_steps']
            )
    logging.warning("relna-client:relna:ship ship request completed")

def fork_workflow():
    """
    """
    print("Enter the TrainerID you want to fork: ")
    trainerID = input()
    logging.warning("relna-client:relna:fork starting fork for trainer {}".format(trainerID))
    bin.client.fork_request(
            trainerID=trainerID,
            local=False,
            )
    logging.warning("relna-client:relna:fork fork for trainer {} completed".format(trainerID))

def data_workflow(
        trainer_folder="./relna_trainer",
        data_prefix_url="https://storage.googleapis.com/relna-mlengine/data/",
        save_folder="./gcloud_data"
        ):
    """
    """
    logging.warning("relna-client:relna:data this procedure will be downloading small sample of data for current trainer")
    trainer_metadata = read_trainer_config(trainer_folder)
    data_filename = data_prefix_url + trainer_metadata['expert_policy']
    if "small" not in data_filename:
        # get the small version of the data
        data_filename = data_filename.replace(".pkl","-small.pkl")
    logging.warning("relna-client:relna:data downloading data from gcloud with absolute path {}".format(data_filename))

    logging.warning("\nIMPORTANT: MAKE SURE {} EXIST AND YOU HAVE ACCESS TO IT\n".format(data_filename))
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    save_filename = os.path.join(save_folder, trainer_metadata['expert_policy'])
    logging.warning("relna-client:relna:data downloading data to {}".format(save_filename))
    urllib.request.urlretrieve(
            data_filename, 
            save_filename
            )
    logging.warning("relna-client:relna:data SUCCESS")


@click.command()
@click.option("--command", default="fork", help = "fork, ship")
def main(command):
    dprint("relna - CLI Client Interface")
    dprint(command)
    if command == "fork": fork_workflow()
    if command == "ship": ship_workflow()
    if command == "data": data_workflow()

if __name__ == "__main__":
    main()
