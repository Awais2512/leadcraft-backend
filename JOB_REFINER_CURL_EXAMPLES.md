# 🚀 Job Description Refiner API - Curl Request Examples

## 🔧 Setup & Configuration

### Base Configuration
```bash
# Set your base URL and authentication token
export API_BASE_URL="http://localhost:8000/api/v1/job-refiner"
export JWT_TOKEN="your-jwt-token-here"

# Common headers for all requests
export HEADERS="-H 'Authorization: Bearer $JWT_TOKEN' -H 'Content-Type: application/json'"
```

### Get Your JWT Token First
```bash
# Login to get JWT token (adjust URL as needed)
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'

# Use the returned token for subsequent requests
export JWT_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 📊 API Endpoint Examples

### 1. 🚀 Process Initial Description

**Process a raw project description and get clarification questions:**

```bash
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We need a React website with user authentication and admin dashboard. It should have a modern UI and be responsive.",
    "client_responses": [],
    "user_preferences": {
      "industry": "Technology",
      "budget": "Medium",
      "timeline": "3-6 months"
    }
  }'
```

**Example with different project types:**

```bash
# E-commerce Project
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "I need an online store for selling handmade jewelry. Customers should be able to browse products, add to cart, and checkout with payment.",
    "user_preferences": {
      "industry": "E-commerce",
      "budget": "Low",
      "timeline": "1-3 months"
    }
  }'

# Mobile App Project
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We want a fitness tracking mobile app that syncs with wearable devices and provides workout recommendations.",
    "user_preferences": {
      "industry": "Health & Fitness",
      "budget": "High",
      "timeline": "6-12 months"
    }
  }'

# API/Backend Service
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We need a REST API for our inventory management system with real-time updates and reporting features.",
    "user_preferences": {
      "industry": "Business/Enterprise",
      "budget": "Medium",
      "timeline": "3-4 months"
    }
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "project_analysis": {
      "project_type": "project",
      "complexity_level": "moderate",
      "primary_industry": "Technology",
      "scope_breakdown": ["Frontend Development", "Authentication System", "Admin Dashboard"],
      "risk_assessment": ["Timeline constraints", "UI/UX complexity"],
      "recommended_next_steps": ["Clarify user roles", "Define admin features"]
    },
    "ambiguity_analysis": {
      "questions_by_category": {
        "User Management": [
          {
            "question": "What specific user roles do you need (admin, moderator, regular user)?",
            "priority": "high",
            "context": "Essential for authentication system design"
          }
        ],
        "Technical": [
          {
            "question": "Do you have any preferred technology stack or frameworks?",
            "priority": "medium",
            "context": "Will influence development approach"
          }
        ]
      }
    }
  },
  "message": "Initial description processed successfully. Clarification questions generated.",
  "processing_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 2. 💬 Submit Client Feedback

**Submit answers to clarification questions:**

```bash
# Save the processing ID from the previous response
export PROCESSING_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X POST "$API_BASE_URL/submit-client-feedback/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "question": "What specific user roles do you need (admin, moderator, regular user)?",
      "answer": "We need admin users who can manage all content and settings, and regular users who can only view and interact with content.",
      "skipped": false,
      "skip_reason": null,
      "additional_context": "Admin should have full CRUD permissions, users should be read-only with some interaction features."
    },
    {
      "question": "Do you have any preferred technology stack or frameworks?",
      "answer": "We prefer React for frontend, Node.js for backend, and PostgreSQL for database.",
      "skipped": false,
      "skip_reason": null,
      "additional_context": "Our team is most experienced with this stack."
    },
    {
      "question": "What is your budget range for this project?",
      "answer": null,
      "skipped": true,
      "skip_reason": "Budget is still being finalized by management",
      "additional_context": null
    },
    {
      "question": "Do you need mobile responsiveness?",
      "answer": "Yes, it must work perfectly on all devices including tablets and phones.",
      "skipped": false,
      "skip_reason": null,
      "additional_context": "Mobile users represent 60% of our traffic."
    }
  ]'
```

**Different feedback scenarios:**

