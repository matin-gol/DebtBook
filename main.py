
from pathlib import Path
import sqlite3
from kivy.utils import platform
from kivy.uix.textinput import TextInput

import arabic_reshaper
from bidi.algorithm import get_display

from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

from database import (
    get_db_path,
    add_person,
    get_all,
    get_total,
    init_db,
    record_payment,
    update_person,
    delete_person
)
from kivy.uix.spinner import Spinner, SpinnerOption

# مسیر فایل‌ها
BASE_DIR = Path(__file__).resolve().parent
FONT_PATH = BASE_DIR / "fonts" / "Vazirmatn.ttf"


# ثبت فونت فارسی
LabelBase.register(
    name="Vazirmatn",
    fn_regular=str(FONT_PATH)
)


# اصلاح متن فارسی
def persian_text(text):
    return get_display(
        arabic_reshaper.reshape(str(text))
    )


class PersianTextInput(TextInput):
    """ورودی فارسی با نمایش حروف متصل"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.raw_text = ""

        self.font_name = "Vazirmatn"
        self.halign = "right"
        self.multiline = False

    def insert_text(self, substring, from_undo=False):
        if from_undo:
            return

        self.raw_text += substring

        # نمایش متن اصلاح‌شده، بدون تغییر متن اصلی
        self.text = persian_text(self.raw_text)

        self.cursor = (len(self.text), 0)

    def do_backspace(self, from_undo=False, mode="bkspc"):
        if not self.raw_text:
            return

        self.raw_text = self.raw_text[:-1]

        self.text = persian_text(self.raw_text)

        self.cursor = (len(self.text), 0)

class PersianSpinnerOption(SpinnerOption):

    font_name = "Vazirmatn"
    font_size = dp(16)
    halign = "right"

class DebtBookDesign(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"

        # اعمال فونت وزیران به سبک‌های KivyMD
        for style, values in self.theme_cls.font_styles.items():
            self.theme_cls.font_styles[style] = [
                "Vazirmatn",
                *values[1:]
            ]

        # اتصال به دیتابیس
        # تعیین مسیر اختصاصی دیتابیس
        self.db_path = str(get_db_path())

        # اتصال به دیتابیس
        init_db(self.db_path)

        debtors = get_all(self.db_path)
        total_debt = get_total(self.db_path)
        debtor_count = len(debtors)

        if platform not in ("android", "ios"):
            Window.size = (390, 780)

        main = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(18)
        )
        main.size_hint_y = None
        main.bind(minimum_height=main.setter("height"))

        # عنوان برنامه
        title = MDLabel(
            text=persian_text("دفترچه بدهی"),
            font_name="Vazirmatn",
            font_size="27sp",
            bold=True,
            halign="right",
            adaptive_height=True
        )

        subtitle = MDLabel(
            text=persian_text("مدیریت آسان حساب و کتاب"),
            font_name="Vazirmatn",
            font_size="14sp",
            halign="right",
            theme_text_color="Secondary",
            adaptive_height=True
        )

        main.add_widget(title)
        main.add_widget(subtitle)

        # کارت مجموع بدهی
        debt_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            radius=[20, 20, 20, 20],
            size_hint_y=None,
            height=dp(160),
            md_bg_color=(0.02, 0.35, 0.32, 1)
        )

        debt_title = MDLabel(
            text=persian_text("مجموع بدهی‌ها"),
            font_name="Vazirmatn",
            font_size="17sp",
            halign="right"
        )

        debt_amount = MDLabel(
            text=persian_text(f"{total_debt:,.0f} تومان"),
            font_name="Vazirmatn",
            font_size="28sp",
            bold=True,
            halign="right"
        )
        self.debt_amount_label = debt_amount

        debt_card.add_widget(debt_title)
        debt_card.add_widget(debt_amount)

        main.add_widget(debt_card)

        # کارت تعداد بدهکاران
        count_card = MDCard(
            orientation="vertical",
            padding=dp(18),
            radius=[18, 18, 18, 18],
            size_hint_y=None,
            height=dp(90)
        )

        count_label = MDLabel(
            text=persian_text(
                f"تعداد بدهکاران: {debtor_count} نفر"
            ),
            font_name="Vazirmatn",
            font_size="18sp",
            halign="right"
        )
        self.count_label = count_label

        count_card.add_widget(count_label)
        main.add_widget(count_card)

        # عنوان عملیات
        operations_title = MDLabel(
            text=persian_text("عملیات"),
            font_name="Vazirmatn",
            font_size="20sp",
            bold=True,
            halign="right",
            adaptive_height=True
        )

        main.add_widget(operations_title)

        # دکمه‌های عملیات
        buttons = [
            "افزودن بدهکار",
            "مشاهده بدهکاران",
            "ثبت پرداخت",
            "ویرایش اطلاعات",
            "حذف بدهکار"
        ]

        for button_text in buttons:

            button = MDRaisedButton(
                text=persian_text(button_text),
                font_name="Vazirmatn",
                font_size="16sp",
                size_hint_x=1,
                size_hint_y=None,
                height=dp(52)
            )

            # اتصال دکمه مشاهده بدهکاران
            if button_text == "مشاهده بدهکاران":
                button.bind(on_release=self.show_debtors)

            elif button_text == "افزودن بدهکار":
                button.bind(on_release=self.add_debtor)

            elif button_text == "ثبت پرداخت":
                button.bind(on_release=self.record_payment_dialog)

            elif button_text == "ویرایش اطلاعات":
                button.bind(on_release=self.edit_debtor)

            elif button_text == "حذف بدهکار":
                button.bind(on_release=self.delete_debtor)

            main.add_widget(button)

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )
        scroll.add_widget(main)

        return scroll

    # ---------------------------------
    # نمایش بدهکاران
    # ---------------------------------

    def show_debtors(self, instance):

        # دریافت اطلاعات از دیتابیس
        debtors = get_all(self.db_path)

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        scroll = ScrollView()

        debtor_list = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None
        )

        debtor_list.bind(
            minimum_height=debtor_list.setter("height")
        )

        if not debtors:

            empty_label = MDLabel(
                text=persian_text(
                    "هنوز بدهکاری ثبت نشده است."
                ),
                font_name="Vazirmatn",
                font_size="18sp",
                halign="center",
                size_hint_y=None,
                height=dp(60)
            )

            debtor_list.add_widget(empty_label)

        else:

            for person_id, name, debt in debtors:

                item = MDCard(
                    padding=dp(15),
                    size_hint_y=None,
                    height=dp(70),
                    radius=[12, 12, 12, 12]
                )

                debtor_info = MDLabel(
                    text=persian_text(
                        f"{name} - {debt:,.0f} تومان"
                    ),
                    font_name="Vazirmatn",
                    font_size="16sp",
                    halign="right",
                    valign="middle"
                )

                item.add_widget(debtor_info)
                debtor_list.add_widget(item)

        scroll.add_widget(debtor_list)
        content.add_widget(scroll)

        # دکمه بستن
        close_button = MDRaisedButton(
            text=persian_text("بستن"),
            font_name="Vazirmatn",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(45)
        )

        content.add_widget(close_button)

        popup = Popup(
            title=persian_text("فهرست بدهکاران"),
            title_font="Vazirmatn",
            content=content,
            size_hint=(0.9, 0.8)
        )

        close_button.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # ---------------------------------
    # افزودن بدهکار
    # ---------------------------------

    def add_debtor(self, instance):

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(15)
        )

        # عنوان فرم
        title = MDLabel(
            text=persian_text("اطلاعات بدهکار جدید"),
            font_name="Vazirmatn",
            font_size="19sp",
            bold=True,
            halign="right",
            adaptive_height=True
        )

        # فیلد نام
        name_input = PersianTextInput(
            hint_text=persian_text("نام و نام خانوادگی"),
            font_size=dp(17),
            size_hint_y=None,
            height=dp(55),
            padding=[dp(12), dp(15)],
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.8, 0.7, 1)
        )

        # فیلد مبلغ بدهی
        # فیلد مبلغ بدهی
        debt_input = TextInput(
            hint_text=persian_text("مبلغ بدهی به تومان"),
            font_name="Vazirmatn",
            font_size=dp(17),
            multiline=False,
            halign="right",
            input_filter="int",
            size_hint_y=None,
            height=dp(55),
            padding=[dp(12), dp(15)],

            # هماهنگ‌سازی رنگ با فیلد نام
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.8, 0.7, 1),
            background_normal="",
            background_active=""
        )

        # دکمه ذخیره
        save_button = MDRaisedButton(
            text=persian_text("ذخیره بدهکار"),
            font_name="Vazirmatn",
            font_size="16sp",
            size_hint_x=1,
            height=dp(50)
        )

        content.add_widget(title)
        content.add_widget(name_input)
        content.add_widget(debt_input)
        content.add_widget(save_button)

        popup = Popup(
            title=persian_text("افزودن بدهکار"),
            title_font="Vazirmatn",
            content=content,
            size_hint=(0.9, 0.5)
        )

        def save_debtor(instance):

            name = name_input.raw_text.strip()
            debt_text = debt_input.text.strip()

            # بررسی خالی نبودن فیلدها
            if not name or not debt_text:
                self.show_message(
                    "لطفاً نام و مبلغ بدهی را وارد کنید."
                )
                return

            try:

                debt = int(debt_text)

                if debt <= 0:
                    self.show_message(
                        "مبلغ بدهی باید بیشتر از صفر باشد."
                    )
                    return

                # ذخیره در دیتابیس
                add_person(self.db_path, name, debt)

                # به‌روزرسانی آمار داشبورد
                self.refresh_dashboard()

                popup.dismiss()

                self.show_message(
                    "بدهکار با موفقیت ثبت شد."
                )

            except sqlite3.IntegrityError:

                self.show_message(
                    "این نام قبلاً در دفترچه ثبت شده است."
                )

            except ValueError:

                self.show_message(
                    "مبلغ واردشده معتبر نیست."
                )

            except sqlite3.Error:

                self.show_message(
                    "خطا در ذخیره اطلاعات رخ داد."
                )

        save_button.bind(
            on_release=save_debtor
        )

        popup.open()
    # ---------------------------------
    # ثبت پرداخت بدهکار
    # ---------------------------------

    def record_payment_dialog(self, instance):

        # دریافت فهرست بدهکاران
        debtors = get_all(self.db_path)

        if not debtors:
            self.show_message("هنوز هیچ بدهکاری ثبت نشده است.")
            return

        # ساخت محتوای پنجره
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(15)
        )

        # عنوان
        title = MDLabel(
            text=persian_text("ثبت پرداخت بدهکار"),
            font_name="Vazirmatn",
            font_size="19sp",
            bold=True,
            halign="right",
            adaptive_height=True
        )

        # ساخت فهرست انتخاب بدهکار
        debtor_options = {}

        for person_id, name, debt in debtors:

            display_name = persian_text(
                f"{name} - {debt:,.0f} تومان"
            )

            debtor_options[display_name] = person_id

        debtor_spinner = Spinner(
            text=persian_text("انتخاب بدهکار"),
            values=list(debtor_options.keys()),
            option_cls="PersianSpinnerOption",
            font_name="Vazirmatn",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(55)
        )

        # فیلد مبلغ پرداختی
        payment_input = TextInput(
            hint_text=persian_text("مبلغ پرداختی به تومان"),
            font_name="Vazirmatn",
            font_size=dp(17),
            multiline=False,
            halign="right",
            input_filter="int",
            size_hint_y=None,
            height=dp(55),
            padding=[dp(12), dp(15)],
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.8, 0.7, 1),
            background_normal="",
            background_active=""
        )

        # دکمه ثبت
        save_button = MDRaisedButton(
            text=persian_text("ثبت پرداخت"),
            font_name="Vazirmatn",
            font_size="16sp",
            size_hint_x=1,
            height=dp(50)
        )

        content.add_widget(title)
        content.add_widget(debtor_spinner)
        content.add_widget(payment_input)
        content.add_widget(save_button)

        # ساخت پنجره
        popup = Popup(
            title=persian_text("ثبت پرداخت"),
            title_font="Vazirmatn",
            content=content,
            size_hint=(0.9, 0.5)
        )

        # عملیات ذخیره پرداخت
        def save_payment(instance):

            selected_name = debtor_spinner.text
            payment_text = payment_input.text.strip()

            # بررسی انتخاب بدهکار
            if selected_name not in debtor_options:
                self.show_message("لطفاً یک بدهکار انتخاب کنید.")
                return

            # بررسی مبلغ
            if not payment_text:
                self.show_message("لطفاً مبلغ پرداختی را وارد کنید.")
                return

            try:

                person_id = debtor_options[selected_name]
                amount = int(payment_text)

                if amount <= 0:
                    self.show_message(
                        "مبلغ پرداختی باید بیشتر از صفر باشد."
                    )
                    return

                # ثبت پرداخت در دیتابیس
                record_payment(self.db_path, person_id, amount)

                # به‌روزرسانی داشبورد
                self.refresh_dashboard()

                popup.dismiss()

                self.show_message(
                    "پرداخت با موفقیت ثبت شد."
                )

            except ValueError as error:

                self.show_message(str(error))

            except sqlite3.Error:

                self.show_message(
                    "خطا در ثبت پرداخت رخ داد."
                )

        save_button.bind(on_release=save_payment)

        popup.open()
    # ---------------------------------
    # ویرایش اطلاعات بدهکار
    # ---------------------------------

    def edit_debtor(self, instance):

        debtors = get_all(self.db_path)

        if not debtors:
            self.show_message("هنوز هیچ بدهکاری ثبت نشده است.")
            return

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(13)
        )

        # عنوان فرم
        title = MDLabel(
            text=persian_text("ویرایش اطلاعات بدهکار"),
            font_name="Vazirmatn",
            font_size="19sp",
            bold=True,
            halign="right",
            adaptive_height=True
        )

        # فهرست بدهکاران
        debtor_options = {}

        for person_id, name, debt in debtors:

            display_name = persian_text(
                f"{name} - {debt:,.0f} تومان"
            )

            debtor_options[display_name] = (
                person_id, name, debt
            )

        debtor_spinner = Spinner(
            text=persian_text("انتخاب بدهکار"),
            values=list(debtor_options.keys()),
            option_cls="PersianSpinnerOption",
            font_name="Vazirmatn",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(55)
        )

        # فیلد نام
        name_input = PersianTextInput(
            hint_text=persian_text("نام و نام خانوادگی"),
            font_size=dp(17),
            size_hint_y=None,
            height=dp(55),
            padding=[dp(12), dp(15)],
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.8, 0.7, 1),
            background_normal="",
            background_active=""
        )

        # فیلد مبلغ بدهی
        debt_input = TextInput(
            hint_text=persian_text("مبلغ بدهی به تومان"),
            font_name="Vazirmatn",
            font_size=dp(17),
            multiline=False,
            halign="right",
            input_filter="int",
            size_hint_y=None,
            height=dp(55),
            padding=[dp(12), dp(15)],
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0, 0.8, 0.7, 1),
            background_normal="",
            background_active=""
        )

        # با انتخاب بدهکار، اطلاعات قبلی نمایش داده شود
        selected_person = {"id": None}

        def select_debtor(spinner, selected_name):

            if selected_name not in debtor_options:
                return

            person_id, name, debt = debtor_options[selected_name]

            selected_person["id"] = person_id

            name_input.raw_text = name
            name_input.text = persian_text(name)
            name_input.cursor = (len(name_input.text), 0)

            debt_input.text = str(int(debt))

        debtor_spinner.bind(text=select_debtor)

        # دکمه ذخیره تغییرات
        save_button = MDRaisedButton(
            text=persian_text("ذخیره تغییرات"),
            font_name="Vazirmatn",
            font_size="16sp",
            size_hint_x=1,
            height=dp(50)
        )

        content.add_widget(title)
        content.add_widget(debtor_spinner)
        content.add_widget(name_input)
        content.add_widget(debt_input)
        content.add_widget(save_button)

        popup = Popup(
            title=persian_text("ویرایش بدهکار"),
            title_font="Vazirmatn",
            content=content,
            size_hint=(0.9, 0.6)
        )

        # ذخیره اطلاعات ویرایش‌شده
        def save_changes(instance):

            person_id = selected_person["id"]
            new_name = name_input.raw_text.strip()
            debt_text = debt_input.text.strip()

            if person_id is None:
                self.show_message("لطفاً ابتدا یک بدهکار انتخاب کنید.")
                return

            if not new_name or not debt_text:
                self.show_message("لطفاً تمام فیلدها را تکمیل کنید.")
                return

            try:

                new_debt = int(debt_text)

                if new_debt < 0:
                    self.show_message(
                        "مبلغ بدهی نمی‌تواند منفی باشد."
                    )
                    return

                # به‌روزرسانی دیتابیس
                update_person(
                    self.db_path,
                    person_id,
                    new_name,
                    new_debt
                )

                # به‌روزرسانی داشبورد
                self.refresh_dashboard()

                popup.dismiss()

                self.show_message(
                    "اطلاعات بدهکار با موفقیت ویرایش شد."
                )

            except sqlite3.IntegrityError:

                self.show_message(
                    "این نام قبلاً برای بدهکار دیگری ثبت شده است."
                )

            except ValueError:

                self.show_message(
                    "مبلغ واردشده معتبر نیست."
                )

            except sqlite3.Error:

                self.show_message(
                    "خطا در ویرایش اطلاعات رخ داد."
                )

        save_button.bind(on_release=save_changes)

        popup.open()
    # ---------------------------------
    # حذف بدهکار
    # ---------------------------------

    def delete_debtor(self, instance):

        debtors = get_all(self.db_path)

        if not debtors:
            self.show_message("هنوز هیچ بدهکاری ثبت نشده است.")
            return

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(15)
        )

        title = MDLabel(
            text=persian_text("انتخاب بدهکار برای حذف"),
            font_name="Vazirmatn",
            font_size="19sp",
            bold=True,
            halign="right",
            adaptive_height=True
        )

        # ساخت فهرست بدهکاران
        debtor_options = {}

        for person_id, name, debt in debtors:

            display_name = persian_text(
                f"{name} - {debt:,.0f} تومان"
            )

            debtor_options[display_name] = person_id

        debtor_spinner = Spinner(
            text=persian_text("انتخاب بدهکار"),
            values=list(debtor_options.keys()),
            option_cls="PersianSpinnerOption",
            font_name="Vazirmatn",
            font_size=dp(16),
            size_hint_y=None,
            height=dp(55)
        )

        # دکمه حذف
        delete_button = MDRaisedButton(
            text=persian_text("حذف بدهکار"),
            font_name="Vazirmatn",
            font_size="16sp",
            size_hint_x=1,
            height=dp(50),
            md_bg_color=(0.75, 0.12, 0.12, 1)
        )

        content.add_widget(title)
        content.add_widget(debtor_spinner)
        content.add_widget(delete_button)

        popup = Popup(
            title=persian_text("حذف بدهکار"),
            title_font="Vazirmatn",
            content=content,
            size_hint=(0.9, 0.4)
        )

        # نمایش پنجره تأیید
        def confirm_delete(instance):

            selected_name = debtor_spinner.text

            if selected_name not in debtor_options:
                self.show_message("لطفاً یک بدهکار انتخاب کنید.")
                return

            person_id = debtor_options[selected_name]

            # ساخت پنجره تأیید
            confirm_content = MDBoxLayout(
                orientation="vertical",
                padding=dp(15),
                spacing=dp(15)
            )

            confirm_label = MDLabel(
                text=persian_text(
                    "آیا از حذف این بدهکار مطمئن هستید؟"
                ),
                font_name="Vazirmatn",
                font_size="17sp",
                halign="center"
            )

            buttons_layout = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(50)
            )

            yes_button = MDRaisedButton(
                text=persian_text("بله، حذف شود"),
                font_name="Vazirmatn",
                md_bg_color=(0.75, 0.12, 0.12, 1)
            )

            no_button = MDRaisedButton(
                text=persian_text("انصراف"),
                font_name="Vazirmatn"
            )

            buttons_layout.add_widget(yes_button)
            buttons_layout.add_widget(no_button)

            confirm_content.add_widget(confirm_label)
            confirm_content.add_widget(buttons_layout)

            confirm_popup = Popup(
                title=persian_text("تأیید حذف"),
                title_font="Vazirmatn",
                content=confirm_content,
                size_hint=(0.85, 0.3)
            )

            # انصراف از حذف
            no_button.bind(
                on_release=confirm_popup.dismiss
            )

            # حذف نهایی
            def perform_delete(instance):

                try:

                    delete_person(self.db_path, person_id)

                    confirm_popup.dismiss()
                    popup.dismiss()

                    self.refresh_dashboard()

                    self.show_message(
                        "بدهکار با موفقیت حذف شد."
                    )

                except sqlite3.Error:

                    self.show_message(
                        "خطا در حذف اطلاعات رخ داد."
                    )

            yes_button.bind(
                on_release=perform_delete
            )

            confirm_popup.open()

        delete_button.bind(
            on_release=confirm_delete
        )

        popup.open()

    # ---------------------------------
    # به‌روزرسانی آمار داشبورد
    # ---------------------------------

    def refresh_dashboard(self):

        debtors = get_all(self.db_path)
        total_debt = get_total(self.db_path)

        self.debt_amount_label.text = persian_text(
            f"{total_debt:,.0f} تومان"
        )

        self.count_label.text = persian_text(
            f"تعداد بدهکاران: {len(debtors)} نفر"
        )

    # ---------------------------------
    # نمایش پیام
    # ---------------------------------

    def show_message(self, message):

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12)
        )

        message_label = MDLabel(
            text=persian_text(message),
            font_name="Vazirmatn",
            font_size="17sp",
            halign="center"
        )

        close_button = MDRaisedButton(
            text=persian_text("تأیید"),
            font_name="Vazirmatn",
            size_hint_x=1
        )

        content.add_widget(message_label)
        content.add_widget(close_button)

        popup = Popup(
            title=persian_text("پیام"),
            title_font="Vazirmatn",
            content=content,
            size_hint=(0.85, 0.3)
        )

        close_button.bind(
            on_release=popup.dismiss
        )

        popup.open()



if __name__ == "__main__":
    DebtBookDesign().run()
