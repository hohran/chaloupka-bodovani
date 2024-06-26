import generate as gen
from get_random import get_random, get_found_elements

class EndOfGameException(Exception):
    pass

def ask_for_skupinka() -> str:
    return input("Skupinka: ")

def is_int(string: str) -> bool:
    if len(string) == 0:
        return False
    for c in string:
        if c < '0' or c > '9':
            return False
    return True

def ask_for_action(action_names) -> int:
    print(f"Akce:")
    for (i,n) in enumerate(action_names):
        print(f'  {i+1} - {n}')
    print("")

    action_number = input("Vyber akci: ")

    if not is_int(action_number):
        return -1
    else:
        action = int(action_number)
        if action > len(action_names):
            return -1
        return action - 1

def add_to_founds(founds_path: str, new_element: str) -> None:
    with open(founds_path, "a") as f:
        f.write(f'{new_element}\n')

def main():
    game_folder = 'games'
    skupinka = ask_for_skupinka()
    skupinka += '.txt'
    founds_file = f'{game_folder}/{skupinka}'
    combofile = 'combo.txt'
    combos = gen.get_combos_from_file(combo_file=combofile)

    already_found_file = 'found.txt'
    found_today_file = 'found-today.txt'

    already_found = get_found_elements(already_found_file)
    
    def combine() -> None:
        combination = input("Elementy ke kombinaci: ")
        print(f'{combination=}')
        combination_elements = combination.split()
        if len(combination_elements) != 2:
            print("Chyba: Zadejte oba elementy s mezerou mezi nimi.")
            return
        e1 = combination_elements[0]
        e2 = combination_elements[1]
        result = gen.get_combo_result(combos, e1, e2)
        if result is None:
            print('Nejde\n')
            return
        element_usage = gen.get_elements_usage(combos)
        if result in element_usage:
            print(f'{result} - ({element_usage[result]} vyuziti)')
        else:
            print(f'{result} - (0 vyuziti)')

        if result not in already_found:
            print('\n!!!BINGO!!!')
        print("")

        add_to_founds(founds_file, result)
        add_to_founds(found_today_file, result)

    def hint() -> None:
        get_random(founds_file, combos)

    def end() -> None:
        raise EndOfGameException
        
    action_names = ['kombinovat', 'napoveda', 'ukoncit']
    actions = [combine, hint, end]

    while True:
        action_number = ask_for_action(action_names)
        if action_number == -1:
            continue
        try:
            actions[action_number]()
        except EndOfGameException:
            print("Konec, diky.")
            break


if __name__ == "__main__":
    main()