```bash
# Minimal feedback (some questions skipped)
curl -X POST "$API_BASE_URL/submit-client-feedback/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "question": "What user roles do you need?",
      "answer": "Just admin and regular users",
      "skipped": false
    },
    {
      "question": "What is your timeline?",
      "answer": null,
      "skipped": true,
      "skip_reason": "Timeline is flexible"
    }
  ]'

# Comprehensive feedback
curl -X POST "$API_BASE_URL/submit-client-feedback/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "question": "What payment methods should be supported?",
      "answer": "Credit cards, PayPal, and Apple Pay",
      "skipped": false,
      "additional_context": "We want to support the most common payment methods for better conversion"
    },
    {
      "question": "Do you need inventory management features?",
      "answer": "Yes, real-time inventory tracking with low stock alerts",
      "skipped": false,
      "additional_context": "We have about 500 products and need automated management"
    },
    {
      "question": "What shipping options do you need?",
      "answer": "Standard shipping, express shipping, and local pickup",
      "skipped": false,
      "additional_context": "We ship nationwide and have a local pickup location"
    }
  ]'
```

---

### 3. ✅ Finalize Description

**Finalize the refined project and save to database:**

```bash
curl -X POST "$API_BASE_URL/finalize-description/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "React Admin Dashboard with Authentication",
    "description": "Modern, responsive React application with role-based authentication system, admin dashboard, and user management features.",
    "additional_notes": "Focus on security, user experience, and mobile responsiveness. Use modern UI components and ensure scalability."
  }'
```

**Different project finalization examples:**

```bash
# E-commerce finalization
curl -X POST "$API_BASE_URL/finalize-description/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Handmade Jewelry E-commerce Store",
    "description": "Complete online store with product catalog, shopping cart, payment processing, and order management for handmade jewelry business.",
    "additional_notes": "Emphasize beautiful product photography display and smooth checkout process."
  }'

# API project finalization
curl -X POST "$API_BASE_URL/finalize-description/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inventory Management REST API",
    "description": "Comprehensive REST API for inventory management with real-time updates, reporting, and integration capabilities.",
    "additional_notes": "Must handle high concurrent requests and provide detailed API documentation."
  }'
```

**Expected Response:**
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

**Check the status of a processing session:**

```bash
curl -X GET "$API_BASE_URL/session/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-uuid-here",
  "raw_description": "We need a React website with user authentication and admin dashboard",
  "status": "refined_completed",
  "initial_analysis": { /* Project analysis data */ },
  "ambiguity_analysis": { /* Questions and ambiguities */ },
  "client_responses": [ /* Client feedback */ ],
  "refined_analysis": { /* Final refined analysis */ },
  "project_id": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "finalized_at": null
}
```

---

### 5. 📋 Get User Sessions

**List all processing sessions for the current user:**

```bash
# Get latest 10 sessions
curl -X GET "$API_BASE_URL/user-sessions" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Get sessions with pagination
curl -X GET "$API_BASE_URL/user-sessions?limit=5&offset=10" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Get first 20 sessions
curl -X GET "$API_BASE_URL/user-sessions?limit=20" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "sessions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "raw_description": "React website with authentication",
      "created_at": "2024-01-15T10:30:00Z",
      "project_id": "660e8400-e29b-41d4-a716-446655440001"
    },
    {
      "id": "661e8400-e29b-41d4-a716-446655440001",
      "status": "initial_processed",
      "raw_description": "Mobile app for fitness tracking",
      "created_at": "2024-01-14T15:20:00Z",
      "project_id": null
    }
  ],
  "total": 2,
  "limit": 10,
  "offset": 0
}
```

---

### 6. 🗑️ Delete Session

**Delete a processing session:**

```bash
curl -X DELETE "$API_BASE_URL/session/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Session deleted successfully"
}
```

---

### 7. ℹ️ Get Crew Information

**Get information about the Job Refiner Crew configuration:**

```bash
curl -X GET "$API_BASE_URL/crew-info" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
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

---

## 🔄 Complete Workflow Examples

### Example 1: React Website Project

```bash
# Step 1: Process initial description
RESPONSE=$(curl -s -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "We need a React website for our consulting company with contact forms and service pages",
    "user_preferences": {
      "industry": "Consulting",
      "budget": "Medium"
    }
  }')

# Extract processing ID
PROCESSING_ID=$(echo $RESPONSE | jq -r '.processing_id')
echo "Processing ID: $PROCESSING_ID"

