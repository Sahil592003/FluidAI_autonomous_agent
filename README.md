# FluidAI_autonomous_agent

# FluidAI - Autonomous AI Document Generator

## 🚀 Overview

**FluidAI** is a production-ready autonomous AI agent that generates professional documents from natural language requests. Built with **FastAPI** and **Google Gemini 2.5 Flash**, it demonstrates advanced AI capabilities including autonomous planning, sequential execution, self-reflection, and professional document generation.

### Key Features

- 🤖 **Autonomous Planning** - Dynamically creates execution plans using LLM
- ⚡ **Batch Execution** - Generates ALL document sections in a single API call (75% fewer API calls)
- 🔍 **Self-Reflection** - Reviews and improves content quality automatically
- 📄 **Professional DOCX** - Generates well-formatted Word documents
- 🌐 **Universal** - Handles ANY document type (business, technical, healthcare, marketing, etc.)
- 🛡️ **Rate Limit Management** - Handles API limits gracefully with retry logic
- 📊 **Production-Ready** - Clean architecture, logging, error handling

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Endpoint                        │
│                         POST /agent                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Autonomous Agent                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐ │
│  │   Planner   │→│  Executor   │→│ Reflection  │→│  DOCX  │ │
│  │  (1 API)   │  │  (1 API)   │  │  (1 API)   │  │ Gen   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────┘ │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Gemini 2.5 Flash API                       │
│                 3-4 API Calls per Document                      │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Highlights

- **Planner**: Analyzes request, creates task list (1 API call)
- **Batch Executor**: Generates ALL sections in ONE API call
- **Reflection**: Reviews quality, improves content (1 API call)
- **DOCX Generator**: Creates professional Word document (0 API calls)
- **Total**: Only 3-4 API calls per document!

---

## 📁 Project Structure

```
fluidAI/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── models.py               # Pydantic models
│   ├── agent.py                # Main orchestrator
│   ├── llm.py                  # Gemini API integration
│   ├── planner.py              # Autonomous planning
│   ├── executor.py             # Sequential task execution
│   ├── batch_executor.py       # Batch execution (ALL sections)
│   ├── reflection.py           # Self-reflection & improvement
│   ├── doc_generator.py        # DOCX document generation
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── prompts.py          # Universal prompts
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Utility functions
│
├── generated_docs/             # Generated documents
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md                   # This file
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fluidAI
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Get your API key**: [Google AI Studio](https://aistudio.google.com/)

---

## 🚀 Running the Application

### Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Usage

### Endpoint: `POST /agent`

Generate a professional document from a natural language request.

#### Request

```json
{
  "request": "Create a business proposal for AI-powered customer service automation with no budget provided."
}
```

#### Response

```json
{
  "status": "success",
  "execution_time": "32.9 sec",
  "plan": [
    "Task 1: Create executive summary",
    "Task 2: Write introduction"
  ],
  "assumptions": [
    "The target audience is business decision-makers",
    "The purpose is to secure funding"
  ],
  "document_path": "generated_docs/business_proposal_20260703_113010.docx",
  "summary": "This proposal outlines an AI-powered customer service automation solution...",
  "error": null
}
```

#### cURL Example

```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Create meeting minutes for a sprint review."
  }'
```

#### Python Example

```python
import requests

response = requests.post(
    "http://localhost:8000/agent",
    json={"request": "Create a business proposal for AI-powered customer service."}
)

