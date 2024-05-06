# استفاده از تصویر پایتون به عنوان پایه
FROM python:3.8

# کپی سورس کد ربات به داخل تصویر

WORKDIR /app

# نصب وابستگی‌های پروژه
RUN pip install telebot
RUN pip install random
RUN pip install re


COPY . .
# تنظیم دستور اجرای ربات
CMD ["python", "moz gostar pishrafte tar"]