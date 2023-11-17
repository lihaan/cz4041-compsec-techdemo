import csv


class Table:
    def __init__(self, data) -> None:
        self.data = data

    def query(self, query) -> dict:
        if query in self.data:
            output = self.data[query]
            return {"found": True, "data": output}

        return {"found": False, "data": None}


def import_data_into_db(path):
    with open(path, mode='r') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        data = {int(row[0]): {headers[i]: row[i] if i != 0 else int(row[i]) for i in range(len(headers))} for row in reader}

    table = Table(data)

    return table


def authenticate(username, password):
    return username == "smith" and password == "password"