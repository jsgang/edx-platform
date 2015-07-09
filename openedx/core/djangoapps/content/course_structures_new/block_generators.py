
def generate_blocks_pre_order(start_block, block_access_checker, get_children):
    stack = [start_block]
    while stack:
        curr_block = stack.pop()

        if block_access_checker(curr_block):
            yield curr_block

            if curr_block.has_children:
                children = get_children(curr_block)
                for block in reversed(children):
                    stack.append(block)

def generate_blocks_topological(start_block, get_parents, get_children=None, block_access_checker=None):
    visited_block_keys = set()
    for block in generate_blocks_pre_order(start_block, block_access_checker, get_children):
        parents = get_parents(block)
        all_parents_visited = all(parent.usage_key in visited_block_keys for parent in parents)
        if all_parents_visited:
            visited_block_keys.add(block.usage_key)
            yield block

