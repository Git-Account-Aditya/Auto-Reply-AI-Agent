from main import run_agent
from gmail_service import GmailService
import asyncio

def manual_mode():
    print('Enter an input to generate response')
    text = input('You : ')
    try:
        if not text:
            print("Please enter some text.")
        response = asyncio.run(run_agent(text))
        if response is not None and 'input_type' in response:
            if response['input_type'] is None:
                print('can not recognize the type of text')
            else:
                if response['input_type'] == 'email':
                    meta_data = response.get('email_data', {}).get('diagnose')
                    data = response.get('reply')
                    print(meta_data, data)
                elif response['input_type'] == 'review':
                    meta_data = response.get('review_data', {}).get('diagnose')
                    data = response.get('reply')
                    print(meta_data, data)
        else:
            print('Some keys are missing, can not generate any response.')
    except (EOFError, KeyboardInterrupt):
        print("\nExiting. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")

def gmail_mode():
    gmail = GmailService()
    emails = gmail.get_unread_emails(max_results=3)
    for email_data in emails:
        print(f"\nFrom: {email_data['sender']}\nSubject: {email_data['subject']}\nBody:\n{email_data['body']}")
        email_content = f"Subject: {email_data['subject']}\n\n{email_data['body']}\n\nFrom: {email_data['sender']}"
        response = asyncio.run(run_agent(email_content))
        reply = response.get('reply')
        if isinstance(reply, dict):
            print(f"\nGenerated Reply:\nTo: {reply.get('to')}\nSubject: {reply.get('subject')}\nBody:\n{reply.get('body')}")
            approve = input("Send this reply? (y/n): ").strip().lower()
            if approve == 'y':
                gmail.send_email(
                    to=reply.get('to', email_data['sender']),
                    subject=reply.get('subject', f"Re: {email_data['subject']}"),
                    body=reply.get('body', ''),
                    thread_id=email_data['thread_id']
                )
                gmail.mark_as_read(email_data['id'])
                print("Sent and marked as read.")
            else:
                print("Skipped.")
        else:
            print("No valid reply generated.")

def main():
    print("1. Manual input\n2. Gmail integration\n3. Exit")
    while True:
        choice = input("Choose: ").strip()
        if choice == '1':
            manual_mode()
        elif choice == '2':
            gmail_mode()
        elif choice == '3':
            break

if __name__ == '__main__':
    main()


