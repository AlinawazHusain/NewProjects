import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

def send_email(smtp_server, port, sender_email, sender_password, recipient_email, subject, body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, sender_password)  # Log in to the email account

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()  # Close the server connection

# Example usage
def sendMail(city):
    SUBJECT = f"Alert for high Temperature in {city}"
    BODY = "As per out record temperature in your city {city} is more than 35 twice in a row"

    send_email(config.SMTP_SERVER, config.PORT, config.SENDER_EMAIL, config.SENDER_PASSWORD, config.RECIPIENT_EMAIL, SUBJECT, BODY)
