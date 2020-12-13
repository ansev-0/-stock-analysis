def basic_summary_from_dict(dictionary):
    return (72*'-').join(('SUMMARY\n', ) +
                            tuple(map(lambda d: f'\n{d[0]}: {d[1]}\n',
                                    dictionary.items())))