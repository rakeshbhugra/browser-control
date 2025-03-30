import os, sys, time, asyncio, litellm, copy
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

class CustomException(Exception):
    def __init__(self, data):
        self.data = data

async def make_sure_messages_dont_exceed_100k(messages):
    completion_messages = copy.deepcopy(messages)
    if messages and "content" in messages[-1]:
        messages[-1]["content"] = messages[-1]["content"][:100000]
    return completion_messages

async def handle_other_roles(messages):
    messages_copy = []
    for message in messages:
        role = message.get("role")
        if role not in ['system', 'user', 'assistant']:
            content = f'[{role}]: {message["content"]}'
            messages_copy.append({'role': 'assistant', 'content': content})
        else:
            messages_copy.append(message)
    return messages_copy

async def get_openai_completion(messages, model, metadata, temperature=0, stream=False):
    t0 = time.time()
    try:
        completion = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream,
            metadata=metadata
        )
        t1 = time.time()
        print(f"Time taken for get_openai_completion: {t1 - t0}")
        return completion
    except Exception as e:
        print(f"Failed to connect to OpenAI API for model {model}: {e}")
        raise

async def get_chat_response(messages, metadata, temperature=0, model="gpt-4o-mini", stream=False):
    # with open('last_model_used.txt', 'a') as f:
    #     f.write(f"{model}\n")
    completion_messages = await make_sure_messages_dont_exceed_100k(messages)
    completion_messages = await handle_other_roles(completion_messages)
    # model = "voa-gpt4-2"
    # Define the fallback models in order
    fallback_models = [
        model,        # Desired initial model
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-4-turbo"         # Final fallback
    ]
    # To track if we've already retried once
    max_retries = 1
    attempt = 0
    retry_wait_time = 2

    while attempt <= max_retries:
        for model_itr in fallback_models:
            try:
                completion = await get_openai_completion(completion_messages, model_itr, metadata, temperature, stream)

                if not stream:
                    try:
                        if completion.choices[0].finish_reason == "content_filter":
                            filter_reason = []
                            content_filter_results = completion.choices[0].content_filter_results
                            for filter_key in content_filter_results:
                                if content_filter_results[filter_key]["filtered"]:
                                    filter_reason.append(filter_key)
                            filter_reason_str = ",".join(filter_reason)
                            error_message = f"content filter has been triggered, message seems: {filter_reason_str} in nature"
                            print(error_message)
                            messages[-1]["content"] += "{%s}" % (error_message)
                            # Restart the process with the initial model
                            raise CustomException("Content filter triggered")
                    except AttributeError:
                        print("Failed to check content filter")

                if stream:
                    return completion
                else:
                    return completion.choices[0].message.content

            except CustomException as ce:
                # Handle custom exceptions like content filter
                print(f"Custom exception encountered: {ce.data}")
                # Decide whether to retry or not based on the exception
                if attempt < max_retries:
                    print("Retrying with fallback models...")
                    break  # Break to retry the fallback models
                else:
                    raise
            except Exception as e:
                print(f"Error with model {model}: {e}")
                # Continue to the next model in the fallback list

        else:
            # If all models have been tried and none succeeded
            attempt += 1
            if attempt > max_retries:
                print("All fallback models failed after retrying.")
                raise CustomException("All fallback models failed.")
            else:
                print("Retrying the entire process...")
                # Optionally, add a delay before retrying
                await asyncio.sleep(retry_wait_time)

    # If the loop exits without returning, raise an exception
    raise CustomException("Failed to get a successful completion after retries.")


async def tool_response(system_init_message, user_input, metadata, temperature=0, model="gpt-4o-mini", stream=False):
    response = await get_chat_response([
        {"role": "system", "content": str(system_init_message)},
        {"role": "user", "content": str(user_input)}
    ], metadata, temperature=temperature, model=model, stream=stream)
    return response
