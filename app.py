from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from pymongo import MongoClient
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_csrf_token
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

# 환경 변수 로딩
load_dotenv()
app = Flask(__name__)

# JWT 설정
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['jungle_note']
memo_collection = db['memos']
user_collection = db['users']

# 루트 → 로그인 페이지 리다이렉트
@app.route('/')
def root():
    return redirect(url_for('login'))

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json()
    print("받은 로그인 데이터 : ", data)
    if data is None:
        return jsonify({'success': False, 'msg': '요청 데이터가 없습니다.'}), 400

    username = data.get('username')
    password = data.get('password')

    user = user_collection.find_one({'user_id': username})
    if not user:
        return jsonify({'success': False, 'msg': '존재하지 않는 사용자입니다.'}), 401

    if not check_password_hash(user['user_pw'], password):
        return jsonify({'success': False, 'msg': '비밀번호가 틀렸습니다.'}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    csrf_token = get_csrf_token(access_token)

    response = jsonify({
        'success': True,
        'msg': '로그인 성공!',
        'csrf_token': get_csrf_token(access_token)
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response

# 로그아웃
@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"logout": True})
    unset_jwt_cookies(response)
    return response

# 회원가입 페이지
@app.route('/make', methods=['GET'])
def make():
    return render_template('register.html')

# 회원가입 처리
@app.route('/register', methods=["POST"])
def register_post():
    data = request.get_json()
    user_name = data.get('name')        # HTML form과 맞춰서 수정
    user_id = data.get('username')
    user_email = data.get('email')
    user_pw = data.get('password')

    if user_collection.find_one({'user_id': user_id}):
        return jsonify({'success': False, 'msg': '이미 존재하는 아이디입니다.'})

    hashed_pw = generate_password_hash(user_pw)

    user_collection.insert_one({
        'user_name': user_name,
        'user_id': user_id,
        'user_email': user_email,
        'user_pw': hashed_pw
    })

    return jsonify({'success': True, 'msg': '회원가입 완료!'})

# 메인 페이지
@app.route('/main')
@jwt_required()
def main():
    user = get_jwt_identity()
    memos = list(memo_collection.find({'user_id': user}))
    return render_template('main.html', memos=memos)

# 메모 추가
@app.route('/memo_add', methods=["GET", "POST"])
@jwt_required()  # 이거 없으면 로그인 없이 접근 가능함
def memo_add():
    if request.method == 'GET':
        return render_template('memo_add.html')  # 메모 작성 폼 페이지 렌더링

    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        user_id = get_jwt_identity()

        memo_collection.insert_one({
            'user_id': user_id,
            'title': title,
            'content': content,
            'created_at': datetime.now(),
            'repeat_visible': True
        })
        return jsonify({'success': True, 'msg': '저장 완료!'})

# 메모 삭제
@app.route('/memo/<memo_id>', methods=["DELETE"])
@jwt_required()
def delete_memo(memo_id):
    user_id = get_jwt_identity()

    result = memo_collection.delete_one({
        '_id': ObjectId(memo_id),
        'user_id': user_id
    })

    if result.deleted_count == 1:
        return jsonify({'success': True, 'msg': '삭제 완료!'})
    else:
        return jsonify({'success': False, 'msg': '삭제 실패!'}), 400


# 리프레시 토큰 → 액세스 토큰 재발급
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user = get_jwt_identity()
    access_token = create_access_token(identity=user)
    response = jsonify({'refresh': True})
    set_access_cookies(response, access_token)
    return response

# 메모 보기 페이지
@app.route('/memo')
@jwt_required()
def memo():
    return render_template('memo.html')


# 리마인더
@app.route('/reminder')
@jwt_required()
def reminder():
    user_id = get_jwt_identity()

    # threshold_date = (datetime.now.date() - timedelta(days=7))
    # threshold_datetime = datetime.combine(threshold_date, datetime.min.time()) 7일 후 !
    threshold_datetime = datetime.now() - timedelta(minutes=1)

    repeat_memos = list(memo_collection.find({
        'user_id': user_id,
        'created_at': { '$lte': threshold_datetime },
        'repeat_visible': True
    }).sort('created_at', -1))  # -1: 내림차순

    return render_template('reminder.html', memos=repeat_memos)

# 완료된 할 일
@app.route('/hide_memo', methods=['POST'])
@jwt_required()
def hide_memo():
    user_id = get_jwt_identity()

    if not request.is_json:
        return jsonify({'msg': 'JSON 형식이 아닙니다.'}), 400

    memo_id = request.json.get('memo_id')

    if not memo_id:
        return jsonify({'msg': 'memo_id가 없습니다.'}), 400

    try:
        object_id = ObjectId(memo_id)
    except InvalidId:
        return jsonify({'msg': '유효하지 않은 memo_id입니다.'}), 400

    result = memo_collection.update_one(
        {'_id': object_id, 'user_id': user_id},
        {'$set': {'repeat_visible': False}}
    )

    if result.modified_count == 1:
        return jsonify({'msg': '숨김 처리 완료'}), 200
    else:
        return jsonify({'msg': '해당 메모가 없거나 권한 없음'}), 400

# 복습 내용 확인
@app.route('/memo/<memo_id>')
@jwt_required()
def review(memo_id):
    user_id = get_jwt_identity()

    memo = memo_collection.find_one({
        '_id': ObjectId(memo_id),
        'user_id': user_id
    })

    if not memo:
        return abort(404, description="해당 메모를 찾을 수 없습니다.")

    return render_template('review.html', memo=memo)

@app.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = user_collection.find_one({'user_id': user_id}, {'_id': False})
    return render_template('profile.html', user=user)

@app.route('/profile_edit', methods=['GET', 'POST'])
@jwt_required()
def profile_edit():
    user_id = get_jwt_identity()

    if request.method == 'GET':
        user = user_collection.find_one({'user_id': user_id}, {'_id': False})
        return render_template('profile_edit.html', user=user)

    data = request.get_json()
    new_id = data.get('user_id')
    new_email = data.get('email')
    new_password = data.get('password')

    update_fields = {
        'user_id': new_id,
        'user_email': new_email
    }
    if new_password:
        update_fields['user_pw'] = generate_password_hash(new_password)

    result = user_collection.update_one(
        {'user_id': user_id},
        {'$set': update_fields}
    )

    # ID가 변경되었으면 JWT도 갱신
    if new_id != user_id:
        access_token = create_access_token(identity=new_id)
        refresh_token = create_refresh_token(identity=new_id)
        response = jsonify({'success': True, 'msg': '수정 완료! (ID 변경됨)'})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response

    return jsonify({'success': True, 'msg': '수정 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
