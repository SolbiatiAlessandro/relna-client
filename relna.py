import click
import bin.client
import logging
import os

DELIMITER = "="*30
def dprint(content):
    print(DELIMITER+"\n"+content+"\n"+DELIMITER)

@click.command()
@click.option("--command", default="fork", help = "fork, ship")
def main(command):
    dprint("relna - CLI Client Interface")
    dprint(command)
    if command == "fork":
        print("Enter the TrainerID you want to fork: ")
        trainerID = input()
        logging.warning("relna-client:relna:fork starting fork for trainer {}".format(trainerID))
        bin.client.fork_request(
                trainerID=trainerID,
                local=False,
                )
        logging.warning("relna-client:relna:fork fork for trainer {} completed".format(trainerID))
    if command == "ship":
        trainer_folder = "./relna_trainer"
        logging.warning("relna-client:relna:ship reading trainer from {}".format(trainer_folder))
        PAYLOAD_FOLDER = "./payload"
        bin.client.prepare_payload(
                trainer_folder,
                payload_folder_name=PAYLOAD_FOLDER)
        bin.client.ship_request(
                zipped_code_path=os.path.join(PAYLOAD_FOLDER, "trainer.zip"),
                trainer_pkg_path=os.path.join(PAYLOAD_FOLDER, "trainer-0.1.tar.gz")
                )
        logging.warning("relna-client:relna:ship ship request completed")


if __name__ == "__main__":
    main()
