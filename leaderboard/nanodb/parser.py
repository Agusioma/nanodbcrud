def parse(sql: str):
    sql = sql.strip().rstrip(";")
    tokens = sql.split()
    cmd = tokens[0].upper()

    if cmd == "CREATE":
        return _parse_create(sql)

    if cmd == "INSERT":
        return {
            "type": "INSERT",
            "table": tokens[2],
            "values": _parse_values(sql)
        }

    if cmd == "SELECT":
        return _parse_select(tokens)

    if cmd == "UPDATE":
        return _parse_update(sql, tokens)

    if cmd == "DELETE":
        return _parse_delete(tokens)

    raise ValueError("Unsupported SQL command")



def _parse_create(sql):
    table = sql.split()[2]
    cols = sql[sql.find("(")+1:sql.find(")")].split(",")

    columns = {}
    indexes = []

    for col in cols:
        parts = col.strip().split()
        name = parts[0]
        dtype = parts[1]
        columns[name] = dtype

        if "PRIMARY" in parts or "UNIQUE" in parts:
            indexes.append(name)

    return {
        "type": "CREATE",
        "table": table,
        "columns": columns,
        "indexes": indexes
    }


def _parse_select(tokens):
    if "JOIN" in tokens:
        return _parse_join(tokens)

    table = tokens[3]

    if "WHERE" in tokens:
        idx = tokens.index("WHERE")
        col = tokens[idx + 1]
        val = tokens[idx + 3].strip("'")
        return {
            "type": "SELECT_WHERE",
            "table": table,
            "column": col,
            "value": val
        }

    return {
        "type": "SELECT_ALL",
        "table": table
    }

def _parse_update(sql, tokens):
    table = tokens[1]

    set_part = sql[sql.upper().find("SET") + 3: sql.upper().find("WHERE")]
    where_part = sql[sql.upper().find("WHERE") + 5:]

    col, val = [x.strip() for x in set_part.split("=")]
    w_col, w_val = [x.strip() for x in where_part.split("=")]

    return {
        "type": "UPDATE",
        "table": table,
        "set": (col, val.strip("'")),
        "where": (w_col, w_val.strip("'"))
    }

def _parse_delete(tokens):
    table = tokens[2]
    col = tokens[4]
    val = tokens[6].strip("'")

    return {
        "type": "DELETE",
        "table": table,
        "where": (col, val)
    }

def _parse_join(tokens):
    join_idx = tokens.index("JOIN")
    join_type = tokens[join_idx - 1].upper()

    if tokens[join_idx - 1].upper() == "OUTER":
        t1 = tokens[join_idx - 3]
        join_type = "FULL"
    else:
        t1 = tokens[join_idx - 2]

    t2 = tokens[join_idx + 1]


    on = tokens[tokens.index("ON") + 1:]
    left_col = on[0]
    right_col = on[2]

    return {
        "type": "JOIN",
        "join_type": join_type,
        "left_table": t1,
        "right_table": t2,
        "left_col": left_col,
        "right_col": right_col
    }

def _parse_values(sql):
    vals = sql[sql.find("(")+1:sql.find(")")]
    return [v.strip().strip("'") for v in vals.split(",")]