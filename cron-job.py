from datetime import datetime, timedelta

def print_message(num):
    print(f"Tried to send {num} order rating emails")
    return True

# cron 15/15 min
def main():
    from datetime import datetime, timedelta
    from model import Order

    from PostgreSQL_lib import Database

    current_time = datetime.utcnow()
    time_start = current_time - timedelta(minutes=135)
    time_end = current_time - timedelta(minutes=120)

    try:
        session = Database.get_session('postgres://usuario:senha@database-host.delivery:5432/orders')
        approved_orders = session.query(Order).filter(Order.last_status.in_(["APPROVED"]), 
                                                      Order.created_date > time_start, 
                                                      Order.created_date < time_end)
        session.close()
        print("Finished querying orders. Starting email sending process")
        for order in approved_orders:
            from AWS import SES
            import os

            SES.send_template(
                region="us-east-1",
                aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
                aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
                email=order.customer_email,
                template="s3://" + "email_templates/" + "rate_your_experience.html",
            )
        return print_message(len(approved_orders))
    except Exception as e:
        raise e