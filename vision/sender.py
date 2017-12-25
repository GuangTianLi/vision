import logging
import smtplib
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText

from vision.creator import CreatorRunner
from vision.datareportcenter import DataReportCenter

logger = logging.getLogger(__name__)


class SenderRunner(DataReportCenter):
    def loginSTMP(self, settings):
        self.smtp = smtplib.SMTP_SSL(settings.get("SMTP_ADDRESS"), port=settings.get("SMTP_PORT"))
        self.smtp.login(settings.get("EMAIL_USER"), settings.get('EMAIL_PASSWORD'))

    def sendEmail(self, data_report, to_address):
        from_user = data_report.settings.get("EMAIL_USER")
        to_user = to_address
        msg = MIMEMultipart()
        msg['Subject'] = Header(data_report.settings.get("DATA_REPORT_TITLE", data_report.name), 'utf-8').encode()
        msg['To'] = from_user
        msg['From'] = to_user
        if data_report.settings.get("SVG_FILE"):
            read_svg_name = data_report.svg_file_name
            send_svg_name = "{0}".format(read_svg_name.split('/')[-1])
            css = "<style>.showy {height: 100% !important;width: 100% !important;}\n.no-showy {display: none;}\n</style>"
            with open(read_svg_name, 'rb') as f:
                mime = MIMEBase('xml', 'svg', filename=send_svg_name)
                mime.add_header('Content-Disposition', 'attachment', filename=send_svg_name)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')

                mime.set_payload(f.read())

                encoders.encode_base64(mime)

                msg.attach(mime)
                msg.attach(MIMEText(css +
                                    '<img class="showy" width="0" height="0" src="cid:0">\n<img class="no-showy" src="my-image.jpg">',
                                    'html', 'utf-8'))

        read_csv_name = data_report.csv_file_name
        send_csv_name = "{0}".format(read_csv_name.split('/')[-1])
        with open(read_csv_name, 'rb') as f:
            mime = MIMEBase('xml', 'svg', filename=send_csv_name)
            mime.add_header('Content-Disposition', 'attachment', filename=send_csv_name)
            mime.add_header('Content-ID', '<1>')
            mime.add_header('X-Attachment-Id', '1')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)

        self.smtp.sendmail(from_user, to_user, msg.as_string())

    def quit(self):
        self.smtp.quit()

    def send(self, data_report_name, *args, **kwargs):
        '''
        This method is to send email by DataReport
        Parameters
        ----------
        data_report_name : DataReport class's name

        Returns
        -------

        '''

        creator = CreatorRunner(self.settings)
        creator.create(data_report_name)

        self.loginSTMP(creator.data_report.settings)

        for to_address in creator.data_report.settings.get("EMAIL_ADDRESS_LIST"):
            self.sendEmail(creator.data_report, to_address)
        self.quit()
