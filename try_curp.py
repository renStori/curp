import json

import click
from rich import print

from curp import Person, calculate_checksum, generate as gen_curp


@click.command()
@click.argument("command")
@click.argument("precurp", required=False)
def main(command, precurp) -> None:
    if command == "generate":
        with open("try_curp.json") as f:
            json_file = json.load(f)
        person = Person(**json_file)
        print(person.name)
        print(person.family_name)
        print(person.second_family_name)
        print(person.gender)
        print(person.birth_state)
        print(person.birth_date)
        curp = gen_curp(person)
        print(f"CURP: {curp}")
    elif command == "checksum" and precurp is not None:
        print(precurp + calculate_checksum(precurp))
    else:
        print("Invalid command or missing checksum")


if __name__ == "__main__":
    main()
