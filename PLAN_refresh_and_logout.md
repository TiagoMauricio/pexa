# Refresh Token, Logout, and User Activity Implementation Plan

## Overview

This document outlines the implementation plan for adding refresh token functionality and a logout endpoint to our authentication system.

## 1. User Activity Tracking

### 1.1 Database Changes

- Update `users` table to add:
  - `last_login`: Timestamp of last successful login
  - `last_activity`: Timestamp of last activity
  - `is_active`: Boolean flag for account status

### 1.2 Implementation

- Update login endpoint to set `last_login` on successful authentication
- Add middleware to update `last_activity` on each authenticated request
- Add user status management (activate/deactivate)
- Add account lockout after failed login attempts

## 2. Refresh Token Implementation

### 1.1 Database Changes

- Add a `refresh_tokens` table to store active refresh tokens with the following fields:
  - `id`: Primary key
  - `user_id`: Foreign key to users table
  - `token`: The refresh token (hashed)
  - `expires_at`: Expiration timestamp
  - `created_at`: Creation timestamp
  - `revoked`: Boolean flag for token revocation

### 1.2 Security Updates

1. Update `security.py` to include:
   - `create_refresh_token()`: Function to generate refresh tokens
   - `verify_refresh_token()`: Function to validate refresh tokens
   - `revoke_refresh_token()`: Function to revoke refresh tokens

2. Update JWT configuration:
   - Set refresh token expiration (e.g., 7 days)
   - Add refresh token secret key

### 1.3 API Endpoints

#### POST /api/auth/refresh

- **Request**:

  ```json
  {
    "refresh_token": "string"
  }
  ```

- **Response**:

  ```json
  {
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "bearer"
  }
  ```

- **Behavior**:
  - Verify the refresh token
  - If valid, issue new access and refresh tokens
  - Revoke the old refresh token
  - Return new tokens

## 3. Logout Implementation

### 2.1 Token Management

- Store refresh tokens in the database (already part of refresh token implementation)
- Implement token revocation on logout

### 2.2 API Endpoints

#### POST /api/auth/logout

- **Request**:

  ```json
  {
    "refresh_token": "string"
  }
  ```

- **Response**:

  ```json
  {
    "message": "Successfully logged out"
  }
  ```

- **Behavior**:
  - Revoke the provided refresh token
  - Optionally, implement token blacklisting for access tokens

## 4. Security Considerations

### 4.1 Security Measures

1. **Refresh Token Rotation**:
   - Issue a new refresh token on each refresh
   - Revoke the previous refresh token
   - Prevent token reuse

2. **Token Storage**:
   - Store only hashed versions of refresh tokens
   - Set appropriate expiration times
   - Implement cleanup of expired tokens

3. **Rate Limiting**:
   - Implement rate limiting on authentication endpoints
   - Prevent token brute force attacks

## 5. Implementation Steps

1. Create database migrations for:
   - Refresh tokens table
   - Add activity fields to users table
2. Update user model and authentication flow:
   - Track last login time
   - Update last activity timestamp
   - Implement account status management
3. Update authentication flow:
   - Add activity logging for auth events
   - Implement refresh token rotation
   - Add logout functionality
4. Add API endpoints:
   - Token refresh
   - Logout
   - Activity log access
5. Add tests for new functionality
6. Update API documentation
7. Add monitoring and alerting for suspicious activities

1. Create database migration for refresh tokens table
2. Implement token management functions in `security.py`
3. Add refresh token endpoint
4. Add logout endpoint
5. Update authentication middleware to handle token refresh
6. Add tests for new endpoints
7. Update API documentation

## 6. Testing Strategy

1. **User Activity Tracking**:
   - Test last login timestamp updates
   - Verify last activity updates
   - Test account status changes
   - Verify failed login handling

2. **Refresh Token Flow**

1. **Refresh Token Flow**:
   - Test successful token refresh
   - Test with expired refresh token
   - Test with invalid refresh token
   - Test refresh token reuse prevention

3. **Logout Flow**:
   - Test successful logout
   - Verify token is revoked after logout
   - Test logout with invalid token
   - Test logout with already revoked token

## 7. Dependencies

- Update requirements if additional packages are needed
- Ensure database migrations are in place

## 8. Rollback Plan

- Database migration rollback script
- API versioning for smooth transitions
