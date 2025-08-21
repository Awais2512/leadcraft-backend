# Simple Job Refiner API - Curl Examples

## 🔧 Setup
```bash
export API_BASE_URL="http://localhost:8000/api/v1/job-refiner"
export JWT_TOKEN="your-jwt-token-here"
```

## 🚀 Flow 1: Initial Processing

Process raw description to get refined description + questions:

```bash
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We need a website for our restaurant with online ordering"
  }'
```

**Response:**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "refined_description": "Professional restaurant website with online ordering system...",
  "title": "Restaurant Website with Online Ordering",
  "project_type": "website",
  "questions": [
    {
      "id": "q1",
      "question": "What payment methods do you want to support?",
      "category": "Requirements",
      "priority": "high"
    },
    {
      "id": "q2", 
      "question": "Do you need table reservation features?",
      "category": "Features",
      "priority": "medium"
    }
  ],
  "message": "Initial processing completed successfully"
}
```

## 🔄 Flow 2: Refine with Answers

Submit answers and get final refined description:

```bash
# Save session ID from previous response
export SESSION_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X POST "$API_BASE_URL/refine-with-answers" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "'$SESSION_ID'",
    "previous_refined_description": "Professional restaurant website with online ordering system...",
    "title": "Restaurant Website with Online Ordering",
    "project_type": "website",
    "answers": [
      {
        "question_id": "q1",
        "question": "What payment methods do you want to support?",
        "answer": "Credit cards, PayPal, and Apple Pay",
        "skipped": false
      },
      {
        "question_id": "q2",
        "question": "Do you need table reservation features?", 
        "answer": "Yes, with time slot booking",
        "skipped": false
      }
    ]
  }'
```

**Response:**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "final_refined_description": "Comprehensive restaurant website with online ordering system supporting credit cards, PayPal, and Apple Pay. Includes table reservation system with time slot booking...",
  "title": "Restaurant Website with Online Ordering",
  "project_type": "website",
  "message": "Description refined successfully with client answers"
}
```

## 📊 Additional Endpoints

### Get Session Data
```bash
curl -X GET "$API_BASE_URL/session/$SESSION_ID" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### Finalize Project
```bash
curl -X POST "$API_BASE_URL/finalize/$SESSION_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Restaurant Website with Online Ordering"
  }'
```

## 🧪 Complete Example Workflow

```bash
# Step 1: Process initial description
RESPONSE=$(curl -s -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We need a mobile app for food delivery"
  }')

# Extract session ID
SESSION_ID=$(echo $RESPONSE | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

# Step 2: Submit answers
curl -X POST "$API_BASE_URL/refine-with-answers" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "'$SESSION_ID'",
    "previous_refined_description": "Mobile food delivery application...",
    "title": "Food Delivery App",
    "project_type": "mobile-app",
    "answers": [
      {
        "question_id": "q1",
        "question": "Which platforms do you need?",
        "answer": "iOS and Android",
        "skipped": false
      }
    ]
  }'

# Step 3: Finalize
curl -X POST "$API_BASE_URL/finalize/$SESSION_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Food Delivery Mobile App"
  }'
```

## 🎯 Test Cases

### Basic Website
```bash
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "Simple portfolio website for a photographer"
  }'
```

### E-commerce
```bash
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "Online store for selling handmade jewelry"
  }'
```

### API Project
```bash
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "REST API for managing inventory"
  }'
```

---

**This simplified flow focuses on the core functionality: process → questions → answers → final refined description**

