package notifications;

import java.util.Date;
import java.util.Properties;

import javax.mail.Message;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public abstract class EmailSender {
    
    public static void sendEmail(
        final String to,
        final String subject,
        final String body
    ) {
        String username = "masonwright14@gmail.com";
        String password = "wtlzbdiotendecfz";
        String smtphost = "smtp.gmail.com";
        String from = "masonwright14@gmail.com";
        Transport myTransport = null;

        try {
           Properties props = System.getProperties();
           props.put("mail.smtp.host", "smtp.gmail.com");
               props.put("mail.smtp.socketFactory.port", "465");
               props.put(
                   "mail.smtp.socketFactory.class",
                   "javax.net.ssl.SSLSocketFactory"
               );
               props.put("mail.smtp.auth", "true");
               props.put("mail.smtp.port", "465");

           Session mailSession = Session.getDefaultInstance(props, null);
           Message msg = new MimeMessage(mailSession);
           msg.setFrom(new InternetAddress(from));
           InternetAddress[] address = {new InternetAddress(to)};
           msg.setRecipients(Message.RecipientType.TO, address);
           msg.setSubject(subject);
           msg.setText(body);
           msg.setSentDate(new Date());

           myTransport = mailSession.getTransport("smtp");
           myTransport.connect(smtphost, username, password);
           msg.saveChanges();
           myTransport.sendMessage(msg, msg.getAllRecipients());
           myTransport.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(final String[] args) {
        sendEmail(
            "masonwright14@gmail.com",
            "test",
            "Hello world!"
        );
    }
}
