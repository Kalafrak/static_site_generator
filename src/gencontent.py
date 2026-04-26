def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            stripped_prefix = line.removeprefix("# ")
            stripped_line = stripped_prefix.strip()
            return stripped_line
    raise Exception("No title found!")
