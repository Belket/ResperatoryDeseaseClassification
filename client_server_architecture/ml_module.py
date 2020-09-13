from server_information import ServerErrors
import os


class MLModule:

    processing = None
    models = None

    @staticmethod
    def fit_model(session, filter_method, balancing_method, model):
        scores = {"accuracy": "", "recall": "", "precision": "", "f_score": ""}
        error_code, df = MLModule.models.read_df(session)
        if error_code == ServerErrors.NO_ERROR:
            error_code, df = MLModule.models.modify_df(df)
            if error_code == ServerErrors.NO_ERROR:
                error_code, df = MLModule.processing.use_filter_method(df, filter_method)
                if error_code == ServerErrors.NO_ERROR:
                    error_code, df = MLModule.processing.use_balancing_method(df, balancing_method)
                    if error_code == ServerErrors.NO_ERROR:
                        error_code, best_estimator = MLModule.models.use_gscv(df, model)
                        if error_code == ServerErrors.NO_ERROR:
                            error_code, scores = MLModule.models.use_kfolds(df, best_estimator)

            os.remove("static/dataframes/" + session + ".csv")
        return error_code, scores
