from main import run_agent
import asyncio

if __name__ == '__main__':
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


