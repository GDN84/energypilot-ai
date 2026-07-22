def get_metadata(metadata, key, fallback=""):

    if not metadata:
        return fallback

    value = metadata.get(key)

    if value is None:
        return fallback

    return str(value)