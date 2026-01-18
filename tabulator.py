import prettytable


def tabulate(datax, width=25, pagination=False, result_perpage_on_pagination=25, dump = False):
    if len(datax)==0:
        datax = [{'NO DATA': '-'}]
    flag = False
    if pagination and len(datax) > result_perpage_on_pagination:
        data = datax[:result_perpage_on_pagination]
        datax = datax[result_perpage_on_pagination:]
        flag = True
    else:
        data = datax

    if isinstance(data, dict):
        data = [data]
    keys = list(data[0].keys())
    table = prettytable.PrettyTable()
    table.field_names = list(keys)

    for item in data:

        row = []
        for key in keys:
            value = item.get(key, None)
            if value is None:
                value = "-"
            str_val = ""

            if isinstance(value, list):
                str_val = ", ".join(map(str, value))
            else:
                str_val = str(value)

            if len(str_val) <= (len(key) + width):
                row.append(str_val)
            else:
                row.append(str_val[: len(key) + width - 3] + "...")

        table.add_row(row)

    table.align = "l"
    if dump:
        return table.get_string()
    else:
        print(table)

    if flag:
        try:
            input("Press Enter for Next Page --> ")
        except KeyboardInterrupt as k:
            print("Keyboard Interrupt")
            exit()
        tabulate(datax, width, pagination, result_perpage_on_pagination)
