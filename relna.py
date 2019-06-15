import click
import bin.client
import logging
import os
import configparser

DELIMITER = "="*30
def dprint(content):
    print(DELIMITER+"\n"+content+"\n"+DELIMITER)

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
    trainer_files += os.listdir(os.path.join(trainer_folder, "trainer"))
    logging.warning("[relna.ship] shipping trainer with the following files (in the zip)")
    for file_name in trainer_files: 
        logging.warning("- {}".format(file_name))
    bin.client.prepare_payload(
            trainer_folder,
            payload_folder_name=payload_folder)

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(
            os.path.join(trainer_folder, "trainer.config")
            )
    trainer_metadata = config['TRAINER_METADATA']
    logging.warning("[relna.ship] shipping trainer with the following config")
    for field, value in trainer_metadata.items():
        logging.warning("- {} : {}".format(field, value))

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

@click.command()
@click.option("--command", default="fork", help = "fork, ship")
def main(command):
    dprint("relna - CLI Client Interface")
    dprint(command)
    if command == "fork": fork_workflow()
    if command == "ship": ship_workflow()

if __name__ == "__main__":
    main()
