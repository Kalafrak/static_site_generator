def markdown_to_blocks(markdown):
    blocks = []
    splits = markdown.split("\n\n")
    for split in splits:
        block = split.strip()
        if block != "":
            blocks.append(block)
    return blocks
