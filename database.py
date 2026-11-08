
import sqlite3
from pathlib import Path
from kivy.app import App
from kivy.utils import platform

def get_db_path():
    """مسیر اختصاصی دیتابیس در اندروید و کامپیوتر"""

    if platform == "android":
        app = App.get_running_app()

        if app is None:
            raise RuntimeError("برنامه هنوز اجرا نشده است.")

        return Path(app.user_data_dir) / "debtbook.db"

    return Path(__file__).resolve().parent / "test_debtbook.db"


def connect(db_path):
    """ایجاد اتصال به پایگاه داده"""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(path)


def init_db(db_path):
    """ساخت جدول بدهکاران در صورت نیاز"""
    with connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS debtors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                debt REAL NOT NULL DEFAULT 0
            )
        """)


def get_all(db_path):
    """دریافت تمام بدهکاران"""
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT id, name, debt FROM debtors ORDER BY name"
        ).fetchall()

    return rows


def add_person(db_path, name, debt):
    """افزودن بدهکار جدید"""
    with connect(db_path) as conn:
        conn.execute(
            "INSERT INTO debtors (name, debt) VALUES (?, ?)",
            (name.strip(), debt)
        )


def update_person(db_path, person_id, new_name, new_debt):
    """ویرایش نام و مبلغ بدهی"""
    with connect(db_path) as conn:
        conn.execute(
            "UPDATE debtors SET name = ?, debt = ? WHERE id = ?",
            (new_name.strip(), new_debt, person_id)
        )


def record_payment(db_path, person_id, amount):
    """ثبت پرداخت و کاهش بدهی"""
    if amount <= 0:
        raise ValueError("مبلغ پرداخت باید بیشتر از صفر باشد.")

    with connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE debtors SET debt = debt - ? "
            "WHERE id = ? AND debt >= ?",
            (amount, person_id, amount)
        )

        if cursor.rowcount == 0:
            raise ValueError("شخص پیدا نشد یا مبلغ پرداخت بیشتر از بدهی است.")


def delete_person(db_path, person_id):
    """حذف بدهکار"""
    with connect(db_path) as conn:
        conn.execute(
            "DELETE FROM debtors WHERE id = ?",
            (person_id,)
        )


def get_person(db_path, person_id):
    """دریافت اطلاعات یک بدهکار"""
    with connect(db_path) as conn:
        return conn.execute(
            "SELECT id, name, debt FROM debtors WHERE id = ?",
            (person_id,)
        ).fetchone()


def get_total(db_path):
    """محاسبه مجموع بدهی‌ها"""
    with connect(db_path) as conn:
        result = conn.execute(
            "SELECT COALESCE(SUM(debt), 0) FROM debtors"
        ).fetchone()

    return result[0]
