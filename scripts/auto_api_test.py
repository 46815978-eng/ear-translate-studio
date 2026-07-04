#!/usr/bin/env python3
""" API (v2 - )"""
import requests, json, sys, time

BASE = "http://localhost:8002"
PASS = 0
FAIL = 0

def ok(name, detail=""):
 global PASS
 PASS += 1
 m = f" [PASS] {name}"
 if detail: m += f" - {detail}"
 print(m)

def fail(name, detail=""):
 global FAIL
 FAIL += 1
 print(f" [FAIL] {name}: {detail}")

print("=" * 50)
print(" API v2")
print("=" * 50)

# 1. Health 
try:
 r = requests.get(BASE + "/health", timeout=5)
 data = r.json()
 if data.get("status") == "ok":
 ok("Health Check")
 else:
 fail("Health Check", str(data))
except Exception as e:
 fail("Health Check", str(e))

# 2. Register 
try:
 uname = f"autobot_{int(time.time())}"
 r = requests.post(BASE + "/auth/register", json={
 "username": uname, "password": "test123456", "role": "student"
 }, timeout=5)
 data = r.json()
 if data.get("code") == 0:
 ok("Register", f"user={uname}")
 else:
 fail("Register", json.dumps(data, ensure_ascii=False)[:200])
except Exception as e:
 fail("Register", str(e))

# 3. Login 
try:
 r = requests.post(BASE + "/auth/login", data={
 "username": "student1", "password": "test123456"
 }, timeout=5)
 data = r.json()
 token = data.get("access_token")
 if token:
 ok("Login", "token ")
 headers = {"Authorization": f"Bearer {token}"}
 else:
 fail("Login", json.dumps(data, ensure_ascii=False)[:200])
 headers = {}
except Exception as e:
 fail("Login", str(e))
 headers = {}

if not headers:
 # Fallback: try teacher1
 r = requests.post(BASE + "/auth/login", data={
 "username": "teacher1", "password": "test123456"
 }, timeout=5)
 data = r.json()
 token = data.get("access_token", "")
 headers = {"Authorization": f"Bearer {token}"} if token else {}

# 4. Me 
try:
 r = requests.get(BASE + "/auth/me", headers=headers, timeout=5)
 data = r.json()
 if data.get("code") == 0 and data["data"].get("username"):
 ok("Get Me", f"user={data['data']['username']}")
 else:
 fail("Get Me", json.dumps(data, ensure_ascii=False)[:200])
except Exception as e:
 fail("Get Me", str(e))

# 5-7. Courses 
for name, method, path, kw in [
 ("Courses List", "get", "/courses/", {}),
 ("Course Detail", "get", "/courses/1", {}),
 ("Course Sections", "get", "/courses/1/sections", {}),
]:
 try:
 fn = getattr(requests, method)
 r = fn(BASE + path, headers=headers, **kw, timeout=5)
 data = r.json()
 if data.get("code") == 0:
 ok(name)
 else:
 fail(name, json.dumps(data, ensure_ascii=False)[:200])
 except Exception as e:
 fail(name, str(e))

# 8-10. Membership 
for name, method, path, kw in [
 ("Membership Plans", "get", "/membership/plans", {}),
 ("Sand Pay", "post", "/membership/sandpay/1", {}),
 ("Purchase", "post", "/membership/purchase", {"data": {"plan_id": "1"}}),
]:
 try:
 fn = getattr(requests, method)
 r = fn(BASE + path, headers=headers, timeout=5, **kw)
 data = r.json()
 code = data.get("code", -1)
 if code == 0 or code == 1001: # 1001 = already purchased
 ok(name)
 else:
 fail(name, json.dumps(data, ensure_ascii=False)[:200])
 except Exception as e:
 fail(name, str(e))

# 11-12. Listening 
for name, method, path, kw in [
 ("Listening Courses", "get", "/listening/courses", {}),
 ("Subtitles", "get", "/listening/subtitles/1", {}),
]:
 try:
 fn = getattr(requests, method)
 r = fn(BASE + path, headers=headers, timeout=5, **kw)
 data = r.json()
 if data.get("code") == 0:
 ok(name)
 else:
 fail(name, json.dumps(data, ensure_ascii=False)[:200])
 except Exception as e:
 fail(name, str(e))

# 13. Review 
try:
 r = requests.get(BASE + "/review/due", headers=headers, timeout=5)
 data = r.json()
 if data.get("code") == 0:
 ok("Review Due")
 else:
 fail("Review Due", json.dumps(data, ensure_ascii=False)[:200])
except Exception as e:
 fail("Review Due", str(e))

# 14-15. Study 
for name, method, path, kw in [
 ("Study Total", "get", "/study/total", {}),
 ("Study Record", "post", "/study/record", {"data": {"course_id": "1", "section_id": "1", "duration_seconds": "300"}}),
]:
 try:
 fn = getattr(requests, method)
 r = fn(BASE + path, headers=headers, timeout=5, **kw)
 data = r.json()
 if data.get("code") == 0:
 ok(name)
 else:
 fail(name, json.dumps(data, ensure_ascii=False)[:200])
 except Exception as e:
 fail(name, str(e))

# Summary
print("=" * 50)
total = PASS + FAIL
print(f"=== : {total} | PASS : {PASS} | FAIL : {FAIL}")
if FAIL == 0:
 print(" !")
 sys.exit(0)
else:
 print(f"! FAIL : {FAIL/total*100:.1f}%")
 sys.exit(1)
