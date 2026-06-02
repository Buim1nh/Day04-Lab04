# OrderDesk Prompt Engineering Lab

Build an LLM order agent for an electronics retailer and improve its score through prompt engineering.

In this lab, the agent must:

- understand Vietnamese and mixed-language order requests
- use tools in the right order
- ask for missing information before acting
- refuse unsafe or policy-breaking requests
- save the final order as grounded JSON

The main goal is not just to make the code run. The goal is to improve agent behavior by tightening the prompt, tool schema, and guardrails.

## What You Will Practice

- writing a stronger system prompt
- designing clearer tool schemas
- forcing clarification before tool use
- adding guardrails for unsafe requests
- grounding final answers in tool results
- debugging failures from tool traces and saved artifacts

## Repository Map

- `src/`: your implementation
- `simple_solution/`: weak baseline
- `data/products.json`: product catalog
- `data/graded_cases.json`: graded scenarios
- `data/expected_orders/`: expected saved JSON for save cases
- `grade/scoring.py`: grader
- `guide.md`: step-by-step workflow
- `rubric.md`: grading rules

## Recommended Workflow

1. Run the weak baseline first.
2. Record its score.
3. Improve `src/`.
4. Run the grader on `src/`.
5. Repeat until your score clearly beats the baseline.

## Setup

Create a `.env` file:

```bash
GOOGLE_API_KEY=...
LLM_MODEL=gemini-2.5-flash
```

Optional local model:

```bash
OLLAMA_MODEL=qwen3.5:3b
OLLAMA_BASE_URL=http://localhost:11434
```

## Commands

Run the weak baseline:

```bash
python grade/scoring.py --module simple_solution.agent.graph --provider google
```

Run your implementation:

```bash
python grade/scoring.py --module src.agent.graph --provider google
```

Run tests:

```bash
pytest -q
```

## What A Strong Submission Does

- clarifies before tool use when required fields are missing
- refuses invalid requests without calling tools
- follows the expected tool sequence on valid orders
- saves the correct JSON artifact
- gives a concise grounded answer in Vietnamese

Read [guide.md](file:///e:/CongViec/Tài%20liệu%20phỏng%20vấn%20Game%20des/AI20K/Day04/Day04-Lab04/guide.md) trước khi chỉnh sửa `src/`.

---

## 🖥️ Giao diện Kiểm thử Trực quan (Interactive UI Dashboard)

Chúng tôi đã phát triển một giao diện Dashboard cực kỳ hiện đại và trực quan dành riêng cho bài Lab 04 này. Giao diện giúp bạn:
- **Chọn nhanh**: Click chọn nhanh bất kỳ kịch bản nào trong số 13 test cases có sẵn.
- **Tùy biến câu hỏi**: Tự viết các truy vấn mua hàng tự do để kiểm chứng Agent.
- **System Prompt**: Hiển thị chi tiết System Prompt hiện tại của Agent.
- **Sơ đồ chuỗi gọi tool**: Bản đồ timeline các bước thực thi (list -> detail -> discount -> total -> save) sáng đèn trực quan thời gian thực.
- **Trace chi tiết**: Phân tích sâu tham số đầu vào (arguments) và kết quả trả về (outputs) của từng công cụ.
- **Grounded Verification**: Bảng tự động kiểm chứng an toàn dữ liệu, tính tuân thủ quy định hết hàng/mạo danh và tương thích POSIX path.

### 🚀 Cách khởi chạy giao diện:

```bash
uv run python ui_server.py
```

Sau khi chạy lệnh trên, bạn hãy mở trình duyệt và truy cập: **[http://127.0.0.1:8888](http://127.0.0.1:8888)**

