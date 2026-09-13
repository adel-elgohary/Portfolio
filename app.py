from flask import Flask, request, jsonify, render_template_string
from twilio.rest import Client

app = Flask(__name__)

# بيانات Twilio الخاصة بك
ACCOUNT_SID = 'YOUR_ACCOUNT_SID'  # استبدله بـ Account SID الخاص بك
AUTH_TOKEN = 'YOUR_AUTH_TOKEN'    # استبدله بـ Auth Token الخاص بك
TWILIO_NUMBER = 'whatsapp:+201204287281'
MY_PHONE_NUMBER = 'whatsapp:+201204287281'  # رقم هاتفك

@app.route('/')
def home():
    # يعرض صفحة الـ HTML عند فتح الموقع
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        # استلام البيانات القادمة من نموذج HTML
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'success': False, 'error': 'الرسالة فارغة'}), 400

        # إرسال الرسالة إلى الواتساب عبر Twilio
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_=TWILIO_NUMBER,
            body=f"📩 رسالة جديدة من الموقع:\n\n{user_message}",
            to=MY_PHONE_NUMBER
        )

        return jsonify({'success': True, 'sid': message.sid})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # تشغيل السيرفر المحلي
    app.run(debug=True, port=5000)
