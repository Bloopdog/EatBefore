            isOK = log_template.create_log(
                "notification",
                0,
                'create',
                'notification',
                'Successful sending of email to ' + emailToSend + ' at notification microservice. \n Subject: ' + subject + '\n Body: ' + message,
                'success')