relevance_and_harmfulness_prompt = (
    "You are an interviewer evaluating a candidate's response. The response is: '{response}'\n"
    "Evaluate the response on the following criteria:\n"
    "1. Is the response clear and related to the question asked? Reply with 'true' or 'false'.\n"
    "2. Is the response appropriate and professional? Reply with 'true' or 'false'.\n"
    "Provide your evaluation below."
)

additional_answers_prompt = (
    "Evaluate the following candidate response: \"{response}\". "
    "Identify any other unanswered questions from the following list that the response addresses: {unanswered_questions}. "
    "Provide a list of questions that are answered by the candidate's response."
)

next_question_prompt = (
    "Given the candidate's response: \"{response}\", and the list of unanswered questions: {unanswered_questions}, "
    "generate the next relevant interview question. Ensure the question maintains context, avoids repetition, "
    "and is relevant to the topics discussed so far."
)

avoid_repeating_questions_prompt = (
    "The user just answered: {response}\n"
    "Here are the questions that have already been answered: {answered_questions}\n"
    "Here are the questions that need to be asked: {unanswered_questions}\n"
    "Based on the user's recent response and the context of the conversation, ask the next relevant question from the list of unanswered questions. "
    "Ensure not to repeat any questions and keep the flow natural and contextual. If the user's response already addresses any unanswered question, skip that question."
)