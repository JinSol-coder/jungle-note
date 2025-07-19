# 🌱 정글 되새김질 메모 (JG Note)

## 📌 프로젝트 소개

정글 부트캠프에서 배운 내용을 체계적으로 관리하고 복습할 수 있는 개인 메모 웹 애플리케이션입니다.

### 주요 기능

- 📝 **메모 작성 & 관리**: 포스트잇 스타일로 학습 내용 정리, 개인적으로만 볼 수 있는 노란 메모와 모두에게 보여주고 싶은 보라색 메모로 전환할 수 있음
- 🔍 **검색 & 태그**: 제목, 내용, 태그 기반 검색
- 🔔 **복습 알림**: 일정 시간 후 복습 알림 제공
- 👥 **라운지**: 다른 사용자와 메모 공유 및 댓글
- 🔐 **사용자 인증**: JWT 기반 안전한 로그인
- 🤖 **AI 챗봇**: OpenAI를 활용한 학습 내용 요약 및 분석

---

## 🛠️ 기술 스택

**Backend**: Flask, MongoDB, JWT  
**Frontend**: HTML/CSS/JS, Tailwind CSS  
**기타**: Python, PyMongo, Werkzeug, OpenAI

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

- MongoDB 접속 (외부 서버 사용 중)
- 또는 로컬 MongoDB 설치 후 app.py의 연결 문자열 수정

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
├── static/                   # 정적 파일 폴더
│   └── profile.png          # 기본 프로필 이미지
├── templates/               # HTML 템플릿 폴더
│   ├── login.html          # 로그인 페이지
│   ├── register.html       # 회원가입 페이지
│   ├── main.html           # 메인 메모 관리 페이지
│   ├── memo_add.html       # 메모 작성 페이지
│   ├── memo_review.html    # 메모 상세보기 페이지
│   ├── profile.html        # 프로필 페이지
│   ├── profile_edit.html   # 프로필 편집 페이지
│   ├── reminder.html       # 복습 알림 페이지
│   └── lounge.html         # 라운지 페이지
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
- OpenAI API 연동

**🎨 Frontend (templates/)**

- `login.html`, `register.html`: 사용자 인증
- `main.html`: 메모 목록 및 관리 인터페이스
- `memo_add.html`, `memo_review.html`: 메모 작성 및 상세보기
- `profile.html`, `profile_edit.html`: 사용자 프로필 관리
- `reminder.html`: 복습 알림 시스템
- `lounge.html`: 커뮤니티 기능

---

## 💾 데이터베이스 구조

**MongoDB Collections:**

### 📝 memos (메모)

```javascript
{
  _id: ObjectId,
  title: String,           // 메모 제목
  content: String,         // 메모 내용
  user_id: String,         // 작성자 ID
  tags: [String],          // 태그 배열
  share: Boolean,          // 라운지 공유 여부
  repeat_visible: Boolean, // 복습 알림 표시 여부
  created_at: Date         // 작성일시
}
```

### 👤 users (사용자)

```javascript
{
  _id: ObjectId,
  user_id: String,         // 로그인 ID
  user_name: String,       // 사용자 이름
  user_email: String,      // 이메일
  user_pw: String          // 암호화된 비밀번호
}
```

### 💬 comments (댓글)

```javascript
{
  _id: ObjectId,
  memo_id: ObjectId,       // 메모 ID (참조)
  user_id: String,         // 댓글 작성자 ID
  user_name: String,       // 댓글 작성자 이름
  content: String,         // 댓글 내용
  created_at: Date         // 작성일시
}
```

---

## 📋 주요 API

| 엔드포인트               | 메서드   | 설명                         |
| ------------------------ | -------- | ---------------------------- |
| `/`                      | GET      | 루트 (로그인으로 리다이렉트) |
| `/login`                 | GET/POST | 로그인                       |
| `/logout`                | POST     | 로그아웃                     |
| `/make`                  | GET      | 회원가입 페이지              |
| `/register`              | POST     | 회원가입 처리                |
| `/main`                  | GET      | 메모 목록                    |
| `/memo_add`              | GET/POST | 메모 작성                    |
| `/memo/<id>`             | GET      | 메모 상세보기                |
| `/memo/<id>`             | DELETE   | 메모 삭제                    |
| `/reminder`              | GET      | 복습 알림                    |
| `/hide_memo`             | POST     | 복습 알림 숨기기             |
| `/profile`               | GET      | 프로필 보기                  |
| `/profile_edit`          | GET/POST | 프로필 편집                  |
| `/lounge`                | GET      | 라운지                       |
| `/memo/share`            | POST     | 메모 공유                    |
| `/memo/unshare`          | POST     | 메모 공유 해제               |
| `/comments`              | POST     | 댓글 작성                    |
| `/comments/<memo_id>`    | GET      | 댓글 조회                    |
| `/comments/<comment_id>` | DELETE   | 댓글 삭제                    |
| `/chat`                  | POST     | AI 챗봇                      |
| `/refresh`               | POST     | JWT 토큰 갱신                |

---
## 구현 화면

### 로그인 화면

<img width="1907" height="1012" alt="image" src="https://github.com/user-attachments/assets/628df312-c435-4f8a-9323-a20dd3eb03ff" />

### 메인 화면 (메모 관리 화면)

<img width="1912" height="1013" alt="image" src="https://github.com/user-attachments/assets/0f62e9f2-5d56-4242-a1d0-f1367b7c87f7" />

### 복습 알림 화면

<img width="1913" height="922" alt="image" src="https://github.com/user-attachments/assets/5616415c-edc3-4c90-a7cd-48c2eed84e46" />

### 라운지 화면

<img width="1908" height="919" alt="image" src="https://github.com/user-attachments/assets/83020c21-933c-4bf6-8fc7-3523e1641c89" />

### 사용자 정보

<img width="1914" height="922" alt="image" src="https://github.com/user-attachments/assets/08d2b6d2-c45b-4409-a3f5-6162ae29409f" />

<img width="1896" height="912" alt="image" src="https://github.com/user-attachments/assets/9339e2d3-a565-48b6-881d-57a10b72870f" />

---

## 🔧 개발 환경

- **Python**: 3.8+
- **MongoDB**: 4.0+
- **브라우저**: Chrome, Firefox, Safari

---

## 🤝 회고록

진솔 : https://velog.io/@imwe25/%ED%81%AC%EB%9E%98%ED%94%84%ED%86%A4-%EC%A0%95%EA%B8%80-10%EA%B8%B0-0%EC%A3%BC%EC%B0%A8-%ED%9A%8C%EA%B3%A0
