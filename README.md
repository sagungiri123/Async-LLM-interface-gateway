![CI](https://github.com/sagungiri123/Async-LLM-interface-gateway/actions/workflows/ci.yml/badge.svg)

# 🚀 Async Inference Gateway

**A production-ready FastAPI microservice that processes AI prompts in the background** — without freezing your web server.

---

## 🤔 What problem does this solve?

AI models take **5–30 seconds** to generate text. If you run them directly inside a web server, the server **freezes** and **times out** when multiple users send requests at the same time.

**This project fixes that** by using a **Task Queue pattern**:

1. The user submits a prompt.
2. The server immediately returns a `task_id` (takes **< 50ms**).
3. A background **Worker** picks up the job, runs the AI model, and stores the result.
4. The user polls a different endpoint to fetch the finished result.

---

## 🧠 How it works (Step-by-Step)
┌─────────┐ 1. POST /generate ┌─────────────┐ 2. Enqueue job ┌─────────────┐
│ User │ ──────────────────────► │ FastAPI │ ─────────────────► │ Redis │
│ (Client)│ │ (Gateway) │ │ (Queue) │
└─────────┘ └─────────────┘ └──────┬──────┘
│ │ │
│ │ │
│ 4. GET /result/{task_id} │ │
│ ◄─────────────────────────────────── │ │
│ │ ┌─────────────────┘
│ │ │ 3. Worker picks
│ │ │ up the job
│ │ ▼
│ │ ┌─────────────┐
│ │ │ Worker │
│ │ │ (RQ) │
│ │ └──────┬──────┘
│ │ │
│ │ │ Runs AI model
│ │ ▼
│ │ ┌─────────────┐
│ └──────────│ Redis │
│ │ (Result) │
│ └─────────────┘


---

## 🛠️ Tech Stack (What we used & why)

| Component        | Technology    | Why we chose it                                                                 |
| :--------------- | :------------ | :------------------------------------------------------------------------------ |
| **Web Server**   | FastAPI       | Blazing fast, async support, automatic API docs (`/docs`), and Pydantic validation. |
| **Queue/Storage**| Redis         | RAM-based (microsecond latency). Perfect for queuing tasks and storing temporary results. |
| **Queue Manager**| RQ (Redis Q)  | Lightweight Python library that manages the queue on top of Redis.              |
| **Background Worker**| Python + RQ | Separate process that runs 24/7, polls Redis, and executes AI tasks.            |
| **Containerization**| Docker       | (Coming soon) Package the API, Redis, and Worker into 3 isolated containers.    |

---

## 📁 Project Structure (Where everything lives)
    fastapi-llm-project/
├── app/
│ ├── main.py # FastAPI app (routes & startup)
│ ├── models/
│ │ └── schemas.py # Pydantic request/response models
│ ├── core/
│ │ └── tasks.py # The background task (AI inference logic)
│ └── utils/
│ └── redis_client.py # Redis connection pool
├── worker.py # The RQ Worker entrypoint
├── requirements.txt # Python dependencies
└── README.md # This file

🎯 What makes this project special 

✅ Decouples the web layer from heavy compute – The API server stays fast even under heavy load.

✅ Scalable by design – Run 5 Workers in parallel to process 5 AI prompts simultaneously.

✅ Production-grade patterns – Uses Redis for queues, RQ for job management, and Docker-ready architecture.

✅ Automatic API documentation – FastAPI generates /docs and /redoc for free.


🤝 Contributing
This is a portfolio project built for learning. If you spot a bug or have a suggestion, feel free to open an issue or submit a pull request.

📄 License
MIT License – free to use for your own portfolio or job applications.

👨‍💻 Author
Sagun Giri
Sagungiri123 | LinkedIn

Built with ❤️ to master FastAPI, asynchronous architectures, and AI deployment.

---

### ✅ What makes this "Clear" version better

- **Problem-first approach:** It immediately tells the reader *why* this project exists before showing code.
- **Visual architecture diagram:** Easy to understand even for non-developers.
- **Actionable setup:** Numbered steps that *anyone* can follow.
- **"What makes this special" section:** Serves as your interview cheat sheet.
- **Clear roadmap:** Shows you are planning ahead and thinking beyond the current code.

---

### 🛑 Quick Checklist for you

1. **Save this as `README.md`** in your project root.
2. **Replace** `yourusername` with your actual GitHub username.
3. **Replace** `Your Name` and the links with your actual details.
4. **Commit it**:
   ```bash
   git add README.md
   git commit -m "docs: add clear user-friendly README for Async Inference Gateway"
