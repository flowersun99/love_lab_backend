from flask import Flask, request, jsonify
from flask_cors import CORS
import yagmail
import os
from dotenv import load_dotenv
import re

load_dotenv()  # .env 파일의 환경변수 로드

app = Flask(__name__)
CORS(app)

# 환경변수 검증
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_TO = os.getenv('EMAIL_TO')

if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
    raise ValueError("필수 환경변수가 설정되지 않았습니다. EMAIL_USER, EMAIL_PASS, EMAIL_TO를 확인해주세요.")

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/send', methods=['POST'])
def send_mail():
    data = request.json
    contact = data.get('contact', '')
    
    if not contact:
        return jsonify({'success': False, 'msg': '입력값이 없습니다.'}), 400
    
    if not is_valid_email(EMAIL_TO):
        return jsonify({'success': False, 'msg': '수신자 이메일 형식이 올바르지 않습니다.'}), 500

    try:
        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
        yag.send(
            to=EMAIL_TO,
            subject='상담 신청이 도착했습니다!',
            contents=f'상담 신청 정보: {contact}'
        )
        return jsonify({'success': True})
    except yagmail.error.YagConnectionError:
        return jsonify({'success': False, 'msg': '이메일 서버 연결에 실패했습니다.'}), 500
    except yagmail.error.YagAuthenticationError:
        return jsonify({'success': False, 'msg': '이메일 인증에 실패했습니다.'}), 500
    except Exception as e:
        print(f"예상치 못한 오류 발생: {str(e)}")
        return jsonify({'success': False, 'msg': '메일 전송 중 오류가 발생했습니다.'}), 500

# 개발 환경에서만 실행
if __name__ == '__main__':
    app.run(debug=True)