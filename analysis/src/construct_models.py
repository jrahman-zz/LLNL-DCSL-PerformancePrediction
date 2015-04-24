import util

def construct_models(data, models):
 
    fitted_models = dict()

    grouped = data.groupby('application')    
    for application, group in grouped:
        fitted_models[application] = dict()
        group = util.get_nonmetadata(group)
        times = group['time']
        del group['time']
        
        for key in models.keys():
            model = models[key]()
            model.fit(times, group.values)
            fitted_models[application][key] = model

    return fitted_models
