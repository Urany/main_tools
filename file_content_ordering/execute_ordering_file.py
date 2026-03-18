from tkinter import filedialog
from pathlib import Path
import tempfile


def sort_file(path : Path) -> None:
    with open (path, "r", encoding="utf-8") as file:
        lines: list[str] = sorted(line.strip() + "\n" for line in file if line.strip())

    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=path.parent) as temp_file:
        temp_file.writelines(lines)
        temp_path = Path(temp_file.name)
        temp_path.replace(path)



def main() -> None:
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    sort_file(Path(file_path))

if __name__=="__main__":
    main()
