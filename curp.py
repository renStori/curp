import re
from unidecode import unidecode
from rich import print

genders = {
    "M": "H",
    "F": "M",
}

states = {
    "AGU": "AS",
    "BCN": "BC",
    "BCS": "BS",
    "CAM": "CC",
    "CHP": "CS",
    "CHH": "CH",
    "COA": "CL",
    "COL": "CM",
    "CMX": "DF",
    "DUR": "DG",
    "GUA": "GT",
    "GRO": "GR",
    "HID": "HG",
    "JAL": "JC",
    "MEX": "MC",
    "MIC": "MN",
    "MOR": "MS",
    "NAY": "NT",
    "NE": "NE",
    "NEX": "NE",
    "NLE": "NL",
    "OAX": "OC",
    "PUE": "PL",
    "QUE": "QT",
    "ROO": "QR",
    "SLP": "SP",
    "SIN": "SL",
    "SON": "SR",
    "TAB": "TC",
    "TAM": "TS",
    "TLA": "TL",
    "VER": "VZ",
    "YUC": "YN",
    "ZAC": "ZS",
}

commons = [
    "MARIA DEL ",
    "MARIA DE LOS ",
    "MARIA ",
    "JOSE DE ",
    "JOSE ",
    "MA. ",
    "MA ",
    "M. ",
    "J. ",
    "J ",
    "M ",
]

inconvenient_words = {
    "BACA": "BXCA",
    "BAKA": "BXKA",
    "BUEI": "BXEI",
    "BUEY": "BXEY",
    "CACA": "CXCA",
    "CACO": "CXCO",
    "CAGA": "CXGA",
    "CAGO": "CXGO",
    "CAKA": "CXKA",
    "CAKO": "CXKO",
    "COGE": "CXGE",
    "COGI": "CXGI",
    "COJA": "CXJA",
    "COJE": "CXJE",
    "COJI": "CXJI",
    "COJO": "CXJO",
    "COLA": "CXLA",
    "CULO": "CXLO",
    "FALO": "FXLO",
    "FETO": "FXTO",
    "GETA": "GXTA",
    "GUEI": "GXEI",
    "GUEY": "GXEY",
    "JETA": "JXTA",
    "JOTO": "JXTO",
    "KACA": "KXCA",
    "KACO": "KXCO",
    "KAGA": "KXGA",
    "KAGO": "KXGO",
    "KAKA": "KXKA",
    "KAKO": "KXKO",
    "KOGE": "KXGE",
    "KOGI": "KXGI",
    "KOJA": "KXJA",
    "KOJE": "KXJE",
    "KOJI": "KXJI",
    "KOJO": "KXJO",
    "KOLA": "KXLA",
    "KULO": "KXLO",
    "LILO": "LXLO",
    "LOCA": "LXCA",
    "LOCO": "LXCO",
    "LOKA": "LXKA",
    "LOKO": "LXKO",
    "MAME": "MXME",
    "MAMO": "MXMO",
    "MEAR": "MXAR",
    "MEAS": "MXAS",
    "MEON": "MXON",
    "MIAR": "MXAR",
    "MION": "MXON",
    "MOCO": "MXCO",
    "MOKO": "MXKO",
    "MULA": "MXLA",
    "MULO": "MXLO",
    "NACA": "NXCA",
    "NACO": "NXCO",
    "PEDA": "PXDA",
    "PEDO": "PXDO",
    "PENE": "PXNE",
    "PIPI": "PXPI",
    "PITO": "PXTO",
    "POPO": "PXPO",
    "PUTA": "PXTA",
    "PUTO": "PXTO",
    "QULO": "QXLO",
    "RATA": "RXTA",
    "ROBA": "RXBA",
    "ROBE": "RXBE",
    "ROBO": "RXBO",
    "RUIN": "RXIN",
    "SENO": "SXNO",
    "TETA": "TXTA",
    "VACA": "VXCA",
    "VAGA": "VXGA",
    "VAGO": "VXGO",
    "VAKA": "VXKA",
    "VUEI": "VXEI",
    "VUEY": "VXEY",
    "WUEI": "WXEI",
    "WUEY": "WXEY",
}


class Person:
    def __init__(
        self,
        name: str,
        family_name: str,
        second_family_name: str,
        gender: str,
        birth_state: str,
        birth_date: str,
    ) -> None:
        self.name = normalize_string(name)
        self.family_name = normalize_string(family_name)
        self.second_family_name = normalize_string(second_family_name)
        self.gender = normalize_string(gender)
        self.birth_state = normalize_string(birth_state)
        self.birth_date = normalize_string(birth_date)


