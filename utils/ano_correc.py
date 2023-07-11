from anonymizer.anonymity import local_aggregation, get_k
from anonymizer.diversity import _l_diversity

"""This is a corrected version of the anonymizer module.
Must be incorporated in the original repo and deleted from this folder."""


def all_local_aggregation(tab, k, variables, method, unknown=""):
    """
        retourne une table k-anonymisée par aggrégation locale

        tab: la table à anonymiser
        k: un entier est le k-anonymat recherché
        variables est une liste de variable de tab :
            on traitera les données dans cet ordre et
            la première variable sera celle dont on est le plus
            prêt à sacrifier l'aggrégation
        method : voir local_aggregation

    Remarque: si pour un groupe donné, plusieurs modalité ont moins de k
    éléments, on les remplace toutes par "dropped", on peut ainsi avoir un
    groupe avec dropped d'une taille supérieure à k.
    Si ensuite on a une modalité plus grande que k à l'intérieur du groupe
    hétéroclyte avec dropped, on peut afficher cette variable
    """
    assert isinstance(k, int)
    assert all([var in tab.columns for var in variables])
    assert all(tab[variables].dtypes == "object")

    if get_k(tab, variables) >= k:
        return tab

    variable_a_aggreger = variables[-1]
    if len(variables) == 1:
        new_serie = local_aggregation(tab[variable_a_aggreger], k, method, unknown)
        tab[variable_a_aggreger] = new_serie
        return tab

    if get_k(tab, variables[:-1]) < k:
        tab = all_local_aggregation(tab, k, variables[:-1], method, unknown)
    # on a une table k-anonymisée lorsqu'elle est restreinte aux
    # len(variables) - 1 premières variables

    # on applique l'aggrégation locale d'une variable par groupe
    grp = tab.groupby(variables[:-1], group_keys=False)
    new_serie = grp[variable_a_aggreger].apply(
        lambda x: local_aggregation(x, k, method, unknown)
    )
    tab[variable_a_aggreger] = new_serie

    assert get_k(tab, variables, unknown) >= k

    return tab


def get_diversities(df, groupby, column):
    """
    Return the diversities levels of a column in a dataframe.

    This implementation takes Nan values as distinct modalities.

    You should replace all invalid, unknown and false rows by
    the numpy nan type before using this function.

    :param df: A pandas dataframe
    :param column: The sensible data column
    :param groupby: The columns to group by
    :type df: pandas.core.frame.DataFrame
    :type column: str
    :type groupby: list
    :return: diversities for each group
    :rtype: pandas.core.frame.DataFrame

    :Example:

    >>> iris = pd.read_csv("tests/iris.csv")
    >>> diversities = anonymization.get_diversities(iris,
                                                   groupby=['Name'],
                                                   column='PetalLength')
    """
    res = df.copy()
    res = res.groupby(groupby, as_index=False)[column].apply(_l_diversity)
    return res


def get_l(df, groupby, column):
    """
    Return the l-diversity value as an integer.

    Calls the get_diversities and extract the minimum l-diversity level.

    :param df: The dataframe to get l from
    :param column: The sensible data column
    :param groupby: The columns to group by
    :type df: pandas.core.frame.DataFrame
    :type column: str
    :type groupby: list
    :return: l-diversity
    :rtype: int


    """
    return min(get_diversities(df, groupby, column)[column])


def less_diverse_groups(df, groupby, column):
    """
    Return the less diversegroups .
    """
    grp = df.groupby(groupby)
    diversity = grp[column].apply(_l_diversity)
    select = diversity[diversity == min(diversity)]
    results = []
    for group_index in select.index:
        results += [grp.get_group(group_index)]
    return results


def aggregate_and_diversify(tab, k, l, variables, method, unknown=""):
    assert isinstance(k, int)
    assert isinstance(l, int)
    assert all([var in tab.columns for var in variables])
    assert all(tab[variables].dtypes == "object")

    #

    return None
