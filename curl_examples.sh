#!/bin/bash
# Minimal cURL scenario: 2 users, budget sharing, token refresh, cleanup
set -euo pipefail
API_URL="http://localhost:8000/api"

# Generate unique emails for each run
UUID=$(uuidgen | tr 'A-Z' 'a-z')
USER1_EMAIL="user1_${UUID}@example.com"
USER2_EMAIL="user2_${UUID}@example.com"
USER1_PASS="testpass1"
USER2_PASS="testpass2"

# Register user1
curl -s -X POST "$API_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{"email": "'$USER1_EMAIL'", "password": "'$USER1_PASS'"}'
echo -e "\nUser1 registered: $USER1_EMAIL"

# Register user2
curl -s -X POST "$API_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{"email": "'$USER2_EMAIL'", "password": "'$USER2_PASS'"}'
echo -e "\nUser2 registered: $USER2_EMAIL"

# Login user1
USER1_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$USER1_EMAIL&password=$USER1_PASS")
USER1_TOKEN=$(echo "$USER1_LOGIN" | jq -r .access_token)
USER1_ID=$(curl -s -X GET "$API_URL/users/me" -H "Authorization: Bearer $USER1_TOKEN" | jq -r .id)
echo "User1 access token: $USER1_TOKEN"

# Login user2
USER2_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$USER2_EMAIL&password=$USER2_PASS")
USER2_TOKEN=$(echo "$USER2_LOGIN" | jq -r .access_token)
USER2_REFRESH=$(echo "$USER2_LOGIN" | jq -r .refresh_token)
USER2_ID=$(curl -s -X GET "$API_URL/users/me" -H "Authorization: Bearer $USER2_TOKEN" | jq -r .id)
echo "User2 access token: $USER2_TOKEN"
echo "User2 refresh token: $USER2_REFRESH"

# User1 creates a budget
BUDGET_ID=$(curl -s -X POST "$API_URL/budgets/" \
    -H "Authorization: Bearer $USER1_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "Shared Budget"}' | jq -r .id)
echo "Budget created by user1: $BUDGET_ID"

# User1 shares budget with user2 (write access)
curl -s -X POST "$API_URL/budgets/share" \
    -H "Authorization: Bearer $USER1_TOKEN" \
    --data-urlencode "budget_id=$BUDGET_ID" \
    --data-urlencode "user_id=$USER2_ID" \
    --data-urlencode "can_write=true"
echo -e "\nBudget shared with user2"

# User2 lists budgets (should see 'Shared Budget')
USER2_BUDGETS=$(curl -s -X GET "$API_URL/budgets/" \
    -H "Authorization: Bearer $USER2_TOKEN")
echo "User2 budgets: $USER2_BUDGETS"
echo "$USER2_BUDGETS" | grep 'Shared Budget' && echo "User2 can see shared budget!" || echo "ERROR: User2 cannot see shared budget."

# User2 refreshes token
REFRESH_RESP=$(curl -s -X POST "$API_URL/auth/refresh" \
    -H "Content-Type: application/json" \
    -d '{"refresh_token": "'$USER2_REFRESH'"}')
USER2_NEW_TOKEN=$(echo "$REFRESH_RESP" | jq -r .access_token)
echo "User2 new access token: $USER2_NEW_TOKEN"

# Cleanup: (Assumes an admin or user delete endpoint exists)
# If not, print instructions for manual deletion
DELETE1=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$API_URL/users/$USER1_ID")
DELETE2=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$API_URL/users/$USER2_ID")
if [[ "$DELETE1" == "200" && "$DELETE2" == "200" ]]; then
  echo "Users deleted."
else
  echo "Manual cleanup needed: delete users $USER1_EMAIL and $USER2_EMAIL from DB."
fi

# 3. Get current user info
curl -X GET "$API_URL/users/me" \
    -H "Authorization: Bearer $USER2_NEW_TOKEN"
echo -e "\n---"

# 4. Create a new budget
BUDGET_ID=$(curl -s -X POST "$API_URL/budgets/" \
    -H "Authorization: Bearer $USER2_NEW_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "My First Budget"}' | jq -r .id)
echo "Budget ID: $BUDGET_ID"
echo -e "\n---"

# 5. List budgets
curl -X GET "$API_URL/budgets/" \
    -H "Authorization: Bearer $USER2_NEW_TOKEN"
echo -e "\n---"

# 6. Create a category in the budget
CATEGORY_ID=$(curl -s -X POST "$API_URL/categories/" \
    -H "Authorization: Bearer $USER2_NEW_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "Groceries", "budget_id": '"$BUDGET_ID"'}' | jq -r .id)
echo "Category ID: $CATEGORY_ID"
echo -e "\n---"

# 7. List categories for the budget
curl -X GET "$API_URL/categories/?budget_id=$BUDGET_ID" \
    -H "Authorization: Bearer $USER2_NEW_TOKEN"
echo -e "\n---"

# 8. Create a transaction in the category
curl -X POST "$API_URL/transactions/" \
    -H "Authorization: Bearer $USER2_NEW_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"amount": 42.50, "note": "Weekly groceries", "category_id": '"$CATEGORY_ID"'}'
echo -e "\n---"

# 9. List transactions for the category
curl -X GET "$API_URL/transactions/?category_id=$CATEGORY_ID" \
    -H "Authorization: Bearer $USER2_NEW_TOKEN"
echo -e "\n---"

# 10. Share budget with another user (replace user_id and can_write as needed)
# curl -X POST "$API_URL/budgets/$BUDGET_ID/share" \
#     -H "Authorization: Bearer $USER2_NEW_TOKEN" \
#     -H "Content-Type: application/json" \
#     -d '{"user_id": 2, "can_write": true}'

# Note: jq is used for parsing JSON (install with `brew install jq` or `apt-get install jq`)
