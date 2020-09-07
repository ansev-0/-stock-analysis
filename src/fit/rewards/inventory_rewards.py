def inventory_rewards(value_inventory, new_value, action):

    diff = new_value - value_inventory

    if action.lower() == 'buy':
        return -diff
    elif action.lower() == 'sell':
        return diff
    else:
        raise ValueError('Invalid action')