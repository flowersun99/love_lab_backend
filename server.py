
from flask import Flask, request, jsonify
from flask_cors import CORS
import yagmail
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 환경변수 로드

app = Flask(__name__)
CORS(app)

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_TO = os.getenv('EMAIL_TO')

@app.route('/send', methods=['POST'])
def send_mail():
    data = request.json
    contact = data.get('contact', '')
    if not contact:
        return jsonify({'success': False, 'msg': '입력값이 없습니다.'}), 400
    try:
        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
        yag.send(
            to=EMAIL_TO,
            subject='상담 신청이 도착했습니다!',
            contents=f'상담 신청 정보: {contact}'
        )
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'msg': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)