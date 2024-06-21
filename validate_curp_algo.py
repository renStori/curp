import pandas as pd
from rich import print

from curp import Person, calculate_checksum, generate, validate

csv = pd.read_csv("forced_corrected.csv")
csv = csv.fillna("")


def trim_row(row):
    return row[
        [
            "user_id",
            "name",
            "first_lastname",
            "second_lastname",
            "gender",
            "birth_state",
            "birth_date",
            "nationality",
            "curp",
        ]
    ]


def get(curp):
    row = csv[csv["curp"] == curp].iloc[0]
    return trim_row(row)


for _, row in csv.iterrows():
    if not validate(row["curp"]):
        print(row)


mismatch = []
for _, row in csv.iterrows():
    person = Person(
        name=row["name"],
        family_name=row["first_lastname"],
        second_family_name=row["second_lastname"],
        gender=row["gender"],
        birth_state=row["birth_state"],
        birth_date=row["birth_date"],
    )
    CURP = generate(person)
    if row["curp"] != CURP:
        m = row["curp"], CURP
        mismatch.append(m)


errors = []
for m in mismatch:
    original, recalculated = m
    err = {
        "original": original,
        "recalculated": recalculated,
        "outer_name": original[:4] != recalculated[:4],
        "date": original[4:10] != recalculated[4:10],
        "gender": original[10] != recalculated[10],
        "state": original[11:13] != recalculated[11:13],
        "inner_name": original[13:16] != recalculated[13:16],
        "homonimia": original[-2:-1] != recalculated[-2:-1]
        and original[:-2] == recalculated[:-2],
        "checksum": original[-1] != recalculated[-1]
        and original[:-1]
        == recalculated[:-1],  # Everything's the same except very last character
        "checksum_not_recalculated": "",
    }
    errors.append(err)

err = pd.DataFrame(errors)


def examine(df: pd.DataFrame):
    if len(df):
        print(df)
        for _, row in df.iterrows():
            print(get(row["original"]))


examine(err[(err["homonimia"] == False) & err["outer_name"]])
examine(err[(err["homonimia"] == False) & err["date"]])
examine(err[(err["homonimia"] == False) & err["gender"]])
examine(err[(err["homonimia"] == False) & err["state"]])
examine(err[(err["homonimia"] == False) & err["inner_name"]])
examine(err[err["homonimia"]])
examine(err[(err["homonimia"] == False) & err["checksum"]])


print(err.sum())
print(len(mismatch) / len(csv))
