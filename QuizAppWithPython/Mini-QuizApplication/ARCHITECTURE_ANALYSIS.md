# Mini Quiz Application - Phân Tích Tổng Thể Dự Án

## 📋 Mục Lục
1. [Tổng Quan Kiến Trúc](#tổng-quan-kiến-trúc)
2. [Tech Stack](#tech-stack)
3. [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
4. [Mô Hình Dữ Liệu](#mô-hình-dữ-liệu)
5. [Luồng Hoạt Động](#luồng-hoạt-động)
6. [Component Chi Tiết](#component-chi-tiết)

---

## 🏗️ Tổng Quan Kiến Trúc

```
┌─────────────────────────────────────────────────────────────────┐
│                     DESKTOP APP (Kivy/KivyMD)                   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              UI Layer (KV Files + Screens)               │   │
│  │  • Login/Register  • Student/Teacher Home                │   │
│  │  • Quiz Create/Play • Class Management • Chatbot         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Business Logic Layer (Services)                │   │
│  │  • auth_services  • quiz_services  • class_services      │   │
│  │  • chatbot_service                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            Data Access Layer (Collections)               │   │
│  │  • USERS  • QUIZZES  • QUESTIONS  • OPTIONS  • RESULTS   │   │
│  │  • CLASSES  • CLASS_STUDENTS                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    MongoDB Database (Local)                      │
│              URI: mongodb://localhost:27017                       │
│              Database: MiniQuizApp                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
          ┌─────────────────────────────────────┐
          │    Optional: OpenAI ChatGPT API     │
          │ (for Chatbot feature fallback)      │
          └─────────────────────────────────────┘
```

---

## 💻 Tech Stack

### Frontend
- **Framework**: Kivy 2.3.1 + KivyMD 1.2.0 (Desktop GUI)
- **Language**: Python 3.13
- **UI Components**: MDDataTable, Button, TextInput, TabbedPanel, ScrollView

### Backend / Services
- **Database**: MongoDB (local, configurable via URI)
- **ORM/Driver**: PyMongo
- **Authentication**: SHA256 password hashing (⚠️ vulnerable, should use bcrypt)
- **Optional AI**: OpenAI (gpt-3.5-turbo via `openai` package)

### Dependencies
```
kivy==2.3.1
kivymd==1.2.0
pymongo
python-dotenv
dnspython
openai (optional)
```

---

## 📁 Cấu Trúc Dự Án

```
Mini-QuizApplication/
├── main.py                          # Entry point - khởi tạo app + screens
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── databases/
│   │   ├── db_connection.py        # MongoDB connection setup
│   │   ├── collections.py          # Collection references (USERS, QUIZZES, etc.)
│   │   └── schema.py               # Document schemas with ObjectId conversion
│   ├── services/
│   │   ├── auth_services.py        # login_user(), register_user(), change_password()
│   │   ├── quiz_services.py        # create_quiz(), list_quizzes_by_user(), save_quiz_result()
│   │   ├── class_services.py       # create_class(), add_student_to_class(), list_classes_by_student()
│   │   └── chatbot_service.py      # ask() with OpenAI fallback + rule-based Q&A
│   ├── screens/
│   │   ├── login.py                # LoginScreen (do_login → routing to student/teacher home)
│   │   ├── register.py             # RegisterScreen (registration flow)
│   │   ├── register_student.py    
│   │   ├── register_teacher.py    
│   │   ├── student_home.py        # StudentHomeScreen (3 tabs: Home, Classes, History)
│   │   ├── teacher_home.py        # TeacherHomeScreen (Quiz & Class management)
│   │   ├── quiz_create.py         # QuizCreateScreen (create quiz + add questions)
│   │   ├── quiz_player.py         # QuizPlayerScreen (take quiz, submit)
│   │   ├── result.py              # ResultScreen (show score)
│   │   ├── change_password.py     # ChangePasswordScreen
│   │   ├── class_create.py        # ClassCreateScreen (teacher creates class)
│   │   ├── class_details.py       # ClassDetailsScreen (view students in class)
│   │   ├── class_list.py          # (reserved for future)
│   │   ├── quiz_history.py        # (reserved for future)
│   │   └── chatbot.py             # ChatbotScreen (AI assistant + rule-based responses)
│   └── kv/
│       ├── login.kv
│       ├── register.kv
│       ├── register_student.kv
│       ├── register_teacher.kv
│       ├── student_home.kv        # 3 tabs + top bar with buttons
│       ├── teacher_home.kv        # Quiz list + Class list tabs
│       ├── quiz_create.kv
│       ├── quiz_player.kv
│       ├── result.kv
│       ├── change_password.kv
│       ├── class_create.kv
│       ├── class_details.kv
│       ├── class_list.kv
│       ├── quiz_history.kv
│       └── chatbot.kv             # Chat UI (messages + input)
```

---

## 🗂️ Mô Hình Dữ Liệu (MongoDB)

### Collection: `users`
```json
{
  "_id": ObjectId,
  "username": "string (unique)",
  "password": "sha256_hash",
  "role": "student | teacher",
  "fullname": "string",
  "dob": "string (DD/MM/YYYY)",
  "id": "string (student ID or teacher ID)",
  "address": "string",
  "major": "string (for student)",
  "subject": "string (for teacher)",
  "degree": "string (for teacher)"
}
```

### Collection: `quizzes`
```json
{
  "_id": ObjectId,
  "user_id": ObjectId (teacher who created),
  "title": "string",
  "description": "string",
  "duration": "int (minutes)",
  "created_at": "datetime"
}
```

### Collection: `questions`
```json
{
  "_id": ObjectId,
  "quiz_id": ObjectId,
  "question_title": "string",
  "correct_answer": "string"
}
```

### Collection: `options`
```json
{
  "_id": ObjectId,
  "question_id": ObjectId,
  "text": "string",
  "display_order": "int"
}
```

### Collection: `results`
```json
{
  "_id": ObjectId,
  "user_id": ObjectId (student),
  "quiz_id": ObjectId,
  "score": "string (e.g., '10.0/10')",
  "submitted_at": "datetime"
}
```

### Collection: `classes`
```json
{
  "_id": ObjectId,
  "teacher_id": ObjectId,
  "class_name": "string",
  "description": "string",
  "created_at": "datetime"
}
```

### Collection: `class_students`
```json
{
  "_id": ObjectId,
  "class_id": ObjectId,
  "student_id": ObjectId,
  "enrolled_at": "datetime"
}
```

---

## 🔄 Luồng Hoạt Động Chính

### 1. 🔐 Luồng Đăng Nhập / Đăng Ký

```
[User] → Login Screen
         ↓ input: username, password
         ↓ call: login_user(username, password)
         ↓ find user in USERS collection
         ↓ SHA256(password) == stored hash?
         ├─ YES → app.user = {_id, username, role}
         │        if role == "student" → StudentHomeScreen
         │        if role == "teacher" → TeacherHomeScreen
         └─ NO  → show error "Invalid credentials"

[User] → Register Screen → choose role
         ├─ Student Path → RegisterStudentScreen (input profile: fullname, dob, id, major, address)
         │                 ↓ call: register_user(username, password, "student", profile)
         │                 ↓ insert into USERS
         │                 ↓ show success → redirect to Login
         └─ Teacher Path → RegisterTeacherScreen (input: fullname, subject, degree, address)
                           ↓ call: register_user(username, password, "teacher", profile)
                           ↓ insert into USERS
                           ↓ show success → redirect to Login
```

### 2. 📚 Luồng Student

```
[Student] → Student Home Screen (3 Tabs)
            ├─ Tab 1: Home
            │   ├─ Input Quiz ID → start_quiz_by_id()
            │   │  ├─ quiz_player_screen.quiz_id = ID
            │   │  └─ navigate to QuizPlayerScreen
            │   └─ Input Class ID → join_class()
            │      ├─ call: class_services.add_student_to_class(class_id, student_id)
            │      ├─ insert into CLASS_STUDENTS
            │      └─ auto refresh Classes list
            ├─ Tab 2: Lớp Học Của Tôi
            │   ├─ on_enter() → call load_my_classes()
            │   ├─ aggregation pipeline:
            │   │   match student_id → lookup classes → unwind → replaceRoot
            │   ├─ display MDDataTable with pagination
            │   └─ no click action (info only)
            └─ Tab 3: Lịch Sử
                ├─ on_enter() → call load_history()
                ├─ call: get_results_by_user(student_id)
                ├─ lookup quiz titles
                └─ display MDDataTable: Quiz Name | Score | Date

[Student] → Quiz Player Screen
            ├─ load_quiz_details(quiz_id) → fetch questions + options
            ├─ display question with radio buttons for answers
            ├─ on Submit:
            │  ├─ calculate score (correct_answer == user_answer)
            │  ├─ call: save_quiz_result(student_id, quiz_id, score)
            │  ├─ insert into RESULTS collection
            │  └─ navigate to ResultScreen
            └─ ResultScreen: display score

[Student] → Chatbot Screen (Optional)
            ├─ send_message()
            │  ├─ display user message
            │  ├─ spawn background thread:
            │  │   call: chatbot_service.ask(prompt)
            │  │   ├─ if OPENAI_API_KEY set:
            │  │   │    use OpenAI ChatCompletion API
            │  │   └─ else:
            │  │        use rule-based Q&A (greetings, quiz help, login help)
            │  └─ display bot response
            └─ go_back() → return to student_home
```

### 3. 👨‍🏫 Luồng Teacher

```
[Teacher] → Teacher Home Screen (2 Tabs)
            ├─ Tab 1: Danh Sách Quiz
            │   ├─ on_enter() → call load_quiz_library()
            │   ├─ call: list_quizzes_by_user(teacher_id)
            │   ├─ display MDDataTable with rows:
            │   │   Quiz Name | Description | Created Date
            │   ├─ on_row_click → on_quiz_row_press(row_index)
            │   │   ├─ popup menu: Copy ID | Edit | Delete
            │   │   └─ Copy ID: copy quiz_id to clipboard
            │   │   └─ Edit: navigate to quiz_create with quiz_id
            │   │   └─ Delete: confirm + delete from QUIZZES + QUESTIONS + OPTIONS + RESULTS
            │   └─ Button "Tạo Quiz" → navigate to QuizCreateScreen
            └─ Tab 2: Danh Sách Lớp Học
                ├─ on_enter() → call load_classes()
                ├─ call: list_classes_by_teacher(teacher_id)
                ├─ display MDDataTable with rows:
                │   Class Name | Description | Created Date
                ├─ on_row_click → on_class_row_press(row_index)
                │   └─ navigate to ClassDetailsScreen(class_id)
                └─ Button "Tạo Lớp" → navigate to ClassCreateScreen

[Teacher] → Quiz Create Screen
            ├─ Input: Quiz Title, Description, Duration
            ├─ Add Questions:
            │   ├─ Question Title
            │   ├─ Correct Answer
            │   └─ Options (text, display order)
            ├─ on Submit:
            │   ├─ call: create_quiz(teacher_id, title, description, duration)
            │   │   ├─ insert into QUIZZES
            │   │   └─ return quiz_id
            │   ├─ for each question:
            │   │   ├─ call: add_question(quiz_id, title, correct_answer, options)
            │   │   ├─ insert into QUESTIONS
            │   │   └─ insert options into OPTIONS
            │   └─ redirect to teacher_home
            └─ Cancel → back to teacher_home

[Teacher] → Class Create Screen
            ├─ Input: Class Name, Description
            ├─ on Submit:
            │   ├─ call: create_class(teacher_id, class_name, description)
            │   ├─ insert into CLASSES
            │   └─ redirect to teacher_home
            └─ Cancel → back to teacher_home

[Teacher] → Class Details Screen (classid)
            ├─ load_class_details(class_id)
            ├─ display:
            │   ├─ Class Name, Teacher Name, Description
            │   └─ MDDataTable: Student List (Name | Username | Enrolled Date)
            └─ Students enrolled from CLASS_STUDENTS collection
```

### 4. 🤖 Luồng Chatbot

```
[User] (Student or Teacher) → click "Trợ lý" button
                              ↓
                              ChatbotScreen
                              ├─ on_enter()
                              │   └─ clear messages container
                              └─ send_message()
                                  ├─ user input
                                  ├─ add user message to UI
                                  ├─ spawn background thread:
                                  │   call: chatbot_service.ask(prompt)
                                  │   ├─ try OpenAI API if OPENAI_API_KEY set
                                  │   │    request: ChatCompletion (gpt-3.5-turbo)
                                  │   │    response: chat response
                                  │   └─ else:
                                  │        rule-based fallback:
                                  │        ├─ "hello" → "Xin chào!"
                                  │        ├─ "quiz" → help about quiz creation
                                  │        ├─ "login" → help about login
                                  │        └─ default → "Mình chưa hiểu..."
                                  └─ display bot response in UI
```

---

## 🧩 Component Chi Tiết

### Front-End Screens

#### LoginScreen (`login.py`)
- **Chức năng**: Xác thực đăng nhập
- **Inputs**: username, password
- **Outputs**: navigate to student_home or teacher_home based on role
- **Error Handling**: Display "Sai tài khoản hoặc mật khẩu!"

#### StudentHomeScreen (`student_home.py`)
- **Tab 1 (Trang Chủ)**: 
  - Start Quiz by ID
  - Join Class by ID
- **Tab 2 (Lớp Học Của Tôi)**:
  - List classes student joined (MDDataTable with pagination)
  - load_my_classes() loads on enter
- **Tab 3 (Lịch Sử)**:
  - Quiz history (score, date)
  - load_history() loads on enter
- **Top Bar**: 
  - "Trợ lý" button → chatbot
  - "Đăng xuất" button → logout

#### TeacherHomeScreen (`teacher_home.py`)
- **Tab 1 (Danh Sách Quiz)**:
  - List teacher's quizzes (MDDataTable with pagination)
  - Row click → popup: Copy ID, Edit, Delete
  - "Tạo Quiz" button → quiz_create
- **Tab 2 (Danh Sách Lớp Học)**:
  - List teacher's classes
  - Row click → class_details screen
  - "Tạo Lớp" button → class_create

#### QuizPlayerScreen (`quiz_player.py`)
- **Flow**: 
  - Load quiz details (questions + options)
  - Display one question at a time
  - Radio buttons for answer selection
  - Submit → calculate score → save to RESULTS → show result

#### ChatbotScreen (`chatbot.py`)
- **Flow**:
  - Input message
  - Call chatbot_service.ask()
  - Display response
  - Threading to prevent UI freeze
  - go_back() → return to previous screen based on role

---

### Back-End Services

#### `auth_services.py`
- `hash_password(password)` → SHA256 hash
- `register_user(username, password, role, profile)` → insert USERS
- `login_user(username, password)` → verify + return user dict
- `change_password(user_id, old_password, new_password)` → update USERS

#### `quiz_services.py`
- `create_quiz(user_id, title, description, duration)` → insert QUIZZES
- `add_question(quiz_id, question_title, correct_answer, options)` → insert QUESTIONS + OPTIONS
- `list_quizzes_by_user(user_id)` → query QUIZZES
- `delete_quiz(quiz_id)` → delete from QUIZZES, QUESTIONS, OPTIONS
- `get_quiz_details(quiz_id)` → fetch full quiz with questions + options
- `get_results_by_user(user_id)` → lookup RESULTS + QUIZZES
- `save_quiz_result(user_id, quiz_id, score)` → insert RESULTS

#### `class_services.py`
- `create_class(teacher_id, class_name, description)` → insert CLASSES
- `list_classes_by_teacher(teacher_id)` → query CLASSES
- `list_classes_by_student(student_id)` → aggregation: CLASS_STUDENTS → CLASSES
- `add_student_to_class(class_id, student_id)` → insert CLASS_STUDENTS
- `list_students_in_class(class_id)` → aggregation: CLASS_STUDENTS → USERS
- `get_class_details(class_id)` → fetch class info

#### `chatbot_service.py`
- `ask(prompt)` → try OpenAI else rule-based
- `_rule_based_answer(prompt)` → dictionary lookup for common queries
- Fallback: "Mình chưa hiểu... Hãy set OPENAI_API_KEY"

---

## 🔌 Database Access Layer (`collections.py`)

```python
USERS = db["users"]
QUIZZES = db["quizzes"]
QUESTIONS = db["questions"]
OPTIONS = db["options"]
RESULTS = db["results"]
CLASSES = db["classes"]
CLASS_STUDENTS = db["class_students"]
```

---

## ⚙️ App Initialization (main.py)

1. **Window Setup**: `Window.maximize()`
2. **Load KV Files**: All 15+ KV files loaded sequentially
3. **Create ScreenManager**: Single screen manager with all screens registered
4. **Run App**: `QuizApp().run()` starts Kivy event loop

---

## 🔐 Security Issues Identified

| Issue | Severity | Impact | Fix |
|-------|----------|--------|-----|
| SHA256 password (not salted) | ⚠️ High | Vulnerable to rainbow tables | Use bcrypt with salt |
| No input validation | ⚠️ High | SQL/NoSQL injection risk | Validate all inputs |
| API key in code (optional) | ⚠️ Medium | Exposed if committed | Use `.env` file |
| No HTTPS (local) | ✅ Low | OK for local only | N/A |

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│ USER INTERACTIONS (KV + Screen Python)                              │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ SCREEN LOGIC (validate, transform, call services)                   │
│ e.g., login.py → calls auth_services.login_user()                  │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ SERVICE LAYER (business logic, aggregations, queries)               │
│ e.g., auth_services.login_user() → USERS.find_one()               │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│ MONGODB OPERATIONS (CRUD, aggregation pipeline)                     │
│ Collections: USERS, QUIZZES, QUESTIONS, OPTIONS, RESULTS, etc.     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📌 Key Features

✅ **Implemented**
- User authentication (login/register with role-based routing)
- Quiz creation with multiple-choice questions
- Quiz taking with scoring
- Class management (teacher creates, student joins)
- Quiz history tracking
- Chatbot with OpenAI + rule-based fallback
- Responsive UI with MDDataTable + pagination
- Screen transitions + navigation

⚠️ **Partially Implemented**
- MDDataTable row click handling (index mismatch on pagination)
- Chatbot bubble-style UI (plain text currently)

❌ **Not Yet Implemented**
- Real-time updates
- File uploads (for class materials)
- Quiz sharing between teachers
- Student notifications

---

## 🚀 Deployment Notes

- **Local**: MongoDB must be running (`mongod` on localhost:27017)
- **Production**: Change MongoDB URI to Atlas/managed service
- **Optional**: Set `OPENAI_API_KEY` environment variable for AI features

---

## 📝 Development Workflow

1. **Add Feature**: Create screen + KV + service
2. **Database**: Schema defined in `schema.py`, collection in `collections.py`
3. **Testing**: Run `main.py`, navigate screens, check MongoDB
4. **Debug**: Print statements in services, check console logs

