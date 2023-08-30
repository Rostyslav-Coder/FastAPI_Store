"""src/tasks/tasks.py"""

import smtplib
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER
from src.domain.orders import OrderPublic
from src.domain.users import User

celery = Celery("tasks", broker="redis://localhost:6379")


def get_email(user: User, subject: str, orders: list[OrderPublic]):
    """Email message options"""

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = SMTP_USER
    email["To"] = user.email

    # Create the email content using the orders_public list and the user object
    if user.is_manager:
        email_content = (
            f"Dear {user.first_name},\n\n"
            f"The following orders have been updated:\n"
        )
        for order in orders:
            email_content += (
                f"- Order ID: {order.id},\n"
                f"- Product ID: {order.product_id},\n"
                f"- Quantity: {order.amount},\n"
                f"- Delivery Address: {order.delivery_address},\n"
                f"- Order Date: {order.order_date}\n"
            )
    else:
        email_content = (
            f"Dear {user.first_name} {user.last_name},\n\n"
            f"The following orders have been updated:\n"
        )
        for order in orders:
            email_content += (
                f"- Product ID: {order.product_id},\n"
                f"Quantity: {order.amount},\n"
                f"Order Date: {order.order_date}\n"
            )

    email_content += "\nBest regards,\nYour FastAPI Store"

    email.set_content(email_content)

    return email


@celery.task
def send_email(user_: User, subject_: str, orders_: list[OrderPublic]):
    """Send Email message"""

    email = get_email(user=user_, subject=subject_, orders=orders_)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)
