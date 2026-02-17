<!-- ========================= HEADER ========================= -->

<div align="center">
  
![Header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=280&section=header&text=Amit%20Tiwari&fontSize=70&fontColor=ffffff&animation=twinkling&fontAlignY=38&desc=Full%20Stack%20Developer%20%7C%20SDE%20%7C%20DevOps%20Practitioner&descSize=20&descAlignY=60)

</div>

---

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/amit-tiwari-cs)
[![GitHub](https://img.shields.io/badge/GitHub-171515?style=for-the-badge&logo=github)](https://github.com/AmiTtiwari43)
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode)](https://leetcode.com/u/AmitTiwari27/)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail)](mailto:amit.tiwari2914@gmail.com)

</div>

---

# 👨‍💻 About Me

<div align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=AmiTtiwari43&theme=tokyonight&no-bg=true&no-frame=true&margin-w=15" alt="trophies" />
</div>

```yaml
Name: Amit Tiwari
Location: Punjab, India
Role: Full Stack Developer (MERN)
Education: B.Tech CSE | CGPA 7.9
Certifications:
  - Oracle OCI DevOps Professional (2025)
  - Oracle OCI Foundations Associate (2025)
Achievements:
  - 550+ LeetCode Problems
  - 150+ Day Coding Streak
```

I design secure, scalable, production-grade systems with performance and architecture clarity.

## 🛠️ Tech Stack

<div align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=react,nextjs,tailwind,nodejs,express,flask,mongodb,postgres,redis,docker,kubernetes,jenkins,githubactions,aws,gcp,js,ts,python,java,cpp&perline=10" />
  </a>
</div>

## 💼 Experience

### Full Stack Developer Intern
**NYERAS Edu-tech & Innovations Pvt. Ltd.**
- 🚀 Reduced API latency by 75% | ⚡ Improved response time by 73%
- 🤖 Automated 90% manual workflows | 🔐 Built 40+ secure REST APIs
- 📦 Designed MVC-based 3-tier architecture

## 🏗️ Featured Projects

<div align="center">

| 🏥 DocVerse | 🎟️ EventEase Lite | 🤖 AI Therapy Assistant |
| :--- | :--- | :--- |
| OWASP Top-10 Secure | 9-State Lifecycle | CBT-Structured |
| Sub-50ms Queries | Zero Double Bookings | Context-Aware |

</div>

<br/>

## 🏗️ Architecture & Technical Deep-Dive

I design systems that balance performance, security, and scalability. Below is a unified view of the architecture used in my high-scale platforms like **EventEase Lite** and **Doctor Management System**.

### 🛠️ Core System Design
```mermaid
graph TD
    subgraph "Frontend Layer"
        Client["React 19 + Vite"] -- "Axios / REST" --> Proxy[Nginx / Vercel]
    end

    subgraph "Logic & Security Layer"
        Proxy --> Auth["JWT & RBAC Middleware"]
        Auth --> API["Node.js Express Stateless API"]
    end

    subgraph "Payment & Notifications"
        API --> UPI["UPI QR Code Integration"]
        API --> Mail["SendGrid / Nodemailer"]
        API --> AI["AI Health Assistant (NLP)"]
    end

    subgraph "Persistence & Performance"
        API --> Cache["Redis Caching"]
        API --> DB[("MongoDB Cluster + Mongoose")]
        DB -.-> Replicas["Primary + Replicas"]
    end

    style UPI fill:#f9f,stroke:#333,stroke-width:2px
    style AI fill:#bbf,stroke:#333,stroke-width:2px
```

### 🔑 Key Implementation Patterns

#### 1️⃣ Financial & Lifecycle Logic (EventEase Lite)
- **UPI QR Code Flow**: Integrated dynamic QR generation for post-confirmation payments.
- **Refund Management**: Implemented a state-machine based refund lifecycle (Requested → Processing → Success) with real-time status updates.
- **Concurrency Control**: Used MongoDB atomic transactions to guarantee **zero double-bookings** across 10K+ concurrent users.

#### 2️⃣ Healthcare Intelligence (Doctor Management)
- **AI Triage Integration**: AI-driven health assistant to provide initial recommendations.
- **Secure Healthcare Records**: Enforced strict RBAC using JWT to separate Patient, Doctor, and Admin access levels.
- **Micro-Optimizations**: achieved **sub-50ms query response** times using compound indexing and Redis caching.

#### 3️⃣ Production-Grade Security
- **OWASP Compliance**: Protected against SQLi, NoSQLi, and XSS.
- **Session Security**: HttpOnly cookies for JWT storage with refresh token rotation.
- **Robustness**: Implemented exponential backoff for external API retries (SendGrid) and centralized error handling for consistency.

#### 4️⃣ Scalability Strategy
- **Stateless Architecture**: Horizontal scaling via Dockerized Node.js containers orchestrated by Kubernetes.
- **Data Integrity**: MongoDB replica sets ensure 99.9% availability and fault tolerance.
- **Optimized UI**: 35% reduction in React re-renders via memoization and efficient state management.

<br/>

## 🔄 Workflow Deep-Dives

Detailed mapping of core business logic and data movement across my major platforms.

### 📅 Secure Appointment & Payment Pipeline (DocVerse)
Visualizing the multi-stage handshake between the client, authentication layer, and secure persistence.

```mermaid
sequenceDiagram
    participant User as Patient (React)
    participant Auth as Auth Middleware (JWT)
    participant API as Booking Controller (Express)
    participant DB as MongoDB (Mongoose)
    participant Pay as UPI Provider
    
    User->>API: 1. Request Slot (SlotID, DoctorID)
    API->>DB: 2. Verify Availability (Atomic Check)
    DB-->>API: Slot Available
    API-->>User: 3. Return Payment QR
    User->>Pay: 4. Scan & Transact
    Pay-->>User: Success
    User->>Auth: 5. Submit TransactionID (JWT Token)
    Auth->>API: Validated Session
    API->>DB: 6. Persist Appointment (Status: Confirmed)
    DB-->>API: Saved
    API-->>User: 7. Digital Receipt & Confirmation
```

### 🧠 End-to-End AI Health Triage (AIChatWidget)
Demonstrating the data flow from symptom analysis to professional discovery.

```mermaid
graph TD
    A[User Symptom Input] --> B{NLP Analysis Engine}
    B -->|Symptom Extraction| C[Context Awareness Layer]
    C -->|Pattern Matching| D[AI Recommendation Engine]
    D -->|Specialization Mapping| E[Specific Medical Category]
    E --> F[Mongoose Aggregation Query]
    F --> G[Filtered Doctor Discovery]
    G --> H[Patient Booking Interface]

    subgraph "Logic Layer"
        B
        C
        D
    end
    
    subgraph "Persistence"
        F
    end

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#f96,stroke:#333,stroke-width:2px
```

---

## 📊 GitHub Analytics

<div align="center">
  <table border="0">
    <tr>
      <td width="550">
        <img src="https://github-readme-stats.vercel.app/api?username=AmiTtiwari43&show_icons=true&theme=tokyonight&hide_border=true" height="170"/>
      </td>
      <td width="400">
        <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=AmiTtiwari43&layout=compact&theme=tokyonight&hide_border=true" height="170"/>
      </td>
    </tr>
  </table>
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=AmiTtiwari43&theme=tokyonight&hide_border=true" width="80%"/>
</div>

<br/>

| 📈 Visitor Heatmap |
| :--- |
| <img src="https://github-readme-activity-graph.vercel.app/graph?username=AmiTtiwari43&theme=tokyo-night&hide_border=true&area=true" width="100%"/> |

<br/>

| 🐍 Contribution Snake |
| :--- |
| <picture> <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmiTtiwari43/AmiTtiwari43/output/github-snake-dark.svg" /> <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/AmiTtiwari43/AmiTtiwari43/output/github-snake.svg" /> <img alt="github contribution snake" src="https://raw.githubusercontent.com/AmiTtiwari43/AmiTtiwari43/output/github-snake-dark.svg" width="100%"> </picture> |

<br/>

| ⏱ WakaTime Coding Stats |
| :--- |
| <img src="https://github-readme-stats.vercel.app/api/wakatime?username=AmiTtiwari43&theme=tokyonight&hide_border=true" width="100%"/> |

<br/>

## 🏆 Competitive Programming
<div align="center">

| LeetCode | HackerRank | Focus Areas |
| :--- | :--- | :--- |
| 550+ Solved | 4★ Java | Arrays, Graphs, DP |
| 150+ Day Streak | Gold Badge | Trees, Strings |

</div>

<br/>

## 🎓 Education & Connect
<div align="center">

| 🎓 Education | 🌐 Connect |
| :--- | :--- |
| **Lovely Professional University** | 📧 [Email](mailto:amit.tiwari2914@gmail.com) |
| B.Tech – CSE (7.9 CGPA) | 💼 [LinkedIn](https://linkedin.com/in/amit-tiwari-cs) |
| Punjab, India | 🧠 [LeetCode](https://leetcode.com/u/AmitTiwari27/) |

</div>

---

<div align="center">

"I engineer systems that survive production."

</div>
