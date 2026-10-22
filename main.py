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
                                    ("accuracy", "FLOAT"), ("status", "STRING")], "id",
                    {"dataset_id": "datasets", "model_id": "models"})

    # 2) INSERT: 5 datasets, 5 models, 20 experiments
    datasets = [
        (1, "MNIST", "classification", 70000),
        (2, "CIFAR10", "classification", 60000),
        (3, "IMDB", "sentiment", 50000),
        (4, "COCO", "detection", 330000),
        (5, "BostonHousing", "regression", 506),
    ]
    for id_, name, task, size in datasets:
        db.insert("datasets", {"id": id_, "name": name, "task": task, "size": size})

    models = [
        (1, "ResNet", "1.0"),
        (2, "VGG", "2.0"),
        (3, "BERT", "1.1"),
        (4, "YOLO", "5.0"),
        (5, "LinearRegression", "1.0"),
    ]
    for id_, name, version in models:
        db.insert("models", {"id": id_, "name": name, "version": version})

    experiments = [
        (1, 1, 1, 0.91, "completed"),
        (2, 1, 2, 0.88, "completed"),
        (3, 2, 1, 0.76, "running"),
        (4, 2, 2, 0.81, "completed"),
        (5, 3, 3, 0.93, "completed"),
        (6, 3, 2, 0.70, "failed"),
        (7, 4, 4, 0.65, "running"),
        (8, 4, 1, 0.58, "completed"),
        (9, 5, 5, 0.72, "completed"),
        (10, 5, 3, 0.40, "failed"),
        (11, 1, 3, 0.95, "completed"),
        (12, 2, 3, 0.84, "running"),
        (13, 3, 1, 0.79, "completed"),
        (14, 4, 2, 0.61, "completed"),
        (15, 5, 1, 0.55, "failed"),
        (16, 1, 4, 0.89, "completed"),
        (17, 2, 4, 0.73, "running"),
        (18, 3, 4, 0.68, "completed"),
        (19, 4, 3, 0.71, "completed"),
        (20, 5, 2, 0.60, "running"),
    ]
    for id_, dataset_id, model_id, accuracy, status in experiments:
        db.insert("experiments", {"id": id_, "dataset_id": dataset_id, "model_id": model_id,
                                  "accuracy": accuracy, "status": status})
    print("База создана, данные добавлены")
else:
    print("База открыта, данные загружены из файлов")

# 3) SELECT всех записей и SELECT с условием
show("SELECT * FROM experiments", db.select("experiments"))
show("SELECT id, accuracy FROM experiments WHERE accuracy > 0.8",
     db.select("experiments", ["id", "accuracy"], ("accuracy", ">", 0.8)))

# 4) UPDATE и DELETE
db.update("experiments", {"status": "completed", "accuracy": 0.8}, ("id", "=", 3))
show("После UPDATE id=3", db.select("experiments", where=("id", "=", 3)))
db.delete("experiments", ("id", "=", 2))
show("После DELETE id=2", db.select("experiments", ["id"]))

# 5) ошибка при неверном FK
try:
    db.insert("experiments", {"id": 21, "dataset_id": 99, "model_id": 1, "accuracy": 0.5, "status": "running"})
except ValueError as e:
    print(f"\n{e}")
