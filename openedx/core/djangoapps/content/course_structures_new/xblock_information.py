
class XBlockInformation(object):

    def __init__(self, usage_key, parent_keys, child_keys, block_fields, transformation_data):
        """
        Arguments:
            usage_key (UsageKey)
            parent_keys (list[UsageKey])
            child_keys (list[UsageKey])
            block_fields (dict[str: *])
            transformation_data (dict[str: C], where C = data_class of transformation type):
                Dictionary containing data collected by each transformation.
                {
                    'VisibilityTransformation': VisibilityTransformation.data_class(...)
                    'StartTransformation': StartTransformation.data_class(...)
                    ...
                }
        """
        self.usage_key = usage_key
        self.parent_keys = parent_keys
        self.child_keys = child_keys
        self.block_fields = block_fields
        self.transformation_data = transformation_data
