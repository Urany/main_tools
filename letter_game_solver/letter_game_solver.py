from pathlib import Path
from urllib.request import urlopen
from itertools import permutations, combinations


def find_all_combos(letters_list: list[str]) -> list[tuple[str]]:
    combination_instances: list[tuple]=[]
    for i in range(3, len(letters_list)+1):
        combination_instances += list(combinations(letters_list, i))

    return combination_instances


def find_all_permutations(combinations_list) -> list[tuple[str]]:
    candidates: list[tuple]=[]
    for combo in combinations_list:
        candidates += list(permutations(combo))
    
    return candidates


def tuples_to_strings(permutations_list) -> list[str]:
    return ["".join(candidate) for candidate in permutations_list]


def write_results_to_file(candidates:list[str], matches:set[str]) -> None:
    cwd: Path = Path.cwd()
    with open (cwd/"list_combinations/results.txt", "w") as f:
        for cand in candidates:
            if cand in matches:
                f.writelines(cand+"\n")


def get_online_matches() -> set[str]:
    with urlopen("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt") as online_source:
        decoded_source:str = online_source.read().decode("utf-8")
    online_matches_set: set[str] = set(decoded_source.splitlines())
    return online_matches_set


def get_letters() -> list[str]:
    return ['c', 'i', 'o', 'n', 's', 's', 't']


def main() -> None:
    string_candidates_set: set[str] = set(tuples_to_strings(find_all_permutations(find_all_combos(get_letters()))))

    write_results_to_file(candidates=sorted(string_candidates_set), matches=get_online_matches())


if __name__ == "__main__":
    main()