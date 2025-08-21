# 🚀 Job Description Refiner Crew - API Documentation

## 📋 Overview

The Job Description Refiner Crew API provides a complete workflow for processing raw project descriptions into professional, structured project requirements. The API supports the entire process from initial analysis to final project creation.

## 🔗 Base URL

```
https://your-domain.com/api/v1/job-refiner
```

## 🔐 Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## 📊 API Endpoints

### 1. 🚀 Process Initial Description

**POST** `/process-initial`

Processes a raw project description and generates initial analysis with clarification questions.

#### Request Body

```json
{
  "raw_description": "We need a React app with authentication and user dashboard",
  "client_responses": [],
  "user_preferences": {
    "industry": "Technology",
    "budget": "Medium",
    "timeline": "3-6 months"
  }
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "project_analysis": {
      "project_type": "project",
      "complexity_level": "moderate",
      "primary_industry": "Technology",
      "scope_breakdown": ["Frontend Development", "Authentication System", "User Dashboard"],
      "risk_assessment": ["Timeline constraints", "Technical complexity"],
      "recommended_next_steps": ["Clarify timeline", "Define user roles"]
    },
    "ambiguity_analysis": {
      "ambiguities": [
        {
          "description": "User roles and permissions not specified",
          "category": "User Management",
          "priority": "high",
          "risk_level": "medium",
          "impact": "Could affect development timeline and scope"
        }
      ],
      "questions_by_category": {
        "User Management": [
          {
            "question": "What user roles do you need (admin, user, moderator)?",
            "category": "User Management",
            "priority": "high",
            "context": "Essential for authentication system design",
            "expected_answer_type": "List of roles with descriptions"
          }
        ]
      }
    }
  },
  "message": "Initial description processed successfully. Clarification questions generated.",
  "processing_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Status Codes

- `200` - Successfully processed
- `400` - Invalid request data
- `401` - Unauthorized (missing/invalid token)
- `500` - Internal server error

---

### 2. 💬 Submit Client Feedback

**POST** `/submit-client-feedback/{processing_id}`

Submits client responses to clarification questions and re-processes the description.

#### Path Parameters

- `processing_id` (string) - The processing session ID from the initial request

#### Request Body

```json
[
  {
    "question": "What user roles do you need (admin, user, moderator)?",
    "answer": "We need admin and regular user roles. Admin should manage users and content.",
    "skipped": false,
    "skip_reason": null,
    "additional_context": "Admin should have full access, users should have limited access"
  },
  {
    "question": "What is your budget range?",
    "answer": null,
    "skipped": true,
    "skip_reason": "Budget not finalized yet",
    "additional_context": null
  }
]
```

#### Response

```json
{
  "success": true,
  "data": {
    "project_analysis": {
      "project_type": "project",
      "complexity_level": "moderate",
      "primary_industry": "Technology"
    },
    "skills_analysis": {
      "explicit_skills": [
        {
          "skill_name": "React",
          "category": "programming",
          "importance": "high",
          "proficiency_level": "intermediate",
          "is_explicit": true
        }
      ],
      "implicit_skills": [
        {
          "skill_name": "Authentication",
          "category": "security",
          "importance": "high",
          "proficiency_level": "intermediate",
          "is_explicit": false
        }
      ]
    },
    "refined_description": {
      "executive_summary": "React application with role-based authentication system",
      "project_overview": {
        "title": "Project Overview",
        "content": "Modern React application with secure authentication..."
      }
    }
  },
  "message": "Description refined successfully with client feedback",
  "processing_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 3. ✅ Finalize Description

**POST** `/finalize-description/{processing_id}`

Finalizes the refined project description and saves it to the database.

#### Path Parameters

- `processing_id` (string) - The processing session ID

#### Request Body

```json
{
  "title": "React Authentication App",
  "description": "Modern React application with secure authentication system",
  "additional_notes": "Focus on security and user experience"
}
```

#### Response

```json
{
  "success": true,
  "message": "Project description finalized and saved successfully",
  "project_id": "660e8400-e29b-41d4-a716-446655440001",
  "processing_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 4. 📊 Get Session Status

**GET** `/session/{processing_id}`

Retrieves the current status and data of a processing session.

#### Path Parameters

- `processing_id` (string) - The processing session ID

#### Response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-uuid-here",
  "raw_description": "We need a React app with authentication",
  "status": "refined_completed",
  "initial_analysis": { ... },
  "ambiguity_analysis": { ... },
  "client_responses": [ ... ],
  "refined_analysis": { ... },
  "project_id": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "finalized_at": null
}
```

---

### 5. 📋 Get User Sessions

**GET** `/user-sessions`

Retrieves all processing sessions for the current user.

#### Query Parameters

- `limit` (integer, optional) - Number of sessions to return (default: 10)
- `offset` (integer, optional) - Number of sessions to skip (default: 0)

#### Response

```json
{
  "sessions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "refined_completed",
      "raw_description": "React app with authentication",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

---

### 6. 🗑️ Delete Session

**DELETE** `/session/{processing_id}`

Deletes a processing session.

#### Path Parameters

- `processing_id` (string) - The processing session ID

#### Response

```json
{
  "success": true,
  "message": "Session deleted successfully"
}
```

---

### 7. ℹ️ Get Crew Information

**GET** `/crew-info`

Retrieves information about the Job Refiner Crew configuration.

#### Response

```json
{
  "success": true,
  "crew_info": {
    "crew_name": "Job Description Refiner Crew",
    "version": "1.0.0",
    "agents": [
      "Project Analyzer Agent",
      "Ambiguity Detector Agent",
      "Client Interaction Agent",
      "Skill Extractor Agent",
      "Project Classifier Agent",
      "Description Refiner Agent"
    ],
    "execution_strategy": "Hierarchical with delegation",
    "memory_enabled": true,
    "llm_model": "gemini/gemini-2.0-flash",
    "temperature": 0.7
  }
}
```

## 🔄 Complete Workflow Example

### Step 1: Process Initial Description

```bash
curl -X POST "https://your-domain.com/api/v1/job-refiner/process-initial" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We need a website for our restaurant with online ordering",
    "user_preferences": {
      "industry": "Food & Beverage",
      "budget": "Medium"
    }
  }'
