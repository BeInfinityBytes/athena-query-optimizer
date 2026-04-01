# athena-query-optimizer
Query Optimization Engine For Amazon Athena

Do this before Implementing

The signup form works correctly on the published URL — it submits and shows "Sign up failed — Network error." This is expected because cognitoConfig.ts still has placeholder values (YOUR_USER_POOL_ID, YOUR_APP_CLIENT_ID, YOUR_IDENTITY_POOL_ID).

To make it work, update src/lib/cognitoConfig.ts with your real AWS Cognito credentials:

UserPoolId — from Cognito → User Pools → General Settings
ClientId — from App Integration → App Client Settings
IdentityPoolId — from Cognito → Identity Pools
Region — your AWS region
Once you provide those values, signup and login will connect to your actual Cognito User Pool.