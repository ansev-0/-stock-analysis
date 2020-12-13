general_info_external_fields = ('username', 'password', 'email', 'phone_number')
general_info_fields = general_info_external_fields + ('online', 'confirmed')

general_info_fields_with_dates = general_info_fields + tuple(map(lambda info: f'date_last_change_{info}',
                                                                  general_info_fields)
                                                            ) 