def compound_terms(string: str) -> str:
    compounds = r"\bDA\b|\bDAS\b|\bVON\b|\bY\b|\bDE\b|\bDEL\b|\bDER\b|\bDI\b|\bDIE\b|\bDD\b|\bEL\b|\bLA\b|\bLOS\b|\bLAS\b|\bLE\b|\bLES\b|\bMAC\b|\bMC\b|\bVAN\b|\bVON\b|\bY\b"
    return re.sub(compounds, "", string).replace("  ", " ").strip()


def normalize_string(string: str = None) -> str:
    if string:
        try:
            string = string.strip().upper().replace("Ñ", "X")
        except AttributeError as e:
            print(string)
            print(e)
        return unidecode(string)
    return string


def calculate_checksum(curp: str) -> str:
    dictionary = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    try:
        ln_sum = sum(dictionary.index(curp[i]) * (18 - i) for i in range(17))
    except ValueError:
        print(f"Pre CURPS: {curp}")
    ln_digt = 10 - (ln_sum % 10)
    return str(ln_digt)[-1]


def get_century_diff(birth_date: str) -> str:
    year = birth_date.split("-")[0]
    return ["0", "A"][int(year) // 1000 - 1]


def get_name_to_use(first_name: str) -> str:
    names = first_name.split()
    if len(names) == 1:
        return names[0]
    is_common = any(first_name.startswith(c) for c in commons)
    return names[1] if is_common else names[0]


def get_date_part(birth_date: str) -> str:
    year, month, day = birth_date.split("-")
    return f"{str(int(year) % 100).zfill(2)}{month}{day}"


def remove_inconvenient(full_name_part: str) -> str:
    return inconvenient_words.get(full_name_part, full_name_part)


def get_gender(gender: str) -> str:
    return genders.get(gender)


def get_state(birth_state: str) -> str:
    return states.get(birth_state)


def get_first_inner_consonant(word: str = None) -> str:
    if not word:
        return "X"
    inner_consonants = "".join([x for x in word if x not in ["A", "E", "I", "O", "U"]])
    if not inner_consonants:
        inner_cons = "X"
    else:
        if word[0] == inner_consonants[0]:
            if len(inner_consonants) == 1:
                inner_cons = "X"
            else:
                inner_cons = inner_consonants[1]
        else:
            inner_cons = inner_consonants[0]
    return inner_cons if inner_cons != "Ñ" else "X"


def get_first_letter(word: str = None) -> str:
    if word and word[0] != "Ñ":
        first_cons = word[0]
    else:
        first_cons = "X"
    return first_cons


def get_inner_vowel(word: str) -> str:
    vowels = "".join([x for x in word if x in ["A", "E", "I", "O", "U"]])
    vowel = vowels[0]
    if not vowels or (len(vowels) == 1 and word[0] == vowels[0]):
        vowel = "X"
    elif len(vowels) > 1:
        if vowels[0] == word[0]:
            vowel = vowels[1]
    return vowel


def calculate_name_parts(
    name: str, family_name: str, second_family_name: str = None
) -> tuple:
    outer = "".join(
        [
            get_first_letter(family_name),
            get_inner_vowel(family_name),
            get_first_letter(second_family_name),
            get_first_letter(name),
        ]
    )
    outer = remove_inconvenient(outer)
    inner = "".join(
        [
            get_first_inner_consonant(family_name),
            get_first_inner_consonant(second_family_name),
            get_first_inner_consonant(name),
        ]
    )
    return outer, inner


def validate_data(person: Person) -> bool:
    if not person.name:
        raise ValueError("Name is required")
    if not person.family_name:
        raise ValueError("Family name is required")
    if not person.birth_date:
        raise ValueError("Birth date is required")
    if not person.gender:
        raise ValueError("Gender is required")
    if not person.birth_state:
        raise ValueError("Birth state is required")
    return True


def generate(person: Person) -> str:
    try:
        validate_data(person)
    except ValueError as e:
        return str(e)
    else:
        name = get_name_to_use(compound_terms(person.name))
        family_name = compound_terms(person.family_name)
        second_family_name = (
            compound_terms(person.second_family_name)
            if person.second_family_name
            else None
        )
        outer_name_part, inner_name_part = calculate_name_parts(
            name, family_name, second_family_name
        )
        date_part = get_date_part(person.birth_date)
        gender_part = get_gender(person.gender)
        state_part = get_state(person.birth_state)
        century_digit = get_century_diff(person.birth_date)
        pre_curp = f"{outer_name_part}{date_part}{gender_part}{state_part}{inner_name_part}{century_digit}"
        return pre_curp + calculate_checksum(pre_curp)


def validate(curp: str) -> bool:
    regex = r"^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$"
    valid = re.match(regex, curp)
    if not valid:
        return False
    source_pre_curp = valid.group(1)
    source_checksum = valid.group(2)
    checksum = calculate_checksum(source_pre_curp)
    return valid and source_checksum == checksum
