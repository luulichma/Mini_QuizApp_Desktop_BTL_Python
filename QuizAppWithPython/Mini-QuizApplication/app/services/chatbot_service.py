import os
from typing import Optional

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Try to import openai if available
try:
    import openai
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
    _OPENAI_AVAILABLE = True
except Exception:
    openai = None
    _OPENAI_AVAILABLE = False


def _rule_based_answer(prompt: str) -> str:
    """Simple fallback rule-based chatbot responses."""
    p = prompt.strip().lower()
    if any(g in p for g in ("hello", "hi", "chào", "xin chào")):
        return "Chào bạn! Mình là trợ lý của Quiz App. Bạn cần giúp gì?"
    if "how" in p and "create" in p or "tạo" in p:
        return "Để tạo quiz: vào tab 'Tạo Quiz' trong giao diện giáo viên, điền tiêu đề, thời gian, và thêm câu hỏi."
    if "login" in p or "đăng nhập" in p:
        return "Nếu bạn gặp lỗi đăng nhập, kiểm tra username/password, hoặc thử reset mật khẩu."
    if "quiz" in p and "id" in p:
        return "Bạn có thể sao chép ID quiz từ thư viện quiz (Teacher) và chia sẻ cho học sinh."
    return "Mình chưa hiểu. Bạn nói rõ hơn được không? (hoặc bật OPENAI_API_KEY để dùng chatbot thông minh hơn)"


async def _openai_chat(prompt: str) -> Optional[str]:
    try:
        # use Chat Completions API
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.6,
        )
        text = resp.choices[0].message.content.strip()
        return text
    except Exception:
        return None


def ask(prompt: str) -> str:
    """Ask the chatbot. If OpenAI key available and package installed, use it. Otherwise return rule-based answer."""
    if _OPENAI_AVAILABLE and OPENAI_API_KEY and openai is not None:
        try:
            # Try synchronous call (OpenAI python lib is sync)
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.6,
            )
            text = resp.choices[0].message.content.strip()
            return text
        except Exception:
            # fallback
            return _rule_based_answer(prompt)
    else:
        return _rule_based_answer(prompt)
