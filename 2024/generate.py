#!/usr/bin/python

import re

class Combo:
    def __init__(self, e1, e2, result=None) -> None:
        self.e1 = e1 if not isinstance(e1, Element) else e1.name
        self.e2 = e2 if not isinstance(e2, Element) else e2.name
        self.result = result

    def __repr__(self) -> str:
        return f'{self.e1} + {self.e2} => {self.result if self.result is not None else "???"}'
    
    def __str__(self) -> str:
        return f'{self.e1} + {self.e2} => {self.result if self.result is not None else "???"}'
    
    def __eq__(self, value: object) -> bool:
        if self.e1 == value.e1 and self.e2 == value.e2:
            return True
        if self.e1 == value.e2 and self.e2 == value.e1:
            return True
        return False
    
class Element:
    def __init__(self, name, value) -> None:
        self.name : str = name
        self.value = value

    def __repr__(self) -> str:
        return f'{self.name} ({self.value})'
    
    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self.name == value
        if isinstance(value, Element):
            return self.name == value.name and self.value == value.value
        else:
            return False

def is_word(string: str) -> bool:
    return re.match('^[a-zA-Z]+$', string)

def is_unknown(string: str) -> bool:
    return re.match('^\?+$', string)

def is_value(string: str) -> bool:
    return re.match('^\([1-9][0-9]*\)$', string)

def check_combo_line_parts_syntax(line_parts: list[str]) -> bool:
    if not is_word(line_parts[0]):
        return False
    if line_parts[1] != '+':
        return False
    if not is_word(line_parts[2]):
        return False
    if line_parts[3] != '=>':
        return False
    
    if len(line_parts) != 5:
        return True
    if not is_word(line_parts[4]) and not is_unknown(line_parts[4]):
        return False
    return True
    

def get_combo_from_line(line: str) -> Combo | None:
    parts = line.split()

    if len(parts) not in [4,5]:
        return None
    
    if not check_combo_line_parts_syntax(parts):
        return None
    
    e1 = parts[0]
    e2 = parts[2]
    if len(parts) == 5:
        result = parts[4] if is_word(parts[4]) else None

    return Combo(e1,e2,result)
    
def get_reachable_results(combos: list[Combo], found_elements: list[str]) -> list[str]:
    results = []
    for combo in combos:
        if combo.e1 in found_elements and combo.e2 in found_elements and combo.result not in found_elements:
            results.append(combo.result)
    return results

def get_combos_from_file(combo_file) -> list[Combo]:
    combos = []
    with open(combo_file) as f:
        for line in f.readlines():
            new_combo = get_combo_from_line(line)
            if new_combo is not None:
                if new_combo in combos:
                    raise RuntimeError(f'Multiple appearances of combination of {new_combo.e1} and {new_combo.e2}')
                combos.append(new_combo)
    return combos

def get_element_from_line(line: str) -> Element | None:
    line_parts = line.split()
    # Skip empty lines
    if len(line_parts) == 0:
        return None
    if len(line_parts) != 2:
        print(f'Line "{line}" does not represent an element')
        return None
    if not is_word(line_parts[0]):
        print(f'Name of an element must consist only of letters (not "{line_parts[0]}")')
        return None
    if not is_value(line_parts[1]):
        print(f'Invalid element value "{line_parts[1]}"')
        return None
    
    name = line_parts[0]
    value = int(line_parts[1][1:-1])
    return Element(name, value)

def remove_empty_combos(combos: list[Combo]) -> list[Combo]:
    new_combos = []
    for combo in combos:
        if combo.result is not None:
            new_combos.append(combo)
    return new_combos

def get_elements_from_file(element_file) -> set[Element]:
    elements = set()
    with open(element_file) as f:
        for line in f.readlines():
            element = get_element_from_line(line)
            if element is None:
                continue
            elements.add(element)
    return elements

def check_combinations(combos: list[Combo], elements: set[Element]) -> set[Element]:
    generated = set()

    def check_element(element: Element) -> int:
        for e in elements:
            if element == e:
                generated.add(e)
                return e.value
        raise RuntimeError(f'Element "{element}" is unknown.')

    for combo in combos:
        v1 = check_element(combo.e1)
        v2 = check_element(combo.e2)

        if combo.result is not None:
            r = combo.result
            if r in elements:
                continue
            else:
                elements.add(Element(r,v1+v2))
        
    return generated

def generate(elements: set[Element], generated: set[Element]) -> set[Combo]:
    generated_combos = []
    for e1 in elements:
        if e1 in generated:
            continue
        for e2 in elements:
            new_combo = Combo(e1,e2)
            if new_combo not in generated_combos:
                generated_combos.append(new_combo)
    return generated_combos

def rewrite_combos(new_combos: list[Combo], combinations_file: str) -> None:
    if len(new_combos) == 0:
        return
    with open(combinations_file, "a") as f:
        f.write("\n")
        for combo in new_combos:
            f.write(f'{combo}\n')

def rewrite_elements(elements: set[str], elements_file: str) -> None:
    elements_copy = list(elements)
    def sort_func(e: Element):
        return e.value
    elements_copy.sort(key=sort_func)
    with open(elements_file, "w") as f:
        for e in elements_copy:
            f.write(f'{e}\n')

def get_elements_usage(combos: list[Combo]) -> dict[str,int]:
    usage = {}
    for combo in combos:
        if combo.result is None:
            continue

        def incr(e: Element):
            if e not in usage:
                usage[e] = 1
            else:
                usage[e] += 1

        incr(combo.e1)
        incr(combo.e2)

        if combo.e1 == combo.e2:
            usage[combo.e1] -= 1

    return usage

if __name__ == "__main__":
    combinations_file = "combo.txt"
    combos = get_combos_from_file(combinations_file)
    elements_file = "element.txt"
    elements = get_elements_from_file(elements_file)
    generated = check_combinations(combos, elements)
    to_generate = generate(elements, generated)
    rewrite_combos(to_generate, combinations_file)
    rewrite_elements(elements, elements_file)
    print(get_elements_usage(combos))



    

