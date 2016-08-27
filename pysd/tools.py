import pysd
import pandas as pd


def static_test_matrix(mdl_file, matrix=None, excel_file=None):

    if matrix:
        pass
    elif excel_file:
        matrix = pd.read_excel('SIR_Extreme_Conditions.xlsx', index_col=[0, 1])
    else:
        raise ValueError('Must supply a test matrix or refer to an external file')

    model = pysd.read_vensim(mdl_file)
    py_mdl_file = model.py_model_file

    errors = []
    for index, row in matrix.iterrows():
        try:
            model = pysd.load(py_mdl_file)
            result = model.run(params=dict([index]),
                               return_columns=row.index.values,
                               return_timestamps=0).loc[0]

            for key, value in row.items():
                if value != '-' and result[key] != value:
                    errors.append('When %s = %s, %s is %s instead of %s' %
                                  (index[0], index[1], key, result[key], value))

        except Exception as e:
            errors.append('When %s = %s, %s' %
                          (index[0], index[1], e))

    try:
        assert errors == []
    except:
        raise AssertionError(errors)
