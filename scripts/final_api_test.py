#!/usr/bin/env python3
"""哇学社全链路API测试 - 最终版"""
import requests, sys, time

BASE = "http://localhost:8002"
PASS = 0
FAIL = 0

def test(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"[PASS] {name} {detail}")
    else:
        FAIL += 1
        print(f"[FAIL] {name} {detail}")

print("=" * 50)
print("Woxueshe Full-Stack API Test (Final)")
print("=" * 50)

# 1. Health
r = requests.get(BASE + "/health", timeout=5)
test("Health Check", r.json().get("status") == "ok")

# 2. Register
uname = f"autobot_{int(time.time())}"
r = requests.post(BASE + "/auth/register", json={
    "username": uname, "password": "test123456",
    "role": "student", "email": f"{uname}@test.com"
}, timeout=5)
test("Register", r.json().get("code") == 0)

# 3. Login
r = requests.post(BASE + "/auth/login", data={
    "username": "student1", "password": "test123456"
}, timeout=5)
j = r.json()
token = j.get("access_token", "")
test("Login", bool(token))

if not token:
    print("SKIP: No auth token")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 4. Me
r = requests.get(BASE + "/auth/me", headers=headers, timeout=5)
test("Get Me", r.json().get("code") == 0)

# 5-7. Courses
r = requests.get(BASE + "/courses/", headers=headers, timeout=5)
test("Courses List", r.json().get("code") == 0)

r = requests.get(BASE + "/courses/1", headers=headers, timeout=5)
test("Course Detail", r.json().get("code") == 0)

r = requests.get(BASE + "/courses/1/sections", headers=headers, timeout=5)
test("Course Sections", r.json().get("code") == 0)

# 8-10. Membership
r = requests.get(BASE + "/membership/plans", headers=headers, timeout=5)
test("Membership Plans", r.json().get("code") == 0)

r = requests.post(BASE + "/membership/sandpay/1", headers=headers, timeout=5)
test("Sand Pay", r.json().get("code") == 0)

r = requests.post(BASE + "/membership/purchase",
                  data={"plan_id": "1"}, headers=headers, timeout=5)
j = r.json()
test("Purchase", j.get("code") in (0, 1001))

# 11-12. Listening
r = requests.get(BASE + "/listening/courses", headers=headers, timeout=5)
test("Listening Courses", r.json().get("code") == 0)

r = requests.get(BASE + "/listening/subtitles/1", headers=headers, timeout=5)
test("Subtitles", r.json().get("code") == 0)

# 13. Review
r = requests.get(BASE + "/review/due", headers=headers, timeout=5)
test("Review Due", r.json().get("code") == 0)

# 14-15. Study
r = requests.get(BASE + "/study/total", headers=headers, timeout=5)
test("Study Total", r.json().get("code") == 0)

r = requests.post(BASE + "/study/record",
                  data={"course_id": "1", "section_id": "1", "duration_seconds": "300"},
                  headers=headers, timeout=5)
test("Study Record", r.json().get("code") == 0)

# Summary
total = PASS + FAIL
print()
print(f"Total: {total} | PASS: {PASS} | FAIL: {FAIL}")
if FAIL == 0:
    print("ALL PASSED!")
    sys.exit(0)
else:
    print(f"FAIL rate: {FAIL/total*100:.1f}%")
    sys.exit(1)
