import os

TYPES = {"INT": int, "STRING": str, "FLOAT": float}

OPS = {
    "=": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
}


class MiniDB:
    def __init__(self, path):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.tables = {}
        for f in os.listdir(path):
            if f.endswith(".schema"):
                self._load_schema(f[:-len(".schema")])

    def _file(self, table, ext):
        return os.path.join(self.path, table + ext)

    def _load_schema(self, table):
        columns = []
        pk = None
        with open(self._file(table, ".schema"), encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                columns.append((parts[0], parts[1]))
                if len(parts) > 2 and parts[2] == "PK":
                    pk = parts[0]
        self.tables[table] = {"columns": columns, "pk": pk}

    def create_table(self, table, columns, primary_key):
        # columns: [("id", "INT"), ("name", "STRING"), ...]
        with open(self._file(table, ".schema"), "w", encoding="utf-8") as f:
            for name, type_ in columns:
                f.write(f"{name} {type_}" + (" PK" if name == primary_key else "") + "\n")
        open(self._file(table, ".tbl"), "w", encoding="utf-8").close()
        self.tables[table] = {"columns": columns, "pk": primary_key}

    def _read(self, table):
        columns = self.tables[table]["columns"]
        rows = []
        with open(self._file(table, ".tbl"), encoding="utf-8") as f:
            for line in f:
                values = line.rstrip("\n").split("\t")
                rows.append({name: TYPES[type_](v) for (name, type_), v in zip(columns, values)})
        return rows

    def _write(self, table, rows):
        with open(self._file(table, ".tbl"), "w", encoding="utf-8") as f:
            for row in rows:
                f.write(self._line(table, row))

    def _line(self, table, row):
        return "\t".join(str(row[name]) for name, _ in self.tables[table]["columns"]) + "\n"

    @staticmethod
    def _match(row, where):
        if where is None:
            return True
        column, op, value = where
        return OPS[op](row[column], value)

    def insert(self, table, row):
        with open(self._file(table, ".tbl"), "a", encoding="utf-8") as f:
            f.write(self._line(table, row))

    def select(self, table, columns=None, where=None):
        result = []
        for row in self._read(table):
            if self._match(row, where):
                result.append({c: row[c] for c in columns} if columns else row)
        return result

    def update(self, table, values, where=None):
        rows = self._read(table)
        count = 0
        for row in rows:
            if self._match(row, where):
                row.update(values)
                count += 1
        self._write(table, rows)
        return count

    def delete(self, table, where=None):
        rows = self._read(table)
        kept = [row for row in rows if not self._match(row, where)]
        self._write(table, kept)
        return len(rows) - len(kept)
