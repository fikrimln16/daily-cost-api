from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from database import SessionLocal
from datetime import datetime 
from pytz import timezone
import os

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello Worlda"

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body')
    response = MessagingResponse()
    print(incoming_msg)
    message = response.message()
    responded = False
    words = incoming_msg.split('@')

    
    if "hello" in incoming_msg:
        rep = "Hello Fikri, selamat datang di bot keuangan buatan Fikri.\n\n"\
            "*. ketik 'help' untuk melihat fitur-fitur .*\n"\
            "=====================================\n"
        message.body(rep)
        responded = True

    if "cek uang" in incoming_msg:
        db = get_db()
        tabungan = db.execute("SELECT uang_gopay, uang_cash, uang_rekening FROM tabungan").fetchall()
        for row in tabungan:
            uanggopay = row[0]
            uangcash = row[1]
            uangrekening = row[2]
            reminder_string = "\nUang anda tersisa : \n\n"\
                "GOPAY = {}.\n"\
                    "CASH = {}.\n"\
                        "REKENING = {}.\n\n"\
                            "TOTAL UANG : {}".format(uanggopay, uangcash, uangrekening, uanggopay+uangcash+uangrekening)
            message.body(reminder_string)
            responded = True
            db.close()


    if "hari ini" in incoming_msg:
        datenow = datetime.now(timezone('Asia/Jakarta'))
        tanggal = datenow.strftime('%Y-%m-%d')
        db = get_db()
        row = db.execute("SELECT nama, jumlah, tanggal, pembayaran FROM pengeluaran WHERE tanggal BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(tanggal, tanggal)).fetchall()
        total = 0
        harga = 0
        for i in row:
            space = "\n"
            reply = "\n\n--------------------\n"\
                        "nama barang : {} \n"\
                        "harga barang : {} \n"\
                        "tanggal beli : {} \n"\
                        "pembayaran : {}\n"\
                            "-------------------\n\n".format(i[0], i[1], i[2], i[3])
            message.body(reply)
            message.body(space)
            harga = harga + int(i[1])
            total = total + 1
            responded = True
            db.close()

        dayspent = ".\n\npada tanggal {} sudah membeli sebanyak {}\n"\
                        "pada tanggal {} sudah menghabiskan uang sejumlah {}\n\n".format(tanggal, total, tanggal,harga)
        message.body(dayspent)
        responded = True

    if "deposit uang" in incoming_msg:
        reminder_string = "Berikut adalah tata cara untuk deposito uang.\n\n"\
            "1. Pilih tabungan GOPAY/CASH/REKENING.\n"\
                "2. Ketik di chat [TABUNGAN]@[UANG]."
        message.body(reminder_string)
        responded = True

    if "bulan" in incoming_msg:
        db = get_db()
        pengeluaran = db.execute("SELECT SUM(jumlah) as 'jumlah', COUNT(jumlah) as 'total' FROM pengeluaran").fetchall()
        for row in pengeluaran:
            totalharga = row[0]
            jumlahbarang = row[1]
        reminder_string = "Berikut adalah pengeluaran anda bulan ini.\n\n"\
            "1. Total harga yang anda beli : {}.\n"\
                "2. Total barang yang anda beli : {}.".format(totalharga, jumlahbarang)
        message.body(reminder_string)
        responded = True
        db.close()

    if "cara beli barang" in incoming_msg:
        reminder_string = "Nih sayang, tata cara untuk membeli barang.\n\n"\
            "1. Format BELI@[PEMBAYARAN]@[HARGA]@[NAMA_BARANG].\n"\
                "2. Ketik di chat lalu enter."
        message.body(reminder_string)
        responded = True

    if "beli" in incoming_msg:
        reminder_string = "Mau beli apa lagi sih sayang, jangan sering2 beli barang yaa sayang, takutnya boros! :D\n"
        message.body(reminder_string)
        responded = True

    if "pengeluaran" in incoming_msg:
        reminder_string = "Berikut adalah tata cara untuk melihat pengeluaran.\n\n"\
            "1. Ketik 'hari ini' untuk melihat pengeluaran hari ini'.\n"\
                "2. Ketik dengan format PENGELUARAN@[tanggal (tahun-bulan-hari)]\n"\
                "3. Ketik 'bulan' untuk melihat pengeluaran bulan ini lalu enter."
        message.body(reminder_string)
        responded = True

    if "narik uang" in incoming_msg:
        reminder_string = "Berikut adalah tata cara untuk menarik uang.\n\n"\
            "1. Ketik dengan format TARIK@[TABUNGAN]@[jumlah_uang] untuk menarik uang'.\n"\
                "2. untuk menarik ini, tidak akan masuk sebagai pengeluaran harian\n"
        message.body(reminder_string)
        responded = True

    if "help" in incoming_msg:
        reminder_string = "Berikut adalah tata cara untuk membeli barang.\n\n"\
            "1. cek uang : tinggal ketik 'cek uang'.\n"\
                "2. deposito uang : tinggal ketik 'deposit uang'.\n"\
                    "3. pengeluaran bulanan : tinggal ketik 'bulan'.\n"\
                        "4. beli barang : tinggal ketik 'beli barang'"
        message.body(reminder_string)
        responded = True

    if "makasih" in incoming_msg:
        reminder_string = "Sama-sama mas pikri, semoga bot ini sangat berguna untuk kehidupan mas pikri :)) Love You"
        message.body(reminder_string)
        responded = True

    if "dikit" in incoming_msg:
        reminder_string = "Yah kasiann, makanya sering-sering nabung mas pikri, makanya pake bot ini ya sayang biar irit :D"
        message.body(reminder_string)
        responded = True
    
    if len(words) == 1 and "no" in incoming_msg:
        reply = "OK, Have a nice day!"
        message.body(reply)
        responded = True


    elif len(words) != 1:
        input_type = words[0].strip()
        input_string = words[1].strip()
        if input_type == "GOPAY":

            db = get_db()
            saldoawalgopay = db.execute("SELECT uang_gopay FROM tabungan").fetchone()
            for i in saldoawalgopay:
                saldogopay = i
            db.close()

            tambahuanggopay = int(input_string)
            saldoakhirgopay = saldogopay + tambahuanggopay
            db.execute("UPDATE tabungan SET uang_gopay = {} WHERE user_id = 1".format(saldoakhirgopay))
            db.commit()

            reply="Berhasil memasukkan GOPAY"
            printout(input_string)
            message.body(reply)
            responded = True

        if input_type == "CASH":

            db = get_db()
            saldoawalcash = db.execute("SELECT uang_cash FROM tabungan").fetchone()
            for i in saldoawalcash:
                saldocash = i
            db.close()

            tambahuangcash = int(input_string)
            saldoakhircash = saldocash + tambahuangcash
            db.execute("UPDATE tabungan SET uang_cash = {} WHERE user_id = 1".format(saldoakhircash))
            db.commit()
            
            printout(input_string)
            reply="Berhasil memasukkan CASH"
            message.body(reply)
            responded = True

        if input_type == "REKENING":

            db = get_db()
            saldoawalrekening = db.execute("SELECT uang_rekening FROM tabungan").fetchone()
            for i in saldoawalrekening:
                saldorekening = i
            db.close()

            tambahuangrekening = int(input_string)
            saldoakhirrekening = saldorekening + tambahuangrekening
            db.execute("UPDATE tabungan SET uang_rekening = {} WHERE user_id = 1".format(saldoakhirrekening))
            db.commit()
            
            reply="Berhasil memasukkan REKENING"
            message.body(reply)
            printout(input_string)
            responded = True

        if input_type == "BELI":
            input_harga = words[2].strip()
            input_barang = words[3].strip()

            if input_string == "GOPAY":
                db = get_db()
                saldoawalgopay = db.execute("SELECT uang_gopay FROM tabungan").fetchone()
                for i in saldoawalgopay:
                    saldogopay = i
                db.close()
                printout(input_barang)
                pengurangan = int(input_harga)
                saldoakhirgopay = saldogopay - pengurangan
                db.execute("UPDATE tabungan SET uang_gopay = {} WHERE user_id = 1".format(saldoakhirgopay))
                db.commit()
                db.close()

            if input_string == "CASH":
                db = get_db()
                saldoawalcash = db.execute("SELECT uang_cash FROM tabungan").fetchone()
                for i in saldoawalcash:
                    saldocash = i
                db.close()

                pengurangancash = int(input_harga)
                saldoakhircash = saldocash - pengurangancash
                db.execute("UPDATE tabungan SET uang_cash = {} WHERE user_id = 1".format(saldoakhircash))
                db.commit()
                db.close()

            if input_string == "REKENING":
                db = get_db()
                saldoawalrekening = db.execute("SELECT uang_rekening FROM tabungan").fetchone()
                for i in saldoawalrekening:
                    saldorekening = i
                db.close()

                penguranganrekening = int(input_harga)
                saldoakhirrekening = saldorekening - penguranganrekening
                db.execute("UPDATE tabungan SET uang_rekening = {} WHERE user_id = 1".format(saldoakhirrekening))
                db.commit()
                db.close()

            reply="Berhasil memasukkan inputan"
            message.body(reply)
            responded = True
            x = datetime.now(timezone('Asia/Jakarta'))
            db.execute("INSERT INTO pengeluaran VALUES(null, '{}', '{}', {}, '{}', 1 )".format(input_barang, x, int(input_harga), input_string))
            db.commit()

        if input_type == "PENGELUARAN":
            db = get_db()
            row = db.execute("SELECT nama, jumlah, tanggal, pembayaran FROM pengeluaran WHERE tanggal BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(input_string, input_string)).fetchall()
            total = 0
            harga = 0
            for i in row:
                space = "\n"
                reply = "\n\n--------------------\n"\
                        "nama barang : {} \n"\
                        "harga barang : {} \n"\
                        "tanggal beli : {} \n"\
                        "pembayaran : {}\n"\
                            "-------------------\n\n".format(i[0], i[1], i[2], i[3])
                message.body(reply)
                message.body(space)
                harga = harga + int(i[1])
                total = total + 1
                responded = True
            db.close()

            dayspent = ".\n\n pada tanggal {} sudah membeli sebanyak {}\n"\
                        "pada tanggal {} sudah menghabiskan uang sejumlah {}\n\n".format(input_string, total, input_string,harga)
            message.body(dayspent)
            responded = True

        if input_type == "TARIK":
            input_tarik = words[2].strip()
            if input_string == "GOPAY":

                db = get_db()
                saldoawalgopay = db.execute("SELECT uang_gopay FROM tabungan").fetchone()
                for i in saldoawalgopay:
                    saldogopay = i
                db.close()

                tambahuanggopay = int(input_tarik)
                saldoakhirgopay = saldogopay - tambahuanggopay
                db.execute("UPDATE tabungan SET uang_gopay = {} WHERE user_id = 1".format(saldoakhirgopay))
                db.commit()

                reply="Berhasil menarik GOPAY"
                printout(input_string)
                message.body(reply)
                responded = True

            if input_string == "CASH":

                db = get_db()
                saldoawalcash = db.execute("SELECT uang_cash FROM tabungan").fetchone()
                for i in saldoawalcash:
                    saldocash = i
                db.close()

                tambahuangcash = int(input_tarik)
                saldoakhircash = saldocash - tambahuangcash
                db.execute("UPDATE tabungan SET uang_cash = {} WHERE user_id = 1".format(saldoakhircash))
                db.commit()
                
                printout(input_string)
                reply="Berhasil menarik CASH"
                message.body(reply)
                responded = True

            if input_string == "REKENING":

                db = get_db()
                saldoawalrekening = db.execute("SELECT uang_rekening FROM tabungan").fetchone()
                for i in saldoawalrekening:
                    saldorekening = i
                db.close()

                tambahuangrekening = int(input_tarik)
                saldoakhirrekening = saldorekening - tambahuangrekening
                db.execute("UPDATE tabungan SET uang_rekening = {} WHERE user_id = 1".format(saldoakhirrekening))
                db.commit()
                
                reply="Berhasil menarik REKENING"
                message.body(reply)
                printout(input_string)
                responded = True


        if not responded:
            message.body("Incorect reequst format")

    return str(response)


def printout(msg):
    return msg


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))