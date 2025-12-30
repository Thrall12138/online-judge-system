# Online Judge System

A comprehensive, scalable online judge system designed for competitive programming challenges, coding interviews, and automated code evaluation. This system provides a robust platform for submitting, testing, and evaluating code solutions across multiple programming languages.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Supported Languages](#supported-languages)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

The Online Judge System is a full-featured platform that enables users to:
- Submit code solutions to programming problems
- Have their submissions automatically evaluated against test cases
- Receive detailed feedback on execution results
- Track submission history and progress
- Compete in coding contests and challenges

This system is designed to be highly scalable, secure, and efficient, capable of handling high volumes of submissions with quick turnaround times.

## ✨ Features

### Core Features
- **Multi-Language Support**: Execute and evaluate code in 10+ programming languages
- **Real-Time Compilation & Execution**: Instant feedback on submissions with minimal latency
- **Sandbox Environment**: Secure code execution with resource limitations to prevent abuse
- **Comprehensive Test Evaluation**: Run multiple test cases with detailed output comparison
- **Verdict System**: Clear verdict messages (Accepted, Wrong Answer, Time Limit Exceeded, Runtime Error, etc.)

### User Features
- **Problem Management**: Browse, search, and filter problems by difficulty and category
- **Submission History**: Track all submissions with timestamps and results
- **Leaderboards**: Global and contest-specific rankings
- **Discussion Forum**: Community interaction around problems and solutions
- **Progress Tracking**: Visual representation of problem-solving progress

### Admin Features
- **Problem Creation**: Add and manage problem sets with custom test cases
- **Contest Management**: Create, schedule, and manage coding contests
- **User Management**: Control access and permissions
- **Statistics Dashboard**: Monitor system performance and user activity
- **Advanced Analytics**: Detailed insights into submission patterns and performance metrics

## 🏗️ Architecture

The Online Judge System follows a modern, distributed architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Web UI)                        │
│              React/Vue.js - Responsive Design                │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  API Gateway / Load Balancer                  │
│                    (Request Routing)                          │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼─────┐ ┌────▼──────┐ ┌──▼────────┐
│   Auth      │ │  Problem  │ │ Contest   │
│ Service     │ │ Service   │ │ Service   │
└─────────────┘ └───────────┘ └───────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────▼────────────┐
        │   Judge Engine Service  │
        │  (Code Execution Core)  │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │  Execution Sandbox      │
        │  - Process Isolation    │
        │  - Resource Limits      │
        │  - Secure Compilation   │
        └────────────┬────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼──┐  ┌─────▼─────┐  ┌───▼──┐
   │ Cache │  │ Database  │  │ Queue │
   │ Layer │  │ (Results) │  │ (Jobs)│
   └───────┘  └───────────┘  └───────┘
```

### Components

1. **Frontend Layer**: User-facing web interface for submission and problem browsing
2. **API Gateway**: Central request handling and load balancing
3. **Microservices**:
   - **Authentication Service**: User login, registration, and session management
   - **Problem Service**: Problem management and metadata
   - **Contest Service**: Contest scheduling and management
   - **Judge Engine**: Core compilation and execution logic
4. **Execution Sandbox**: Isolated environment for secure code execution with resource constraints
5. **Data Layer**: 
   - Database for persistent storage
   - Cache layer for performance optimization
   - Job queue for asynchronous processing

## 💻 Supported Languages

The Online Judge System supports the following programming languages:

| Language | Compiler/Runtime | Version |
|----------|------------------|---------|
| C | GCC | 11.x |
| C++ | G++ | 11.x |
| Java | OpenJDK | 17 LTS |
| Python | CPython | 3.10+ |
| Python 3 | CPython | 3.11+ |
| JavaScript | Node.js | 18.x LTS |
| TypeScript | Node.js | 18.x LTS |
| Go | Go Compiler | 1.20+ |
| Rust | Rust Compiler | 1.70+ |
| PHP | PHP CLI | 8.2+ |
| Ruby | Ruby Interpreter | 3.2+ |
| C# | .NET | 7.0+ |

Each language environment is containerized with appropriate toolchains and libraries pre-installed.

## 🚀 Setup Instructions

### Prerequisites

- **Operating System**: Linux (Ubuntu 20.04+), macOS, or Windows (WSL2)
- **Docker**: 20.10+ (for containerized execution)
- **Node.js**: 16.x or higher
- **Python**: 3.8 or higher
- **Git**: 2.30+

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/Thrall12138/online-judge-system.git
cd online-judge-system
```

#### 2. Environment Setup

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Configure the following variables:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=online_judge
DB_USER=judge_user
DB_PASSWORD=secure_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# API Configuration
API_PORT=3000
API_HOST=0.0.0.0

# Judge Engine Configuration
JUDGE_PORT=5000
JUDGE_MAX_MEMORY=256MB
JUDGE_MAX_TIME=5000ms
JUDGE_MAX_PROCESSES=10

# Security
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRY=24h

# Frontend
FRONTEND_URL=http://localhost:3000
```

#### 3. Backend Setup

```bash
# Install dependencies
npm install

# or if using Python backend
pip install -r requirements.txt

# Initialize database
npm run db:migrate

# Seed initial data
npm run db:seed
```

#### 4. Docker Setup (Recommended)

```bash
# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

#### 5. Frontend Setup

```bash
cd frontend
npm install
npm start
```

#### 6. Verify Installation

