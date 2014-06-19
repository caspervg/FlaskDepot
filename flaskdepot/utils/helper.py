from flask import url_for as flask_url_for


def url_for(endpoint, **values):
    """
    Generates a URL to the given endpoint with the method provided
        :param endpoint: the endpoint of the URL (name of the function)
        :param values: the variable arguments of the URL rule
        :param _params: if provided this dictionary is used to add additional parameters at runtime
    """
    runtime_parameters = values.pop('_params', None)
    if runtime_parameters:
        for k, v in runtime_parameters.items():
            # Make sure we don't overwrite compile time arguments
            if not k in values.keys():
                values[k] = v
    return flask_url_for(endpoint, **values)