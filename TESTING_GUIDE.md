# Wovenry Manual Testing Guide

Use this guide to walk through every feature in the app and verify it works correctly. Each section has step-by-step instructions and expected results.

---

## Prerequisites

### 1. Environment Setup

```bash
cd <project-root>
cp .env.example .env        # edit .env with a real SECRET_KEY and optionally a GEMINI_API_KEY
source venv/Scripts/activate # Windows (Git Bash / MSYS2)
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt  # if a requirements file exists
python manage.py migrate
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/**.

### 2. Create Test Accounts

You need at least **two** test users to fully test permissions and social features.

**Option A — Use Django admin (if a superuser exists):**

```bash
python manage.py createsuperuser  # if you need one
```

Go to http://127.0.0.1:8000/admin/, then:
1. Under **Core > Allowed emails**, add two emails (e.g. `tester1@test.com`, `tester2@test.com`).
2. Register each account in the app (see section 1 below).

**Option B — From the Django shell:**

```bash
python manage.py shell
```

```python
from core.models import AllowedEmail
AllowedEmail.objects.create(email="tester1@test.com")
AllowedEmail.objects.create(email="tester2@test.com")
```

---

## Test Checklist

Use the Status column to track results: **PASS**, **FAIL**, or **SKIP**.

| #    | Test Case | Status |
|------|-----------|--------|
| 1.1  | Register with invited email | |
| 1.2  | Register with non-invited email (rejected) | |
| 1.3  | Register with duplicate username (rejected) | |
| 1.4  | Register with mismatched passwords (rejected) | |
| 1.5  | Login with valid credentials | |
| 1.6  | Login with wrong password (rejected) | |
| 1.7  | Logout | |
| 1.8  | Access any page while logged out (redirects to login) | |
| 2.1  | Create a project | |
| 2.2  | View project detail page | |
| 2.3  | Edit a project | |
| 2.4  | Delete a project | |
| 2.5  | Pin / unpin a project | |
| 2.6  | Make a project public (with 1-3 categories) | |
| 2.7  | Make a project public with 0 or >3 categories (rejected) | |
| 2.8  | Make a project private again | |
| 3.1  | Create a standalone metaprompt | |
| 3.2  | Create a metaprompt inside a project | |
| 3.3  | Edit a metaprompt | |
| 3.4  | Delete a metaprompt | |
| 3.5  | Pin / unpin a metaprompt | |
| 3.6  | Publish a metaprompt (draft -> published) | |
| 3.7  | Unpublish a metaprompt (published -> draft, auto-reverts to private) | |
| 3.8  | Make a published metaprompt public (with 1-3 categories) | |
| 3.9  | Make a published metaprompt public with 0 or >3 categories (rejected) | |
| 3.10 | Try to make a draft metaprompt public (should be blocked) | |
| 3.11 | Make a metaprompt private again | |
| 3.12 | AI auto-categorize (requires GEMINI_API_KEY in .env) | |
| 4.1  | Cockpit shows metaprompts tab by default | |
| 4.2  | Switch to projects tab | |
| 4.3  | Pinned items appear in "Pinned" section | |
| 4.4  | Unpinned items appear in "Recent" section | |
| 5.1  | Library: browse public projects | |
| 5.2  | Library: browse public metaprompts | |
| 5.3  | Library: search by keyword | |
| 5.4  | Library: filter by category | |
| 5.5  | Library: search + category filter combined | |
| 6.1  | View a public metaprompt in the Mixer | |
| 6.2  | Try to view a private metaprompt you don't own (403) | |
| 7.1  | Copy a public project to your account | |
| 7.2  | Copy a public metaprompt to your account | |
| 7.3  | Copied items are private drafts by default | |
| 8.1  | Report a project | |
| 8.2  | Report a metaprompt | |
| 8.3  | Toast confirmation appears after report | |
| 9.1  | Cannot view another user's private project (403) | |
| 9.2  | Cannot view another user's private metaprompt via Mixer (403) | |
| 9.3  | Cannot edit another user's project (404) | |
| 9.4  | Cannot edit another user's metaprompt (404) | |
| 9.5  | Cannot delete another user's project (404) | |
| 9.6  | Cannot delete another user's metaprompt (404) | |
| 9.7  | Project detail: non-owner only sees public metaprompts | |
| 10.1 | Sort metaprompts in project: newest, oldest, title | |

---

## Detailed Test Steps

### 1. Authentication

**1.1 Register with invited email**
1. Add `tester1@test.com` to AllowedEmail (see Prerequisites).
2. Go to `/auth/register/`.
3. Enter email `tester1@test.com`, pick a username and password.
4. **Expected:** Account created, redirected to Cockpit (home).

**1.2 Register with non-invited email**
1. Go to `/auth/register/`.
2. Enter an email NOT in AllowedEmail (e.g. `random@test.com`).
3. **Expected:** Form error: "This email is not on the invite list."

**1.3 Register with duplicate username**
1. Try registering with the same username as an existing user.
2. **Expected:** Form error: "Username already taken."

**1.4 Register with mismatched passwords**
1. Enter different values for password and password confirmation.
2. **Expected:** Form error: "Passwords do not match."

**1.5 Login with valid credentials**
1. Go to `/auth/login/`.
2. Enter correct username and password.
3. **Expected:** Redirected to Cockpit.

**1.6 Login with wrong password**
1. Enter correct username but wrong password.
2. **Expected:** Form error: "Invalid username or password."

**1.7 Logout**
1. Click logout (or go to `/auth/logout/`).
2. **Expected:** Redirected to login page.

**1.8 Access page while logged out**
1. While logged out, navigate to `/` or any other non-auth URL.
2. **Expected:** Redirected to `/auth/login/`.

---

### 2. Projects

**2.1 Create a project**
1. Go to `/projects/new/`.
2. Enter a title and optional description.
3. Submit.
4. **Expected:** Redirected to the new project's detail page.

**2.2 View project detail**
1. Click on a project from the Cockpit.
2. **Expected:** Project title, description, and metaprompt grid are displayed.

**2.3 Edit a project**
1. On the project detail page, click edit.
2. Change the title or description.
3. Submit.
4. **Expected:** Changes saved, redirected back to project detail.

**2.4 Delete a project**
1. On the project, click delete.
2. Confirm deletion.
3. **Expected:** Project removed, redirected to Cockpit. Project no longer listed.

**2.5 Pin / unpin a project**
1. Click the pin button on a project.
2. **Expected:** Project appears in the "Pinned" section on the Cockpit.
3. Click again to unpin.
4. **Expected:** Project moves back to "Recent".

**2.6 Make a project public**
1. On a project you own, click to change visibility to public.
2. A category modal should appear.
3. Select 1-3 categories and confirm.
4. **Expected:** Project is now public and appears in the Library.

**2.7 Reject invalid category count**
1. Try to make a project public but select 0 categories (or more than 3).
2. **Expected:** Error message: "Select 1 to 3 categories."

**2.8 Make a project private**
1. On a public project, change visibility back to private.
2. **Expected:** Project removed from Library. Category tags cleared.

---

### 3. Metaprompts

**3.1 Create a standalone metaprompt**
1. Go to `/metaprompts/new/`.
2. Fill in title, content, and description.
3. Submit.
4. **Expected:** Redirected to the metaprompt editor page.

**3.2 Create a metaprompt inside a project**
1. From a project detail page, click to add a new metaprompt (the URL will include `?project=<id>`).
2. Fill in the form and submit.
3. **Expected:** Metaprompt created and linked to that project.

**3.3 Edit a metaprompt**
1. Go to a metaprompt's editor page.
2. Change any field and save.
3. **Expected:** Changes persisted, page reloads with updated content.

**3.4 Delete a metaprompt**
1. Click delete on a metaprompt, confirm.
2. **Expected:** Metaprompt removed. If it was inside a project, redirected to that project's detail page. Otherwise, redirected to Cockpit.

**3.5 Pin / unpin a metaprompt**
1. Click pin on a metaprompt.
2. **Expected:** Appears in "Pinned" section on the Cockpit.

**3.6 Publish a metaprompt**
1. On a draft metaprompt's editor, click publish.
2. **Expected:** Status changes to "published".

**3.7 Unpublish a metaprompt**
1. On a published metaprompt, click to revert to draft.
2. **Expected:** Status changes to "draft", visibility automatically set to "private", category tags cleared.

**3.8 Make a published metaprompt public**
1. On a published metaprompt, change visibility to public.
2. Select 1-3 categories.
3. **Expected:** Metaprompt is now public, appears in the Library.

**3.9 Reject invalid category count on metaprompt**
1. Try to make a metaprompt public with 0 or >3 categories.
2. **Expected:** Error: "Select 1 to 3 categories."

**3.10 Try to make a draft metaprompt public**
1. On a draft metaprompt, attempt to set visibility to public.
2. **Expected:** Blocked. Redirected back to editor without changing visibility.

**3.11 Make a metaprompt private**
1. On a public metaprompt, switch visibility to private.
2. **Expected:** Removed from Library, category tags cleared.

**3.12 AI auto-categorize**
> Requires a valid `GEMINI_API_KEY` in `.env`. Skip if not configured.
1. On a metaprompt editor, click the AI categorize button.
2. **Expected:** 1-3 category suggestions appear, drawn from the existing category list.

---

### 4. Cockpit (Home Dashboard)

**4.1 Default tab is metaprompts**
1. Go to `/`.
2. **Expected:** The metaprompts tab is active by default.

**4.2 Switch to projects tab**
1. Click the projects tab.
2. **Expected:** Your projects are displayed (via HTMX tab switch).

**4.3 Pinned items**
1. Pin a project and a metaprompt.
2. **Expected:** They appear under a "Pinned" section in their respective tabs.

**4.4 Recent items**
1. **Expected:** Non-pinned items appear under a "Recent" section.

---

### 5. Library (Public Browsing)

**5.1 Browse public projects**
1. Go to `/library/projects/`.
2. **Expected:** All public projects are listed (from any user).

**5.2 Browse public metaprompts**
1. Go to `/library/metaprompts/`.
2. **Expected:** All public, published metaprompts are listed.

**5.3 Search by keyword**
1. Type a keyword into the search box.
2. **Expected:** Results filtered to items matching the keyword in title or description.

**5.4 Filter by category**
1. Click a category tag.
2. **Expected:** Only items tagged with that category are shown.

**5.5 Combined search + filter**
1. Enter a keyword AND select a category.
2. **Expected:** Results match both the keyword and the category.

---

### 6. Mixer (Metaprompt Viewer)

**6.1 View a public metaprompt**
1. Go to `/mixer/<id>/` for a public metaprompt.
2. **Expected:** Full metaprompt content displayed.

**6.2 View a private metaprompt you don't own**
1. Log in as a different user. Go to `/mixer/<id>/` for a private metaprompt.
2. **Expected:** 403 Forbidden page.

---

### 7. Social (Copy)

**7.1 Copy a public project**
1. From the Library or a public project detail page, click the copy button.
2. **Expected:** A new project titled "<Original> (Copy)" is created under your account, set to private.

**7.2 Copy a public metaprompt**
1. From the Mixer view of a public metaprompt, click the copy button.
2. **Expected:** A new metaprompt titled "<Original> (Copy)" is created under your account, set to private/draft.

**7.3 Verify copied items are private drafts**
1. Check your Cockpit after copying.
2. **Expected:** Copied items are private and (for metaprompts) in draft status.

---

### 8. Reporting

**8.1 Report a project**
1. On a public project, click the report button.
2. Enter a reason and submit.
3. **Expected:** Report created. Toast message: "Report submitted. Thank you."

**8.2 Report a metaprompt**
1. On a public metaprompt (Mixer), click the report button.
2. Enter a reason and submit.
3. **Expected:** Report created. Toast confirmation.

**8.3 Verify report in admin**
1. Go to `/admin/` > Core > Reports.
2. **Expected:** The report appears with correct reporter, target, and reason.

---

### 9. Permissions & Access Control

> These tests require **two user accounts** (User A = owner, User B = other).

**9.1 Private project: non-owner gets 403**
1. User A creates a private project, note the `<id>`.
2. User B navigates to `/projects/<id>/`.
3. **Expected:** 403 Forbidden page.

**9.2 Private metaprompt: non-owner gets 403 in Mixer**
1. User A creates a private metaprompt, note the `<id>`.
2. User B navigates to `/mixer/<id>/`.
3. **Expected:** 403 Forbidden page.

**9.3 Cannot edit another user's project**
1. User B navigates to `/projects/<id>/edit/` (User A's project).
2. **Expected:** 404 Not Found (the `owner=request.user` filter excludes it).

**9.4 Cannot edit another user's metaprompt**
1. User B navigates to `/metaprompts/<id>/edit/` (User A's metaprompt).
2. **Expected:** 404 Not Found.

**9.5 Cannot delete another user's project**
1. User B navigates to `/projects/<id>/delete/` (User A's project).
2. **Expected:** 404 Not Found.

**9.6 Cannot delete another user's metaprompt**
1. User B navigates to `/metaprompts/<id>/delete/` (User A's metaprompt).
2. **Expected:** 404 Not Found.

**9.7 Non-owner sees only public metaprompts in a public project**
1. User A creates a public project with 2 metaprompts: one public, one private.
2. User B views the project detail page.
3. **Expected:** Only the public metaprompt is visible.

---

### 10. Sorting

**10.1 Sort metaprompts in a project**
1. Go to a project detail page with multiple metaprompts.
2. Use the sort control to switch between: **newest**, **oldest**, **title**.
3. **Expected:** Metaprompt grid re-orders accordingly.

---

## Notes for Testers

- The app uses **HTMX** for interactive elements (tabs, pin buttons, search filtering, toasts). If something doesn't update dynamically, try a full page refresh to confirm the action went through.
- **AI categorize** (test 3.12) requires a valid Gemini API key. If the key is missing or invalid, the feature returns no suggestions silently.
- The **admin panel** (`/admin/`) is available for inspecting data directly (AllowedEmails, Projects, Metaprompts, Reports, Categories).
- All timestamps use `auto_now` / `auto_now_add`, so items should always show accurate creation/update times.