# Step 2: Submit client feedback
curl -X POST "$API_BASE_URL/submit-client-feedback/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "question": "What services do you offer?",
      "answer": "Business strategy, digital transformation, and process optimization",
      "skipped": false
    },
    {
      "question": "Do you need a blog section?",
      "answer": "Yes, for thought leadership content",
      "skipped": false
    }
  ]'

# Step 3: Finalize project
curl -X POST "$API_BASE_URL/finalize-description/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Consulting Company Website",
    "description": "Professional React website with service pages, contact forms, and blog section"
  }'
```

### Example 2: E-commerce Project

```bash
# Step 1: Initial processing
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "Online store for selling custom t-shirts with design upload feature",
    "user_preferences": {
      "industry": "E-commerce",
      "budget": "Medium"
    }
  }' | jq '.processing_id' | tr -d '"' > processing_id.txt

PROCESSING_ID=$(cat processing_id.txt)

# Step 2: Comprehensive feedback
curl -X POST "$API_BASE_URL/submit-client-feedback/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "question": "What payment methods do you want to support?",
      "answer": "Credit cards, PayPal, and digital wallets",
      "skipped": false
    },
    {
      "question": "Do you need inventory management?",
      "answer": "Yes, with automatic reordering for blank t-shirts",
      "skipped": false
    },
    {
      "question": "What file formats should the design uploader accept?",
      "answer": "PNG, JPG, SVG, and PDF files up to 10MB",
      "skipped": false
    }
  ]'

# Step 3: Finalize
curl -X POST "$API_BASE_URL/finalize-description/$PROCESSING_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Custom T-Shirt E-commerce Platform",
    "description": "Complete e-commerce solution for custom t-shirt printing with design upload, payment processing, and inventory management"
  }'
```

---

## 🔧 Debugging & Monitoring

### Check API Health
```bash
# Test if the API is running
curl -X GET "$API_BASE_URL/crew-info" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### Monitor Session Progress
```bash
# Check session status periodically
watch -n 5 "curl -s -X GET '$API_BASE_URL/session/$PROCESSING_ID' -H 'Authorization: Bearer $JWT_TOKEN' | jq '.status'"
```

### List All Sessions for Debugging
```bash
# Get all sessions with details
curl -X GET "$API_BASE_URL/user-sessions?limit=100" \
  -H "Authorization: Bearer $JWT_TOKEN" | jq '.'
```

---

## 🛠️ Advanced Usage

### Using Variables for Reusability
```bash
# Set up environment
export API_BASE_URL="http://localhost:8000/api/v1/job-refiner"
export JWT_TOKEN="your-token-here"

# Function to process description
process_description() {
  local description="$1"
  local industry="$2"
  
  curl -X POST "$API_BASE_URL/process-initial" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"raw_description\": \"$description\",
      \"user_preferences\": {
        \"industry\": \"$industry\"
      }
    }"
}

# Usage
process_description "We need a mobile app for food delivery" "Food & Beverage"
```

### Batch Processing Multiple Projects
```bash
# Process multiple descriptions
descriptions=(
  "React dashboard for analytics"
  "Mobile app for event planning"
  "API for IoT device management"
)

for desc in "${descriptions[@]}"; do
  echo "Processing: $desc"
  curl -X POST "$API_BASE_URL/process-initial" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"raw_description\": \"$desc\"}" \
    | jq '.processing_id'
  sleep 2  # Rate limiting
done
```

---

## 🔍 Error Handling

### Common Error Responses
```bash
# Invalid token (401)
curl -X GET "$API_BASE_URL/crew-info" \
  -H "Authorization: Bearer invalid-token"

# Session not found (404)
curl -X GET "$API_BASE_URL/session/invalid-id" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Invalid request data (400)
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
```

### Testing Error Scenarios
```bash
# Test with empty description
curl -X POST "$API_BASE_URL/process-initial" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "",
    "user_preferences": {}
  }'

# Test with missing authentication
curl -X GET "$API_BASE_URL/user-sessions"

# Test with invalid session ID
curl -X DELETE "$API_BASE_URL/session/non-existent-id" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

---

**These curl examples provide comprehensive coverage of all Job Description Refiner API endpoints with practical, real-world scenarios. Use them to test your API implementation and integrate with your frontend applications.**

