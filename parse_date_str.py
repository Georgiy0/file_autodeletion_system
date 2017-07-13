def parse_date_str(date_str, delimiter, y_idx, m_idx, d_idx):
    """
    Parses a string that contains a date in order to retrive
    a tuple with three integers corresponding to year, month and day:
    (Year, month, day)
    """
    month_name = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    split_date = date_str.split(delimiter)
    try:
        y = int(split_date[y_idx])
    except ValueError:
        # tries to handle the ValueError by deleting empty substrings
        # that might appear if there are double delimiters in the date string
        for i in range(0, len(split_date) - 1):
            if split_date[i] == '':
                split_date.pop(i)
        y = int(split_date[y_idx])
    try:
        m = int(split_date[m_idx])
    except ValueError:
        # tries to handle the ValueError by checking if the month_name
        # was given in the symbolic format.
        try:
            m = month_name[split_date[m_idx]]
        except KeyError:
            raise ValueError('Cannot parse month')
    d = int(split_date[d_idx])
    return (y, m, d)
