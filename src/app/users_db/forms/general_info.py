general_info_valid_fields = ('username', 'password', 'email', 'phone_number')

general_info_valid_fields = general_info_valid_fields + tuple(map(lambda info: f'update_date_{info}',
                                                                  general_info_valid_fields)
                                                             ) + ('validated', )