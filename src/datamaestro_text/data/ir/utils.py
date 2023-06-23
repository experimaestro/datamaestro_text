from ir_datasets.formats import GenericQuery, GenericDoc


def get_text(object) -> str:
    """Returns the text of an object (e.g. query, document)

    :param query: any object
    """
    if isinstance(object, GenericQuery, GenericDoc):
        return object.text

    raise NotImplementedError(
        f"No pre-defined method to retrieve the text of an object of type {type(object)}"
    )


def get_qid_text(object) -> str:
    """Returns the ID and the text of an object (e.g. query, document)

    :param query: any object
    """
    if isinstance(object, GenericDoc):
        return object.doc_id, object.text

    if isinstance(object, GenericQuery):
        return object.query_id, object.text

    raise NotImplementedError(
        f"No pre-defined method to retrieve the text of an object of type {type(object)}"
    )
