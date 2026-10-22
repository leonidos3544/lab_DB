from minidb import MiniDB


def show(title, rows):
    print(f"\n{title}")
    for row in rows:
        print(" ", row)


db = MiniDB("data")

# 1) создать базу и таблицы (если их ещё нет)
if not db.tables:
    db.create_table("datasets", [("id", "INT"), ("name", "STRING"), ("task", "STRING"), ("size", "INT")], "id")
    db.create_table("models", [("id", "INT"), ("name", "STRING"), ("version", "STRING")], "id")
    db.create_table("experiments", [("id", "INT"), ("dataset_id", "INT"), ("model_id", "INT"),
                                    ("accuracy", "FLOAT"), ("status", "STRING")], "id")

    # 2) INSERT
    db.insert("datasets", {"id": 1, "name": "MNIST", "task": "classification", "size": 70000})
    db.insert("datasets", {"id": 2, "name": "CIFAR10", "task": "classification", "size": 60000})
    db.insert("models", {"id": 1, "name": "ResNet", "version": "1.0"})
    db.insert("models", {"id": 2, "name": "VGG", "version": "2.0"})
    db.insert("experiments", {"id": 1, "dataset_id": 1, "model_id": 1, "accuracy": 0.91, "status": "completed"})
    db.insert("experiments", {"id": 2, "dataset_id": 1, "model_id": 2, "accuracy": 0.88, "status": "completed"})
    db.insert("experiments", {"id": 3, "dataset_id": 2, "model_id": 1, "accuracy": 0.76, "status": "running"})
    print("База создана, данные добавлены")
else:
    print("База открыта, данные загружены из файлов")

# 3) SELECT всех записей и SELECT с условием
show("SELECT * FROM experiments", db.select("experiments"))
show("SELECT id, accuracy FROM experiments WHERE accuracy > 0.8",
     db.select("experiments", ["id", "accuracy"], ("accuracy", ">", 0.8)))

# 4) UPDATE и DELETE
db.update("experiments", {"status": "completed", "accuracy": 0.8}, ("id", "=", 3))
show("После UPDATE id=3", db.select("experiments"))
db.delete("experiments", ("id", "=", 2))
show("После DELETE id=2", db.select("experiments"))
