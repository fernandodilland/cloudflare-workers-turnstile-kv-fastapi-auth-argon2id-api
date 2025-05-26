@echo off
echo Adding test user to KV store...
echo.
echo Test User Credentials:
echo Username: testuser
echo Password: password123
echo.

npx wrangler kv key put "user:testuser" --path="test_user_data.json" --binding=USERS_KV --remote --preview false

echo.
echo Test user added to KV store!
echo You can now test the login endpoint with:
echo   Username: testuser
echo   Password: password123
pause
