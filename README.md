# 🌱 정글 되새김질 메모 (JG Note)

## 📌 프로젝트 소개

정글 부트캠프에서 배운 내용을 체계적으로 관리하고 복습할 수 있는 개인 메모 웹 애플리케이션입니다.

### 주요 기능
- 📝 **메모 작성 & 관리**: 포스트잇 스타일로 학습 내용 정리
- 🔍 **검색 & 태그**: 제목, 내용, 태그 기반 검색
- 🔔 **복습 알림**: 일정 시간 후 복습 알림 제공
- 👥 **라운지**: 다른 사용자와 메모 공유 및 댓글
- 🔐 **사용자 인증**: JWT 기반 안전한 로그인

---

## 🛠️ 기술 스택

**Backend**: Flask, MongoDB, JWT  
**Frontend**: HTML/CSS/JS, Tailwind CSS  
**기타**: Python, PyMongo, Werkzeug

---

## 🚀 설치 및 실행

### 1. 환경 설정
```bash
git clone <repository-url>
cd jgnote
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
pip install -r requirements.txt
```

### 2. MongoDB 설정
- MongoDB 설치 및 실행 (localhost:27017)

### 3. 환경 변수 설정
`.env` 파일 생성:
```
SECRET_KEY=your-secret-key-here
```

### 4. 실행
```bash
python app.py
```
→ http://localhost:5000 접속

---

## 📱 사용법

1. **회원가입/로그인** → 계정 생성 후 로그인
2. **메모 작성** → 플로팅 버튼(+)으로 메모 추가
3. **검색** → 키워드 또는 `#태그명`으로 검색
4. **복습 알림** → 헤더에서 복습할 메모 확인
5. **라운지** → 메모 공유하고 댓글 작성

---

## 📁 프로젝트 구조

```
jgnote/
├── app.py                    # Flask 메인 애플리케이션
├── README.md                 # 프로젝트 문서
├── .env                      # 환경 변수 (생성 필요)
├── requirements.txt          # 의존성 패키지 목록 (생성 필요)
├── static/                   # 정적 파일 폴더
│   └── profile.png          # 기본 프로필 이미지
├── templates/               # HTML 템플릿 폴더
│   ├── login.html          # 로그인 페이지
│   ├── register.html       # 회원가입 페이지
│   ├── main.html           # 메인 메모 관리 페이지
│   ├── memo_add.html       # 메모 작성 페이지
│   ├── memo_edit.html      # 메모 수정 페이지
│   ├── profile.html        # 프로필 페이지
│   ├── reminder.html       # 복습 알림 페이지
│   ├── lounge.html         # 라운지 페이지
│   └── search.html         # 검색 결과 페이지
└── myenv/                   # Python 가상환경 폴더
    ├── bin/                 # 실행 파일들 (Linux/Mac)
    ├── lib/                 # 설치된 패키지들
    └── pyvenv.cfg          # 가상환경 설정
```

### 파일별 주요 역할

**🐍 Backend (app.py)**
- Flask 애플리케이션 설정 및 라우팅
- MongoDB 연결 및 데이터 처리
- JWT 인증 및 세션 관리
- RESTful API 엔드포인트 구현

**🎨 Frontend (templates/)**
- `login.html`, `register.html`: 사용자 인증
- `main.html`: 메모 목록 및 관리 인터페이스
- `memo_add.html`, `memo_edit.html`: 메모 CRUD 기능
- `reminder.html`: 복습 알림 시스템
- `lounge.html`: 커뮤니티 기능
- `profile.html`: 사용자 프로필 관리

**📦 정적 리소스 (static/)**
- 이미지, CSS, JavaScript 파일들
- 프로필 이미지 및 기타 에셋

---

## 📋 주요 API

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/login` | GET/POST | 로그인 |
| `/register` | POST | 회원가입 |
| `/main` | GET | 메모 목록 |
| `/memo_add` | GET/POST | 메모 작성 |
| `/reminder` | GET | 복습 알림 |
| `/lounge` | GET | 라운지 |

---

## 🔧 개발 환경

- **Python**: 3.8+
- **MongoDB**: 4.0+
- **브라우저**: Chrome, Firefox, Safari

---

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/기능명`)
3. Commit your Changes (`git commit -m 'Add: 새 기능'`)
4. Push to the Branch (`git push origin feature/기능명`)
5. Open a Pull Request
