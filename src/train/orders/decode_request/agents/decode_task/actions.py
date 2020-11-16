from src.model_environment.run.run import OutputModelActionAdapter

class DecodeActionsTask:


    def __call__(self, dict_actions):
        output_adapter = OutputModelActionAdapter(False)

        if 'no_action' in dict_actions.keys():
            output_adapter.add_no_action()

        return self._decode_buy_and_sell(dict_actions, output_adapter)

    def _decode_buy_and_sell(self, dict_actions, output_adapter):

        for action, action_params in dict_actions.items():
            for type_action, value in action_params.items():
                try:
                    getattr(output_adapter, f'add_{action}_{type_action}')(value)
                except Exception:
                    pass

        return output_adapter
