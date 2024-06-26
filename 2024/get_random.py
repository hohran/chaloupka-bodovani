import generate
import random
import time

def get_found_elements(filepath) -> list[str]:
    elements = []
    with open(filepath) as f:
        for e in f.readlines():
            elements.append(e[:-1])

    return elements

def get_random(founds_path: str, combos=None) -> None:
    combofile = 'combo.txt'
    # founds_parent_folder = 'games'
    # found_elements_file = f'{founds_parent_folder}/{founds_path}'


    if combos is None:
        combos = generate.get_combos_from_file(combofile)
        combos = generate.remove_empty_combos(combos)
    found_elements = get_found_elements(founds_path)


    reachable_results = generate.get_reachable_results(combos, found_elements)
    print(random.choice(reachable_results))
