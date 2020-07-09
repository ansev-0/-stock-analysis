from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.models import load_model
from keras.optimizers import Adam

def train_model(model, x_train, y_train, epochs, name_model):
    
    earlyStopping = EarlyStopping(monitor='val_loss', patience=12, verbose=0, mode='min')
    mcp_save = ModelCheckpoint(name_model, save_best_only=True,
                               monitor='val_loss', mode='min')
    reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1,
                                       patience=10, verbose=1, min_delta=1e-4, mode='min')
    
    results_1 = model.fit(x_train, y_train,
                          validation_split=0.2,
                          epochs=epochs, 
                          callbacks=[earlyStopping, mcp_save, reduce_lr_loss]
                         )
    

    
    earlyStopping = EarlyStopping(monitor='loss', patience=12, verbose=0, mode='min')
    mcp_save = ModelCheckpoint(name_model, save_best_only=True,
                               monitor='loss', mode='min')
    reduce_lr_loss = ReduceLROnPlateau(monitor='loss', factor=0.1,
                                   patience=10, verbose=1, min_delta=1e-4, mode='min')

    best_model = load_model(name_model)
    best_model.compile(Adam(learning_rate=0.00005), loss='mse')

    results_2 = best_model.fit(x_train, y_train, epochs=100, 
                               callbacks=[earlyStopping, mcp_save, reduce_lr_loss])
    best_model = load_model(name_model)
    
    return best_model, results_1.history, results_2.history