```bash
# Check API health
curl http://localhost:3000/api/health

# Access the web interface
open http://localhost:3000
```

### Database Setup

The system uses PostgreSQL for persistent storage:

```bash
# Connect to PostgreSQL
psql -U judge_user -d online_judge

# Run migrations
npm run migrate
```

### Security Considerations

1. **Change default credentials** in production
2. **Use HTTPS** in production environment
3. **Configure firewall rules** to restrict access
4. **Set up SSL certificates** for encrypted communication
5. **Enable rate limiting** on API endpoints
6. **Use environment variables** for sensitive data

## 📖 Usage Guide

### For Users

#### Submitting a Solution

1. **Navigate to a Problem**
   - Browse the problem list
   - Click on a problem to view its details
   - Read the problem statement and constraints

2. **Write Your Solution**
   - Select your preferred programming language
   - Write your code in the editor
   - Use the built-in syntax highlighting

3. **Submit Your Code**
   - Click the "Submit" button
   - Your code will be compiled and tested
   - Wait for the verdict

4. **Review Results**
   - View your submission status
   - Check execution details (time, memory)
   - Analyze failed test cases if applicable

#### Viewing Submission History

```
Profile → My Submissions → Filter/Sort Results
```

### For Problem Setters

#### Creating a New Problem

1. **Access Admin Panel**
   - Navigate to `/admin/problems`
   - Click "Create New Problem"

2. **Fill Problem Details**
   - Title and slug
   - Problem statement (supports Markdown)
   - Difficulty level (Easy, Medium, Hard)
   - Time limit (seconds)
   - Memory limit (MB)
   - Tags and categories

3. **Add Test Cases**
   - Input format
   - Expected output
   - Sample/Hidden test cases

4. **Set Constraints**
   - Input/Output constraints
   - Time limit per test case
   - Memory limit

5. **Publish Problem**
   - Review all settings
   - Click "Publish"
   - Problem becomes available to users

### For Administrators

#### Contest Management

```bash
# Create a new contest
POST /api/contests
{
  "title": "Weekly Challenge #1",
  "description": "...",
  "startTime": "2025-12-31T10:00:00Z",
  "endTime": "2025-12-31T12:00:00Z",
  "problems": [1, 2, 3, 4, 5]
}

# Update contest
PUT /api/contests/:id

# Delete contest
DELETE /api/contests/:id
```

#### User Management

```bash
# Ban/Unban user
PATCH /api/users/:id/status

# Reset password
POST /api/users/:id/reset-password

# Export statistics
GET /api/analytics/export
```

## 🔌 API Documentation

### Authentication

All endpoints (except public ones) require authentication via JWT token:

```bash
# Login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password"
}

# Response
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { ... }
}
```

Include token in subsequent requests:

```bash
Authorization: Bearer <token>
```

### Core Endpoints

#### Problems

```bash
# List all problems
GET /api/problems?page=1&limit=20&difficulty=medium

# Get problem details
GET /api/problems/:id

# Get problem samples
GET /api/problems/:id/samples
```

#### Submissions

```bash
# Submit solution
POST /api/submissions
{
  "problemId": 123,
  "language": "cpp",
  "code": "..."
}

# Get submission status
GET /api/submissions/:id

# List user submissions
GET /api/submissions?userId=:id&status=accepted
```

#### Contests

```bash
# List contests
GET /api/contests?status=active

# Get contest details
GET /api/contests/:id

# Join contest
POST /api/contests/:id/join

# Get contest leaderboard
GET /api/contests/:id/leaderboard
```

### Response Format

All responses follow a standard format:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2025-12-30T06:47:18Z"
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Validation failed"
  },
  "timestamp": "2025-12-30T06:47:18Z"
}
```

## 🧪 Testing

### Unit Tests

```bash
npm run test:unit
```

### Integration Tests

```bash
npm run test:integration
```

### End-to-End Tests

```bash
npm run test:e2e
```

### Code Coverage

```bash
npm run test:coverage
```

## 📊 Performance & Scaling

- **Horizontal Scaling**: Stateless design allows multiple judge engine instances
- **Caching**: Redis caching for frequently accessed data
- **Queue System**: Asynchronous job processing for heavy computations
- **Load Balancing**: Automatic distribution of submissions across multiple workers

## 🐛 Troubleshooting

### Compilation Errors

Check language-specific compiler output in the error logs:

```bash
docker logs online-judge-judge-1
```

### Timeout Issues

- Increase `JUDGE_MAX_TIME` in `.env`
- Check for infinite loops in test code
- Verify input size matches constraints

### Memory Issues

- Adjust `JUDGE_MAX_MEMORY` setting
- Profile your solution locally
- Optimize data structures

### Database Connection Errors

```bash
# Verify PostgreSQL is running
psql -U judge_user -d online_judge -c "SELECT 1"

# Check connection string in .env
```

## 📝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please ensure:
- Code follows the project style guide
- Tests pass: `npm run test`
- Documentation is updated
- Commits have clear messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For issues, questions, or suggestions:

- **GitHub Issues**: [Open an issue](https://github.com/Thrall12138/online-judge-system/issues)
- **Email**: support@online-judge.example.com
- **Discord**: [Join our community](https://discord.gg/example)

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by platforms like Codeforces, LeetCode, and HackerRank
- Built with modern technologies and best practices

---

**Last Updated**: December 30, 2025

For more information, visit our [official documentation](https://docs.online-judge.example.com)
