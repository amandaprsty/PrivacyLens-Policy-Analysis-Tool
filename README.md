## PrivacyLens: Policy Analysis Tool - README

URL to Deployed Application: https://ewtxfayvgednowu4fk28db.streamlit.app/ 

Note: Ensure you provide your own API credentials in the sidebar to enable all features.

## Test Case: Privacy Policy Upload and Analysis
# Purpose
This test demonstrates the core functionality of PrivacyLens: uploading a privacy policy document and using AI to ask questions based on its content.

# Steps to Run
1. Open the deployed application using the URL above.
2. Upload a sample privacy policy document provided in /test_artifacts:
<unimelb_privacy_policy.pdf>
3. Wait for the document to be processed (this may take a few seconds).
4. Ask a question in the text input box:
"Is the university's employee phone number covered in this privacy policy?"
5. Verify the response: Confirm that the AI generates a relevant and concise answer based on the document’s content.

## Expected Result
1. The uploaded document is processed successfully.
2. The AI responds with accurate and relevant answers to the question, such as whether the phone number of university employees is covered under the policy.

## Test Artefacts
Sample Privacy Policy Document
Location: /test_artifacts/unimelb_privacy_policy.pdf

Use this document to test the upload and analysis feature. You may also upload any other valid privacy policy (PDF or TXT) for further testing.