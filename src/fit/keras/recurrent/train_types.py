class OneBatchTrain:
    '''
    In this type of training SAMPLES == BATCH_SIZE,
    Moreover the state is not preserved at the end 
    (which could be done for prediction or evaluation tasks,
    see the rest of class).
    '''
    pass 

class OneBatchKeepEndStateTrain:
    '''
    In this type of training SAMPLES == BATCH_SIZE,
    Moreover the state is  preserved at the end.
    '''
    pass

class ManyBatchTrain:
    '''
    In this type of training BATCH_SIZE is N times less than SAMPLES,
    being N a natural number.
    '''
    pass

class ManyBatchStatefulTrain:
    '''
    In this type of training BATCH_SIZE is N times less than SAMPLES being n a natural number.
    The state is transferred from one batch to another using stateful = True.
    '''
    pass

class ManyBatchStatefulKeepEndStateTrain:
    '''
    In this type of training BATCH_SIZE is N times less than SAMPLES being N a natural number.
    The state is transferred from one batch to another using stateful = True.
    In addition, the state is preserved in the last training period,
    which can be useful for prediction or evaluation tasks with training data
    immediately subsequent chronologically.
    '''
    pass