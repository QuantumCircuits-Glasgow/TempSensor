def send_autoemail(sensor_number, temp, logged_time):
    import smtplib, ssl

    sensor_number = sensor_number
    temp = temp
    logged_time = logged_time
    sleep_time = 120 #only send an email a maximum of once every two hours

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "116raspberrypi@gmail.com"  # Enter your address
    receiver_email = "eng-quantumcircuits-uog@lists.cent.gla.ac.uk"  # Enter receiver address
    password = "quantumspin" #
    message = """\
    Subject: Chilled water threshold temperature exceeded!

    Sensor {} reached a temperature of {} degrees C at {}. This message will only be sent a maximum of once every 2 hours.""".format(sensor_number, temp, logged_time)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        time.sleep(sleep_time)
    return