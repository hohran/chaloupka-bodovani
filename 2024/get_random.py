import generate
import random
import time

def get_found_elements(filepath) -> list[str]:
    elements = []
    with open(filepath) as f:
        for e in f.readlines():
            elements.append(e[:-1])

    return elements


combofile = 'combo.txt'
found_elements_file = 'hra-vojta1.txt'

combos = generate.get_combos_from_file(combofile)
combos = generate.remove_empty_combos(combos)
found_elements = get_found_elements(found_elements_file)

reachable_results = generate.get_reachable_results(combos, found_elements)
print(random.choice(reachable_results))