```

**Response**: Get `processing_id` and clarification questions

### Step 2: Submit Client Feedback

```bash
curl -X POST "https://your-domain.com/api/v1/job-refiner/submit-client-feedback/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "question": "What payment methods do you want to support?",
      "answer": "Credit cards and PayPal",
      "skipped": false
    }
  ]'
```

**Response**: Get refined project description

### Step 3: Finalize and Save

```bash
curl -X POST "https://your-domain.com/api/v1/job-refiner/finalize-description/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Restaurant Website with Online Ordering",
    "description": "Modern restaurant website with online ordering system"
  }'
```

**Response**: Project saved to database with `project_id`

## 📊 Database Schema

The API automatically creates and manages the following database tables:

### `job_refiner_sessions`
- Processing session tracking
- Initial and refined analysis results
- Client feedback storage

### `projects`
- Finalized project information
- Project metadata and classification
- User ownership and status

### `project_requirements`
- Detailed project requirements
- Scope, deliverables, timeline
- Risk assessment and success criteria

### `project_skills`
- Required skills and technologies
- Skill categorization and importance
- Proficiency level requirements

## 🛡️ Security Features

- **JWT Authentication**: All endpoints require valid authentication
- **Row Level Security**: Users can only access their own data
- **Input Validation**: Pydantic schema validation for all requests
- **Error Handling**: Comprehensive error messages and status codes

## 📈 Performance Considerations

- **Session Management**: In-memory session storage for active processing
- **Database Optimization**: Proper indexing and RLS policies
- **Async Processing**: Background task support for long-running operations
- **Caching**: Session data cached for quick access

## 🔧 Error Handling

### Common Error Responses

```json
{
  "success": false,
  "error": "Error description",
  "message": "User-friendly error message",
  "processing_id": ""
}
```

### Error Status Codes

- `400` - Bad Request (invalid data)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (access denied)
- `404` - Not Found (session/project not found)
- `500` - Internal Server Error

## 🧪 Testing

### Test with Sample Data

```bash
# Test the complete workflow
curl -X POST "https://your-domain.com/api/v1/job-refiner/process-initial" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We need a simple blog website with admin panel",
    "user_preferences": {
      "industry": "Technology",
      "budget": "Low"
    }
  }'
```

### Monitor Session Status

```bash
# Check session status
curl -X GET "https://your-domain.com/api/v1/job-refiner/session/<processing_id>" \
  -H "Authorization: Bearer <your-token>"
```

## 🚀 Integration Examples

### Frontend Integration

```javascript
// Process initial description
const processDescription = async (rawDescription) => {
  const response = await fetch('/api/v1/job-refiner/process-initial', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      raw_description: rawDescription,
      user_preferences: { industry: 'Technology' }
    })
  });
  
  const result = await response.json();
  return result;
};

// Submit client feedback
const submitFeedback = async (processingId, responses) => {
  const response = await fetch(`/api/v1/job-refiner/submit-client-feedback/${processingId}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(responses)
  });
  
  const result = await response.json();
  return result;
};
```

### Backend Integration

```python
# Process project description
from app.agents.job_refiner_crew import JobRefinerCrew
from app.schemas.job_refiner import JobRefinerRequest

crew = JobRefinerCrew()
request = JobRefinerRequest(
    raw_description="We need a Python API with authentication",
    client_responses=[],
    user_preferences={"industry": "Technology"}
)

result = crew.process_project_description(request)
print(f"Project Type: {result.project_analysis.project_type}")
```

---

**This API provides a complete, secure, and scalable solution for processing project descriptions through the Job Description Refiner Crew. The workflow supports the entire process from initial analysis to final project creation, with comprehensive error handling and security features.**
