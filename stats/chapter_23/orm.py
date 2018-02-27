# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

from collections import defaultdict


class Table:
    def __init__(self, columns):
        self.columns = columns
        self.rows = []

    def __repr__(self):
        """pretty representation of the table: columns then rows"""
        return str(self.columns) + "\n" + "\n".join(map(str, self.rows))

    def insert(self, row_values):
        if len(row_values) != len(self.columns):
            raise TypeError("wrong number of elements")
        row_dict = dict(zip(self.columns, row_values))
        self.rows.append(row_dict)

    def update(self, updates, predicate):
        for row in self.rows:
            if predicate(row):
                for column, new_value in updates.items():
                    row[column] = new_value

    def delete(self, predicate=lambda row: True):
        """delete all rows matching predicate
        or all rows if no predicate supplied"""
        self.rows = [row for row in self.rows if not(predicate(row))]

    def select(self, keep_columns=None, additional_columns=None):

        if keep_columns is None:         # if no columns specified,
            keep_columns = self.columns  # return all columns

        if additional_columns is None:
            additional_columns = {}

        # new table for results
        result_table = Table(keep_columns + list(additional_columns.keys()))

        for row in self.rows:
            new_row = [row[column] for column in keep_columns]
            for column_name, calculation in additional_columns.items():
                new_row.append(calculation(row))
            result_table.insert(new_row)

        return result_table

    def where(self, predicate=lambda row: True):
        """return only the rows that satisfy the supplied predicate"""
        where_table = Table(self.columns)
        where_table.rows = list(filter(predicate, self.rows))
        return where_table

    def limit(self, num_rows=None):
        """return only the first num_rows rows"""
        limit_table = Table(self.columns)
        limit_table.rows = (self.rows[:num_rows]
                            if num_rows is not None
                            else self.rows)
        return limit_table

    def group_by(self, group_by_columns, aggregates, having=None):

        grouped_rows = defaultdict(list)

        # populate groups
        for row in self.rows:
            key = tuple(row[column] for column in group_by_columns)
            grouped_rows[key].append(row)

        result_table = Table(group_by_columns + list(aggregates.keys()))

        for key, rows in grouped_rows.items():
            if having is None or having(rows):
                new_row = list(key)
                for aggregate_name, aggregate_fn in aggregates.items():
                    new_row.append(aggregate_fn(rows))
                result_table.insert(new_row)

        return result_table

    def order_by(self, order):
        new_table = self.select()       # make a copy
        new_table.rows.sort(key=order)
        return new_table

    def join(self, other_table, left_join=False):

        join_on_columns = [c for c in self.columns           # columns in
                           if c in other_table.columns]      # both tables

        additional_columns = [c for c in other_table.columns # columns only
                              if c not in join_on_columns]   # in right table

        # all columns from left table + additional_columns from right table
        join_table = Table(self.columns + additional_columns)

        for row in self.rows:
            def is_join(other_row):
                return all(other_row[c] == row[c] for c in join_on_columns)

            other_rows = other_table.where(is_join).rows

            # each other row that matches this one produces a result row
            for other_row in other_rows:
                join_table.insert([row[c] for c in self.columns] +
                                  [other_row[c] for c in additional_columns])

            # if no rows match and it's a left join, output with Nones
            if left_join and not other_rows:
                join_table.insert([row[c] for c in self.columns] +
                                  [None for c in additional_columns])

        return join_table

if __name__ == "__main__":
    users = Table(["user_id", "name", "num_friends"])
    users.insert([0, "Hero", 0])
    users.insert([1, "Dunn", 2])
    users.insert([2, "Sue", 3])
    users.insert([3, "Chi", 3])
    users.insert([4, "Thor", 3])
    users.insert([5, "Clive", 2])
    users.insert([6, "Hicks", 3])
    users.insert([7, "Devin", 2])
    users.insert([8, "Kate", 2])
    users.insert([9, "Klein", 3])
    users.insert([10, "Jen", 1])
    print(users)

    users.update({'num_friends': 3},  # set num_friends = 3
                 lambda row: row['user_id'] == 1)  # in rows where user_id == 1

    print(users)

    # users.delete(lambda row: row["user_id"] == 1)  # deletes rows with user_id == 1
    # print(users)
    # users.delete()  # deletes every row
    # print(users)

    print("SELECT * FROM users;")
    print(users.select())
    print("SELECT * FROM users LIMIT 2")
    print(users.limit(2))
    print("SELECT user_id FROM users;")
    print(users.select(keep_columns=["user_id"]))

    print("SELECT user_id FROM users WHERE name = 'Dunn'")
    print(users.where(lambda row: row["name"] == "Dunn")
          .select(keep_columns=["user_id"]))

    print("SELECT LENGTH(name) AS name_length FROM users;")
    name_length = lambda row: len(row["name"])

    print(users.select(keep_columns=[],
                       additional_columns={"name_length": name_length}))


    def min_user_id(rows): return min(row["user_id"] for row in rows)


    stats_by_length = users \
        .select(additional_columns={"name_length": name_length}) \
        .group_by(group_by_columns=["name_length"],
                  aggregates={"min_user_id": min_user_id,
                              "num_users": len})
    print(stats_by_length)
