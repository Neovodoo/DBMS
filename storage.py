import os
import shutil
from student import Student


class Storage:
    def __init__(self):
        self.db_file = ""
        self.current_id = 0

    def new_db(self, db_name):
        if os.path.exists(db_name):
            return False
        self.db_file = db_name
        return True

    def open_db(self, db_name):
        if not os.path.exists(db_name):
            return False
        self.db_file = db_name
        return True

    def clear_db(self):
        if not os.path.exists(self.db_file):
            return False
        open(self.db_file, "w").close()
        return True

    def delete_db(self):
        if not os.path.exists(self.db_file):
            return False
        os.remove(self.db_file)
        return False

    def copy_db(self, name):
        if not os.path.exists(self.db_file):
            return False
        shutil.copy(self.db_file, name)
        return True

    def new_record(self):
        if not self.db_file:
            return False
        with open(self.db_file, "a+") as file:
            file.write(str(Student(i=self.current_id + 1)))

    def edit_record(self, i, values):
        if not self.db_file:
            return False
        with open(self.db_file) as file:
            fields = []
            for line in file.readlines():
                item = [x.strip() for x in line.split(";")]
                if item[0] == i:
                    item[1:] = values
                fields.append(";".join(item))
        with open(self.db_file, "r+") as file:
            file.write("\n".join(fields))
        return True

    def delete_record(self, field, value):
        res = []
        with open(self.db_file) as file:
            for line in file.readlines():
                if not line.strip():
                    continue
                item = [x.strip() for x in line.split(";")]
                if (field.lower() == "id" and item[0].lower() != value.lower()) \
                    or (field.lower() == "name" and item[1].lower() != value.lower()) \
                    or (field.lower() == "was present" and item[2].lower() != value.lower()) \
                    or (field.lower() == "group" and item[3].lower() != value.lower()) \
                    or (field.lower() == "mark" and item[4].lower() != value.lower()):
                    res.append(";".join(item))
        with open(self.db_file, "w") as file:
            file.write("\n".join(res))

    def search_record(self, field, value):
        res = []
        with open(self.db_file) as file:
            for line in file.readlines():
                if not line.strip():
                    continue
                item = [x.strip() for x in line.split(";")]
                if (field.lower() == "id" and item[0].lower() == value.lower()) \
                    or (field.lower() == "name" and item[1].lower() == value.lower()) \
                    or (field.lower() == "was present" and item[2].lower() == value.lower()) \
                    or (field.lower() == "group" and item[3].lower() == value.lower()) \
                    or (field.lower() == "mark" and item[4].lower() == value.lower()):
                    res.append(Student(i=int(item[0]),
                                     name=item[1],
                                     was_present=item[2].lower() == "false",
                                     group=int(item[3]),
                                     mark=float(item[4])))
        return res

    def get_records(self):
        res = []
        if not os.path.exists(self.db_file):
            return res
        try:
            with open(self.db_file) as file:
                for line in file.readlines():
                    if not line.strip():
                        continue
                    token = [x.strip() for x in line.split(";")]
                    self.current_id = int(token[0])
                    res.append(Student(i=self.current_id,
                                     name=token[1],
                                     was_present=True if token[2].lower() == "true" else False,
                                     group=int(token[3]),
                                     mark=float(token[4])))
        except Exception as err:
            print(err)
        return res

