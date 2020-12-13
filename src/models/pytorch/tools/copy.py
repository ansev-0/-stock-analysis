def torch_model_copy(model_to_copy):
    model_copy = type(model_to_copy)()
    model_copy.load_state_dict(model_to_copy.state_dict())
    return model_copy