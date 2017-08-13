from pandas import read_table


def read_g2p(g2p_file_path):
    """
    Read .g2p file.
    Arguments:
        g2p_file_path (str): .g2p file path
    Returns:
        dict: {'header': .g2p file header (list),
            'table': .g2p file table (DataFrame)}
    """

    # Read header
    with open(g2p_file_path) as f:
        header = [l.strip() for l in f if l.startswith('#')]

    return {'header': header, 'table': read_table(g2p_file_path, comment='#')}


def write_g2p(g2p, file_path):
    """
    Write .g2p file.
    Arguments:
        g2p (dict): {'header': .g2p file header (list),
            'table': .g2p file table (DataFrame)}
        file_path (str): .g2p file path
    Returns:
        None
    """

    with open(file_path, 'w') as f:

        # Write header
        header = g2p['header']
        if len(header):
            f.write('\n'.join(header) + '\n')

        # Write table
        g2p['table'].to_csv(f, sep='\t', index=None)
