import click
import bin.client

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
        bin.client.fork_request(
                trainerID=trainerID,
                local=False,
                )

if __name__ == "__main__":
    main()
