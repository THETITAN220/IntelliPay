# from dotenv import load_dotenv
# import os
# from mistralai import Mistral

# load_dotenv()
# # Initialize Mistral client
# api_key = os.environ["BfcNrvpRr2n0aMxL2mSDJoQzSaBxZQxB"]
# model = "mistral-large-latest"
# client = Mistral(api_key=api_key)

# def handle_response(text: str) -> str:
#     try:
#         chat_response = client.chat.complete(
#             model=model,
#             messages=[
#                 {"role": "user", "content": text},
#             ]
#         )
#         # Extract and return the model's response
#         return chat_response.choices[0].message.content
#     except Exception as e:
#         print(f"Error calling Mistral API: {e}")
#         return "Sorry, I couldn't process your request right now."
