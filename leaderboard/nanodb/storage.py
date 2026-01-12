import os
import json

DB_ROOT = "db"


class Storage:
    def __init__(self):
        os.makedirs(DB_ROOT, exist_ok=True)

    def table_path(self, table):
        return os.path.join(DB_ROOT, table)

    def create_table(self, name, schema):
        path = self.table_path(name)
        os.makedirs(path, exist_ok=True)
        os.makedirs(os.path.join(path, "indexes"), exist_ok=True)

        with open(os.path.join(path, "schema.json"), "w") as f:
            json.dump(schema, f)

        open(os.path.join(path, "data.jsonl"), "a").close()

        for col in schema.get("indexes", []):
            self._write_index(name, col, {})

    def load_schema(self, table):
        with open(os.path.join(self.table_path(table), "schema.json")) as f:
            return json.load(f)

    def insert(self, table, row):
        schema = self.load_schema(table)

        for col in schema.get("indexes", []):
            idx = self._read_index(table, col)
            if row[col] in idx:
                raise ValueError(f"Duplicate value for {col}")

        path = os.path.join(self.table_path(table), "data.jsonl")
        with open(path, "a") as f:
            pos = f.tell()
            f.write(json.dumps(row) + "\n")

        for col in schema.get("indexes", []):
            idx = self._read_index(table, col)
            idx[row[col]] = pos
            self._write_index(table, col, idx)

    def read_all(self, table):
        path = os.path.join(self.table_path(table), "data.jsonl")
        with open(path) as f:
            return [json.loads(line) for line in f if line.strip()]

    def read_where(self, table, column, value):
        schema = self.load_schema(table)

        if column in schema.get("indexes", []):
            idx = self._read_index(table, column)
            if value not in idx:
                return []
            with open(os.path.join(self.table_path(table), "data.jsonl")) as f:
                f.seek(idx[value])
                return [json.loads(f.readline())]

        return [
            row for row in self.read_all(table)
            if row.get(column) == value
        ]

    def _index_path(self, table, column):
        return os.path.join(self.table_path(table), "indexes", f"{column}.idx")

    def _read_index(self, table, column):
        path = self._index_path(table, column)
        if not os.path.exists(path):
            return {}
        with open(path) as f:
            return json.load(f)

    def _write_index(self, table, column, data):
        with open(self._index_path(table, column), "w") as f:
            json.dump(data, f)

    def update(self, table, set_col, set_val, where_col, where_val):
        schema = self.load_schema(table)
        rows = self.read_all(table)

        updated = False
        for row in rows:
            if row.get(where_col) == where_val:
                row[set_col] = set_val
                updated = True

        if not updated:
            return 0

        self._rewrite_table(table, rows, schema)
        return 1

    def delete(self, table, where_col, where_val):
        schema = self.load_schema(table)
        rows = self.read_all(table)

        new_rows = [
            r for r in rows if r.get(where_col) != where_val
        ]

        deleted = len(rows) - len(new_rows)
        if deleted == 0:
            return 0

        self._rewrite_table(table, new_rows, schema)
        return deleted

    def _rewrite_table(self, table, rows, schema):
        path = self.table_path(table)

        data_path = os.path.join(path, "data.jsonl")
        #index_path = os.path.join(path, "indexes")

        open(data_path, "w").close()
        for col in schema.get("indexes", []):
            self._write_index(table, col, {})

        for row in rows:
            self.insert(table, row)

