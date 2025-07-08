# 🌱 정글 되새김질 노트

## 📌 프로젝트 목적

**정글 부트캠프에서 배운 내용을 반복 복습할 수 있도록 돕는**,  
**“자동 복습 알림 기능”이 포함된 개인 메모 웹 애플리케이션**입니다.

- 학습 내용을 **메모**로 작성하고
- 작성일 기준 **1일, 3일, 7일, 15일, 30일 후** 복습 알림을 제공
- 복습 주기에 따라 메모를 다시 떠올리며 **장기 기억 정착을 유도**

---

## 💡 사용 의도

- “한 번 몰입하고 나면 끝?” → **반복이 진짜 실력이다!**
- 잊혀지기 전에 적절한 시점에 다시 보도록 유도
- **정글에서 성장한 기록**을 누적하고 회고하며 실력 다지기

> ✍️ *오늘 배운 내용을 내일의 내가, 그리고 한 달 뒤의 내가 다시 마주하도록.*

---



## 🤝 GitHub 협업 절차 (한눈에 보기)

모든 팀원은 아래 절차를 **순서대로 복사해서 따라하면 됩니다.**

---

#### 1. 저장소 클론 (최초 1회만)

```bash
git clone https://github.com/JinSol-coder/jungle-note.git
cd jungle-note
```

---

#### 2. 브랜치 생성 (작업 전 항상!)

```bash
git checkout main
git pull origin main
git checkout -b feature/기능이름
```

- 예: `feature/login`, `feature/signup`
- `main` 브랜치를 기준으로 새 브랜치를 따서 작업

---

#### 3. 작업 후 커밋

```bash
git add .
git commit -m "Add: 로그인 기능 UI 구현"
```

- 커밋 메시지는 `"타입: 내용"` 형식  
- 예: `Fix: 회원가입 이메일 오류 수정`

---

#### 4. 브랜치 푸시

```bash
git push origin feature/기능이름
```

- GitHub로 코드 업로드

---

#### 5. GitHub에서 Pull Request 생성

1. GitHub 웹에 접속
2. `Compare & Pull Request` 클릭
3. 제목/설명 작성 → 리뷰 요청
4. Merge 승인되면 기능 반영 완료

---

#### 6. main 최신화 (다음 작업 전 무조건!)

```bash
git checkout main
git pull origin main
```

- 다음 작업 전에 최신 코드 받아오기

---

#### 💡 브랜치 이름 규칙

| 목적     | 예시               |
|----------|--------------------|
| 기능 개발 | `feature/login`     |
| 버그 수정 | `fix/login-error`   |
| UI 작업   | `style/navbar-ui`   |

---

#### ❗ 협업 규칙 요약

- `main` 브랜치 직접 수정 ❌
- 반드시 브랜치 → PR → Merge로 반영 ✅
- 충돌은 본인 브랜치에서 해결 후 다시 PR ✅
