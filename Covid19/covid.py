import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DATASET_PATH = 'dataset.xlsx'


def load_dataset(dataset_path=DATASET_PATH):
    data = pd.read_excel(dataset_path)
    df = data.copy()
    return df


def general_info(df):
    displayHead(df, True, True)
    shapeOfDF(df)
    typeOfDFValues(df)


def displayHead(df, every_column=False, every_row=False):
    if every_column:
        pd.set_option('display.max_column', 111)

    if every_row:
        pd.set_option('display.max_row', 111)

    # print(df.head())
    return df.head()


def shapeOfDF(df):
    print("Shape is : {}".format(df.shape))
    return df.shape


def typeOfDFValues(df):
    print(df.dtypes.value_counts())
    return df.dtypes.value_counts()


def checkNan(df):
    # print(df.isna())
    return df.isna()


def constructHeatMap(data):
    plt.figure(figsize=(20, 10))
    sns.heatmap(data, cbar=False)
    plt.show()


def missing_values_percentage(df):
    missing_values = (checkNan(df).sum() / df.shape[0]).sort_values(ascending=True)
    # print(len(missing_values[missing_values > 0.9])  # Ex : 0.98 = 98% of missing values
    #     / len(missing_values[missing_values > 0.0]))  # Give the percentage of missing values > 90% compared to all
    # the missing values : 68 % (more than half the variables are > 90% of NaN)
    return missing_values


def missing_rate(df):
    return df.isna().sum() / df.shape[0]


def keep_values(df, percentage_to_keep=0.9):
    return df[df.columns[df.isna().sum() / df.shape[0] < percentage_to_keep]]  # Keep the values where there are
    # less than 90% of missing values


def dropColumn(df, colonName):
    return df.drop(colonName, axis=1)


def analyse_target(df, target, normalized=False):
    return df[target].value_counts(normalize=normalized)


def draw_histograms(df, data_type='float'):
    for col in df.select_dtypes(data_type):
        if data_type == 'float' or data_type == 'int':
            sns.distplot(df[col])

        if data_type == 'object':
            plt.figure()
            df[col].value_counts().plot.pie()

        plt.show()


def description_object(df, target):
    return df[target].unique()


def qual_to_quan(df, target, criteria1):
    return df[df[target] == criteria1]


def rate_borned(df, missing_rate, rate_inf, rate_sup):
    return df.columns[(missing_rate < rate_sup) & (missing_rate > rate_inf)]


def display_relations(column_name, relation):
    for col in column_name:
        plt.figure()
        for rel, lab in relation:
            sns.distplot(rel[col], label=lab)
        plt.legend()
    plt.show()


if __name__ == "__main__":
    df = load_dataset(dataset_path=DATASET_PATH)
    # general_info(df)
    displayHead(df, True, True)
    NaN = checkNan(df)
    # constructHeatMap(NaN)
    missing_values_percentage(df)
    df = keep_values(df, percentage_to_keep=0.9)
    df = dropColumn(df, 'Patient ID')
    # analyse_target(df, "SARS-Cov-2 exam result", True)
    # draw_histograms(df, 'object')


    """
    Target/Variables relation :
    """
    ### Positive and Negative collections
    positive_df = qual_to_quan(df, "SARS-Cov-2 exam result", 'positive')
    negative_df = qual_to_quan(df, "SARS-Cov-2 exam result", 'negative')

    ### Blood and Viral collections
    MR = missing_rate(df)
    blood_columns = rate_borned(df, MR, 0.88, 0.9)
    viral_columns = rate_borned(df, MR, 0.75, 0.88)

    relation = [(positive_df, 'positive'), (negative_df, 'negative')]
    display_relations(blood_columns, relation)




