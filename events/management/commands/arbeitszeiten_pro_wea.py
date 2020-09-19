import os
import csv
import pyodbc
import datetime
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        todayDate = datetime.date.today()
        if todayDate == todayDate.replace(day=1):
            os.environ["ODBCSYSINI"] = "/home/S713FF3N"
            con = pyodbc.connect('DSN=sqlserverdatasource;Uid=xs_read;Pwd=xs_read_1;Encrypt=yes;Connection Timeout=30;Database=LmobileProd;')

            if con:
                cursor = con.cursor()

                request_month = todayDate.month - 1
                request_year = todayDate.year
                if request_month == 0:
                    request_month = 12
                    request_year =  request_year - 1
                startDate = todayDate.replace(day=1, month=request_month, year=request_year)
                endDate = todayDate.replace(day=1)
                endDate = endDate - datetime.timedelta(days=1)

                request = '''SELECT Arbeitsstd.Windpark, Arbeitsstd.WEA, Arbeitsstd.Kunde, Arbeitsstd.Arbeitsstunden, Transportstd.Transportstunden FROM (
                                SELECT CRM.Contact.Name AS Windpark, SMS.InstallationHead.Description AS WEA, CRM.Company.ShortText AS Kunde, Sum(SMS.ServiceOrderTimePostings.DurationInMinutes/60) AS Arbeitsstunden
                                FROM ((((SMS.InstallationHead INNER JOIN SMS.ServiceOrderHead ON SMS.InstallationHead.InstallationNo = SMS.ServiceOrderHead.InstallationNo) INNER JOIN SMS.ServiceOrderTimePostings ON SMS.ServiceOrderHead.OrderNo = SMS.ServiceOrderTimePostings.OrderNo) INNER JOIN SMS.ServiceObject ON SMS.InstallationHead.FolderKey = SMS.ServiceObject.ContactKey) INNER JOIN CRM.Contact ON SMS.ServiceObject.ContactKey = CRM.Contact.ContactId) INNER JOIN CRM.Company ON CRM.Company.ContactKey = SMS.ServiceOrderHead.CustomerContactId
                                WHERE (((SMS.ServiceOrderTimePostings.ItemNo) In ('820001','820003','820004','820005','820006','820101','820103','820104','820105'))) And SMS.ServiceOrderTimePostings.Date > DATEFROMPARTS ('''+str(startDate.year)+","+str(startDate.month)+","+str(startDate.day)+''') And SMS.ServiceOrderTimePostings.Date < DATEFROMPARTS ('''+str(endDate.year)+","+str(endDate.month)+","+str(endDate.day)+''') And SMS.ServiceOrderTimePostings.DurationInMinutes<>1440 GROUP BY CRM.Contact.Name, SMS.InstallationHead.Description, CRM.Company.ShortText)
                            AS Arbeitsstd LEFT JOIN (
                                SELECT SMS.InstallationHead.Description AS TsWEA, Sum(SMS.ServiceOrderTimePostings.DurationInMinutes/60) AS Transportstunden
                                FROM ((((SMS.InstallationHead INNER JOIN SMS.ServiceOrderHead ON SMS.InstallationHead.InstallationNo = SMS.ServiceOrderHead.InstallationNo) INNER JOIN SMS.ServiceOrderTimePostings ON SMS.ServiceOrderHead.OrderNo = SMS.ServiceOrderTimePostings.OrderNo) INNER JOIN SMS.ServiceObject ON SMS.InstallationHead.FolderKey = SMS.ServiceObject.ContactKey) INNER JOIN CRM.Contact ON SMS.ServiceObject.ContactKey = CRM.Contact.ContactId) INNER JOIN CRM.Company ON CRM.Company.ContactKey = SMS.ServiceOrderHead.CustomerContactId
                                WHERE (((SMS.ServiceOrderTimePostings.ItemNo) In ('820002','820007','820106','820107'))) And SMS.ServiceOrderTimePostings.Date > DATEFROMPARTS ('''+str(startDate.year)+","+str(startDate.month)+","+str(startDate.day)+''') And SMS.ServiceOrderTimePostings.Date < DATEFROMPARTS ('''+str(endDate.year)+","+str(endDate.month)+","+str(endDate.day)+''') And SMS.ServiceOrderTimePostings.DurationInMinutes<>1440 GROUP BY CRM.Contact.Name, SMS.InstallationHead.Description, CRM.Company.ShortText)
                            AS Transportstd ON Arbeitsstd.WEA = Transportstd.TsWEA
                            ORDER BY Arbeitsstd.WEA;'''
                cursor.execute(request)

                filename = settings.MEDIA_ROOT + "arbeitszeiten_pro_wea/Arbeitszeiten_pro_WEA_"+ (startDate).strftime("%B") + "_" + str(startDate.year) + ".csv"
                with open(filename, "w", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([i[0] for i in cursor.description])
                    csv_writer.writerows(cursor)

                headline = "Arbeitszeiten pro WEA "+ (startDate).strftime("%B") + " " + str(startDate.year)
                mail_content="Im Anhang befinden sich die Arbeitszeiten pro WEA für den " + (startDate).strftime("%B") + " " + str(startDate.year)
                mail_content += """<br><br><br> Da es sich bei der hierbei um eine .CSV-Datei handelt, müssen die Daten in Excel importiert werden, damit sie korrekt angezeigt werden. Dafür müssen folgende Schritte in Excel durchgeführt werden:<br>
                                    <br><b>Neuere Versionen:</b><br>
                                    <BLOCKQUOTE>
                                        1. Klicken Sie auf der Registerkarte <b>Daten</b> in der Gruppe <b>#a0 Transformationsdaten</b> abrufen auf <b>von Text/CSV</b>.<br>
                                        <br>
                                        2. Suchen Sie im Dialogfeld <b>Daten importieren</b> nach der Textdatei, die Sie importieren möchten, und doppelklicken Sie darauf, und klicken Sie auf <b>importieren</b>.<br>
                                        <br>
                                        3. Wählen Sie als <b>Dateiursprung Unicode (UTF-8)</b> aus, damit Umlaute korrekt angezeigt werden.<br>
                                        <br>
                                        4. Im Dialogfeld Vorschau stehen Ihnen mehrere Optionen zur Auswahl:<br>
                                            <BLOCKQUOTE>
                                            <br>
                                            - Wählen Sie <b>Laden</b> aus, wenn Sie die Daten direkt in ein neues Arbeitsblatt laden möchten.<br>
                                            <br>
                                            - Sie können auch Load to auswählen, wenn Sie die Daten in eine Tabelle, eine PivotTable/PivotChart, ein vorhandenes/neues Excel-Arbeitsblatt laden oder einfach eine Verbindung erstellen möchten. Darüber hinaus haben Sie die Möglichkeit, Ihre Daten zum Datenmodellhinzuzufügen.<br>
                                            <br>
                                            - Wählen Sie Daten transformieren aus, wenn Sie die Daten in Power Query laden möchten, und bearbeiten Sie Sie, bevor Sie Sie in Excel bringen.<br>
                                            </BLOCKQUOTE>
                                    </BLOCKQUOTE>
                                    <br>
                                    <b>Office 2016-2010</b>:<br>
                                    <BLOCKQUOTE>
                                        1. Klicken Sie auf die Zelle, in die die Daten aus der Textdatei eingefügt werden sollen.<br>
                                        <br>
                                        2. Klicken Sie auf der Registerkarte <b>Daten</b> in der Gruppe <b>Externe Daten</b> abrufen auf <b>Aus Text</b>.<br>
                                        <br>
                                        3. Suchen Sie im Dialogfeld <b>Daten importieren</b> nach der Textdatei, die Sie importieren möchten, und doppelklicken Sie darauf, und klicken Sie auf <b>importieren</b>.<br>
                                        <br>
                                        <BLOCKQUOTE>
                                            - Folgen Sie den Anweisungen des Text Import-Assistenten. Klicken Sie auf einer beliebigen Seite des Text Import-Assistenten auf Hilfe Schaltflächensymbol , um weitere Informationen zur Verwendung des Assistenten zu erhalten.<br>
                                            - Damit Umlaute korrekt angezeigt werden, wählen Sie als <b>Dateiursprung Unicode (UTF-8)</b> aus.<br>
                                            - Wenn Sie die Schritte im Assistenten beendet haben, klicken Sie auf <b>Fertig stellen</b>, um den Importvorgang abzuschließen.<br>
                                        </BLOCKQUOTE>
                                        <br>
                                        4. Führen Sie im Dialogfeld <b>Daten importieren</b> folgende Schritte aus:<br>
                                        <BLOCKQUOTE>
                                            <br>
                                            a) Führen Sie unter <b>Wo sollen die Daten eingefügt werden?</b> eine der folgenden Aktionen aus:<br>
                                                <BLOCKQUOTE>
                                                <br>
                                                - Wenn Sie die Daten an die ausgewählte Position zurückgeben möchten, klicken Sie auf <b>Vorhandenes Arbeitsblatt</b>.<br>
                                                <br>
                                                - Wenn Sie die Daten an die obere linke Ecke eines neuen Arbeitsblatts zurückgeben möchten, klicken Sie auf <b>Neues Arbeitsblatt</b>.<br>
                                                <br>
                                                </BLOCKQUOTE>
                                            b) Klicken Sie optional auf <b>Eigenschaften</b>, um die Aktualisierungs-, Formatierungs- und Layoutoptionen für die importierten Daten festzulegen.<br>
                                            <br>
                                            c) Klicken Sie auf <b>OK</b>.<br>
                                                <br>
                                            - Der externe Datenbereich wird in Excel an der angegebenen Position eingefügt.
                                        </BLOCKQUOTE>
                                    </BLOCKQUOTE>"""
                recipient = "arbeitssicherheit@deutsche-windtechnik.com"

                mail = EmailMessage(subject=headline, body=mail_content, from_email='success-map@deutsche-windtechnik.com', to=[recipient])
                mail.content_subtype = "html"
                mail.attach_file(filename)
                mail.send()

                con.close()
