🔄Complete Data Flow(Submit Bug)

User fills form → clicks "Submit Bug Report"
        ↓
handleSubmit() runs
        ↓
fetch('POST /api/reports/', body: formData JSON)
        ↓
Django URL router → BugReportViewSet.create()
        ↓
Serializer validates + deserializes JSON
        ↓
BugReport object → database save
        ↓
Response: { id: 42, title: "...", ... }
        ↓
React: setSubmittedBugId(data.id) → shows success screen

🤖 Complete Data Flow — AI Review
User clicks "Review Bug"
        ↓
handleReview() runs
        ↓
fetch('POST /api/reports/42/ai-review/')
        ↓
Django → ai_review() action method
        ↓
DB बाट bug fetch → Claude API मा पठाउँछ
        ↓
Claude ले analysis गरेर text return गर्छ
        ↓
ai_review field मा save → Response पठाउँछ
        ↓
React: message list मा AI response add हुन्छ
        ↓
setReviewed(true) → "Review complete" देखाउँछ