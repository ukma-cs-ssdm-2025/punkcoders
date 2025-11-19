def find_failed_attr_in_err_response(data, attr):
    if "errors" not in data:
        raise AssertionError(f'"errors" not in {data}')
    for err in data["errors"]:
        if err["attr"] == attr:
            return err
    raise AssertionError(f'no error on "{attr}" in {data}')
