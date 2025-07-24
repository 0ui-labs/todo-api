#!/bin/bash

# Test Categories API with curl

echo "===== Testing Categories API ====="

# Variables
BASE_URL="http://localhost:8000/api/v1"
EMAIL="testcategories@example.com"
PASSWORD="TestPassword123"
NAME="Category Test User"

echo -e "\n1. Register new user"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\", \"name\": \"$NAME\"}")
echo "Response: $REGISTER_RESPONSE"

echo -e "\n2. Login to get token"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")
echo "Response: $LOGIN_RESPONSE"

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
if [ -z "$TOKEN" ]; then
  echo "Failed to get token. Exiting."
  exit 1
fi
echo "Token obtained: ${TOKEN:0:20}..."

echo -e "\n3. Create category (Work)"
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/categories/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Work", "color": "#FF5733"}')
echo "Response: $CREATE_RESPONSE"
CATEGORY_ID=$(echo $CREATE_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)

echo -e "\n4. Create another category (Personal)"
curl -s -X POST "$BASE_URL/categories/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Personal", "color": "#00FF00"}'

echo -e "\n5. List all categories"
curl -s -X GET "$BASE_URL/categories/" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo -e "\n6. Get specific category"
curl -s -X GET "$BASE_URL/categories/$CATEGORY_ID" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo -e "\n7. Update category"
UPDATE_RESPONSE=$(curl -s -X PATCH "$BASE_URL/categories/$CATEGORY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Work Projects", "color": "#0000FF"}')
echo "Response: $UPDATE_RESPONSE"

echo -e "\n8. Search categories"
curl -s -X GET "$BASE_URL/categories/?search=project" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo -e "\n9. Test pagination"
curl -s -X GET "$BASE_URL/categories/?limit=1&offset=0" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo -e "\n10. Delete category"
DELETE_RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/categories/$CATEGORY_ID" \
  -H "Authorization: Bearer $TOKEN")
echo "Response code: $DELETE_RESPONSE"

echo -e "\n11. Verify category is deleted"
curl -s -X GET "$BASE_URL/categories/$CATEGORY_ID" \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\n===== Test completed ====="