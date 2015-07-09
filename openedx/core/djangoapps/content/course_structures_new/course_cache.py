
from .xblock_information import XBlockInformation, XBlockInformation
from .transformations import TRANSFORMATIONS


def _load_block_tree(block, block_map, parent_map, child_map):
    """
    Arguments:
        block (XBlock)
        block_map (dict[UsageKey: XBlock])
        parent_map (dict[UsageKey: list[UsageKey])
        child_map (dict[UsageKey: list[UsageKey])
    """
    block_map[block.usage_key] = block
    child_map[block.usage_key] = []

    children = block.get_children()
    for child in children:
        child_map[block.usage_key].append(child.usage_key)
        if child.usage_key in parent_map:
            # Child has already been visited.
            # Just add block to the existing parent_map entry.
            parent_map[child.usage_key].append(block.usage_key)
        else:
            # Child hasn't yet been visited.
            # Add it to parent_map and recurse.
            parent_map[child.usage_key] = [block.usage_key]
            _load_block_tree(child, block_map, parent_map, child_map)


def _get_block_information_for_cache(root_block):
    """
    Arguments:
        root_block (XBlock)

    Returns:
        dict[UsageKey: XBlockInformation]: All blocks under root_block_key.
            Contains information from the "collect" phase.
    """

    # Load entire course hierarchy.
    block_map = {}
    parent_map = {}
    child_map = {}
    _load_block_tree(root_block, block_map, parent_map, child_map)

    # Define functions for traversing course hierarchy.
    get_children = lambda block: [
        block_map[child_key] for child_key in child_map[block.usage_key]
    ]
    get_parents = lambda block: [
        block_map[child_key] for child_key in parent_map[block.usage_key]
    ]

    # For each transformation, extract required fields and collect specially
    # computed data.
    required_fields = set()
    collected_data = {}
    for transformation in TRANSFORMATIONS:
        required_fields |= transformation.required_fields
        collected_data[transformation.__name__] = transformation.collect(root_block, get_children, get_parents)

    # Build a dictionary mapping usage keys to block information.
    return {
        usage_key: XBlockInformation(
            usage_key,
            parent_map[usage_key],
            child_map[usage_key],
            {
                required_field.__name__: getattr(block, required_field)
                for required_field in required_fields
            },
            {
                transformation_name: collected_data[transformation_name][usage_key]
                for transformation_name in collected_data
            }
        )
        for usage_key, block in block_map.iteritems()
    }


def _get_block_information_for_user(root_block, cached_block_information, user):
    """
    Arguments:
        root_block_key (UsageKey)
        block_information (dict[UsageKey: XBlockInformation]): All blocks under
            root_block_key. Contains information from the "collect" phase.
        user (User)

    Returns:
        dict[UsageKey: XBlockInformation]: User-specific blocks under
            root_block_key. Contains information from after the
            "apply" phase.
    """
    result = cached_block_information.copy()
    for transformation in TRANSFORMATIONS:
        transformation.apply(root_block, result, user)
    for __, block in result.iteritems():
        # Remove information that was necessary for generating the course, but
        # that we don't want to give back to the caller.
        # TODO: instead, do this using inheritance or something
        block.transformation_data = None
        block.parents = None
    return result
