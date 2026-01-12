from .storage import Storage

class Engine:
    def __init__(self):
        self.storage = Storage()

    def execute(self, ast):
        t = ast["type"]

        if t == "CREATE":
            self.storage.create_table(
                ast["table"],
                {
                    "columns": ast["columns"],
                    "indexes": ast["indexes"]
                }
            )
            return "OK"

        if t == "INSERT":
            schema = self.storage.load_schema(ast["table"])
            cols = list(schema["columns"].keys())
            row = dict(zip(cols, ast["values"]))
            self.storage.insert(ast["table"], row)
            return "OK"

        if t == "SELECT_ALL":
            return self.storage.read_all(ast["table"])

        if t == "SELECT_WHERE":
            return self.storage.read_where(
                ast["table"],
                ast["column"],
                ast["value"]
            )

        if t == "UPDATE":
            count = self.storage.update(
                ast["table"],
                ast["set"][0],
                ast["set"][1],
                ast["where"][0],
                ast["where"][1]
            )
            return f"{count} row(s) updated"

        if t == "DELETE":
            count = self.storage.delete(
                ast["table"],
                ast["where"][0],
                ast["where"][1]
            )
            return f"{count} row(s) deleted"

        if t == "JOIN":
            return self._join(ast)

    def _join(self, ast):
        left_rows = self.storage.read_all(ast["left_table"])
        right_rows = self.storage.read_all(ast["right_table"])

        # create hash map on right table
        hash_map = {}
        for r in right_rows:
            hash_map.setdefault(r[ast["right_col"]], []).append(r)

        results = []
        matched_right_keys = set()

        # iterate left table
        for l in left_rows:
            key = l.get(ast["left_col"])
            matches = hash_map.get(key)

            if matches:
                for r in matches:
                    results.append({**l, **r})
                matched_right_keys.add(key)
            else:
                if ast["join_type"] in ("LEFT", "FULL"):
                    results.append(l)

        # handle RIGHT / FULL join unmatched rows
        if ast["join_type"] in ("RIGHT", "FULL"):
            for r in right_rows:
                key = r.get(ast["right_col"])
                if key not in matched_right_keys:
                    if ast["join_type"] == "RIGHT":
                        results.append(r)
                    elif ast["join_type"] == "FULL":
                        # add r + empty left fields
                        left_schema = self.storage.load_schema(ast["left_table"])
                        empty_left = {col: None for col in left_schema["columns"].keys()}
                        results.append({**empty_left, **r})

        return results