print(response.json())
```

---

## 🧪 Test Cases with Actual Results

Below are test cases with their **actual generated document content** from the latest run.

### ✅ Test 1: Business Proposal

**Request:**
```json
{
  "request": "Create a business proposal for AI-powered customer service automation with no budget provided."
}
```

**Result:**
- **Status**: ✅ Success
- **Execution Time**: 29.6 seconds
- **Document**: `business_proposal_20260703_121459.docx`
- **Assumptions**: 4 intelligent assumptions generated

**Summary:**
> Professional Business Proposal generated

---

### ✅ Test 2: Technical Documentation

**Request:**
```json
{
  "request": "Create technical documentation for a RESTful API with authentication and rate limiting."
}
```

**Result:**
- **Status**: ✅ Success
- **Execution Time**: 74.1 seconds
- **Document**: `api_reference_documentation_20260703_121647.docx`
- **Assumptions**: 5 assumptions including RESTful principles, authentication methods, rate limiting headers

**Summary:**
> This document serves as the official reference for the Task Management API, a robust RESTful interface for programmatically managing tasks, projects, and users. It guides developers through core concepts, a quick integration walkthrough, and the secure OAuth 2.0 Bearer Token authentication process.

---

### ✅ Test 3: Healthcare Proposal

**Request:**
```json
{
  "request": "Create a project proposal for an AI-powered patient monitoring system with no budget or timeline provided."
}
```

**Result:**
- **Status**: ✅ Success
- **Execution Time**: 58.4 seconds
- **Document**: `project_proposal_20260703_121809.docx`
- **Assumptions**: 4 assumptions including investors/stakeholders, securing funding, phased approach
- **Sections**: 7/7 sections generated with **EXCELLENT** quality

**Document Content Includes:**
1. Executive Summary - Problem, solution, key benefits
2. Introduction & Problem Statement - Current challenges in patient monitoring
3. Proposed Solution - AI-powered monitoring system with core functionalities
4. Value Proposition & Benefits - For patients, providers, healthcare system
5. Implementation Plan - Phased approach (R&D, Pilot, Full deployment)
6. Risks & Mitigation - Technical, ethical, regulatory, adoption risks
7. Conclusion & Call to Action - Next steps for approval

**Summary:**
> This proposal introduces an AI-Powered Patient Monitoring System to address current intermittent, labor-intensive, and error-prone monitoring practices. Leveraging continuous, real-time vital sign analysis and predictive analytics, this system will significantly enhance patient safety, reduce healthcare costs, and optimize clinical staff workload.

---

### ✅ Test 4: Marketing Strategy

**Request:**
```json
{
  "request": "Create a digital marketing strategy for launching a new SaaS product to enterprise customers."
}
```

**Result:**
- **Status**: ✅ Success
- **Execution Time**: 75.5 seconds
- **Document**: `digital_marketing_strategy_document_20260703_121946.docx`
- **Assumptions**: 5 assumptions including clear value proposition, existing sales team, allocated budget

**Document Content Includes:**
1. Executive Summary & Strategic Overview
2. Product Value Proposition & Enterprise Target Audience Segmentation
3. Marketing Objectives, KPIs & Success Metrics
4. Enterprise Customer Journey & Content Strategy
5. Digital Channels & Tactics (ABM, SEO, SEM, LinkedIn)
6. Lead Generation, Nurturing & Sales Enablement Strategy

**Summary:**
> This Digital Marketing Strategy details a comprehensive, data-driven plan for launching our new enterprise SaaS product. It employs a highly targeted Account-Based Marketing (ABM) approach, integrated with content marketing, SEO, and digital advertising, to educate, nurture, and convert high-value enterprise accounts.

---

## 📊 Test Results Summary

| Test | Document Type | Time | Quality | Status |
|------|---------------|------|---------|--------|
| 1 | Business Proposal | 29.6s | Good | ✅ Success |
| 2 | API Documentation | 74.1s | Good | ✅ Success |
| 3 | Healthcare Proposal | 58.4s | **Excellent** | ✅ Success |
| 4 | Marketing Strategy | 75.5s | Good | ✅ Success |

---

## 📁 Generated Documents

```
generated_docs/
├── business_proposal_20260703_121459.docx
├── api_reference_documentation_20260703_121647.docx
├── project_proposal_20260703_121809.docx
└── digital_marketing_strategy_document_20260703_121946.docx
```
