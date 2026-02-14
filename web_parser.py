from bs4 import BeautifulSoup

class Stratagem:
    def __init__(self, name: str, arrows: list[str]) -> None:
        self.name: str = name
        self.arrows: list[str] = arrows


def parse_content(content: str) -> list[Stratagem]:
    soup = BeautifulSoup(content, 'html.parser')
    rows = soup.find_all('tr')  # First h1 tag
    rows = [x.find_all('td') for x in rows]

    stratagems: list[Stratagem] = []
    for tds in rows:

        try:
            name = tds[1].text.strip()

            images = tds[2].find_all("img")
            arrows = []
            for image in images:
                arrow = image.attrs.get("alt")
                if arrow is None:
                    break;
                arrow = str(arrow)
                if arrow.startswith("Stratagem Arrow Down"):
                    arrow = "Down"
                elif arrow.startswith("Stratagem Arrow Left"):
                    arrow = "Left"
                elif arrow.startswith("Stratagem Arrow Right"):
                    arrow = "Right"
                elif arrow.startswith("Stratagem Arrow Up"):
                    arrow = "Up"
                else:
                    raise Exception("Did not recognize arrow type!")

                arrows.append(arrow)

            s = Stratagem(name, arrows)
            stratagems.append(s)
        except:
            pass

    return stratagems


if __name__ == "__main__":
    with open("./stratagems.html", 'r') as f:
        content = f.read()

    stratagems = parse_content(content)
    filtered_stratagems = []
    for s in stratagems:
        if len(s.name) == 0:
            continue
        elif len(s.arrows) == 0:
            continue
        s.name = s.name.replace('"', '\\"')
        filtered_stratagems.append(s)

    strats = [f"Stratagem::new(\"{s.name}\".to_string(), vec![{','.join([f"Binding::{k}" for k in s.arrows])}])" for s in filtered_stratagems]
    print(",\n".join(strats))
