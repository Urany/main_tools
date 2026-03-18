import re
from time import strftime, localtime
from tkinter import Tk, Label, Button, Text, filedialog, END
from typing import Literal


###
###FRONTEND
###

class MyGUI:
    def __init__(self):
        
        def get_filepaths() -> (tuple[str, ...] | Literal['']):
            return filedialog.askopenfilenames(filetypes=[("prefabs", "*.prefab")])

        def add_prefab_to_textbox(prefabs: list[str]) -> None:
            for prefab in prefabs:
                self.textbox.insert(END, prefab)

        def execute_analysis() -> None:
            filepaths = get_filepaths()
            if filepaths:
                for filepath in filepaths:
                    try:
                        address_description = f"\nUnique prefabs in {filepath}:\n\n"
                        self.textbox.insert(END, address_description)
                        add_prefab_to_textbox(read_file(filepath))
                    except Exception as e:
                        exception_text = f"There was an error reading file {filepath}.\nError: {str(e)}"
                        self.textbox.insert(END, exception_text)
                        break
                    
                    self.textbox.insert(END, f"\n{"-" * 15} FILE END {"-" * 15}\n\n")

                endReportText = f"\n{"-" * 15}\nEND OF REPORT - Retrieved at: {get_current_time()}\n{"-" * 15}\n"
                self.textbox.insert(END, endReportText)



        self.root = Tk()
        self.root.geometry("700x600")
        self.root.title("Find prefabs in prefabs")


        self.label = Label(self.root, 
                           text="Unique instances of prefabs in prefab files", 
                           font=("Arial", 18),
                           padx=10,
                           pady=20
                           )
        
        self.button_exit = Button(self.root, 
                                  text="Exit", 
                                  command=self.root.quit
                                  )
        
        self.button_open_file = Button(self.root, 
                                       text="Open Prefab File(s)", 
                                       command=execute_analysis,
                                       padx=10,
                                       pady=10
                                       )

        self.textbox = Text(self.root, 
                            height=25, 
                            width=90,
                            font=("Arial", 8),
                            bg= "light yellow",
                            padx=5,
                            pady=5,
                            fg= "black",
                            xscrollcommand="True",
                            yscrollcommand="True",
                            )
        

        self.label.pack()
        self.button_open_file.pack()
        self.textbox.pack(padx=20, pady=20)
        self.button_exit.pack(pady=20)


        self.root.mainloop()



###
###Backend
###



def find_prefabs_in_file(fileContent: str) -> set[str]:

    pattern: str = r'(?<="m_PrefabName":\s\[12,\s").*\b'
    matches: list[str] = re.findall(pattern, fileContent)

    setOfPrefabs:set[str] = {f"{prefab}.prefab\n" for prefab in matches}

    if not setOfPrefabs:
        setOfPrefabs.add(f"{"-" * 15} No prefabs found in file. {"-" * 15}\n")

    return setOfPrefabs


def get_current_time() -> str:

    """
    Gets current local time and returns it in form HH:MM:SS

    :Example:
    >>> get_current_time()
    "20:59:19"
    """

    return str(strftime("%H:%M:%S", localtime()))


def read_file(filepath: str) -> list[str]:
    with open (filepath) as file:
        prefabs: list[str] = sorted(find_prefabs_in_file(file.read()))
    return prefabs


def main() -> None:
    MyGUI()

if __name__ == "__main__":
    main()