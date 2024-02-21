import re, ast

from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from dotenv import load_dotenv

load_dotenv()


class GenreGenAssistant:
    def __init__(self):
        self.interpreter_assistant = OpenAIAssistantRunnable.create_assistant(
            name="genre_gen_assistant",
            instructions="i want you make me music that Based on my previous music notes."
                         " suggestion is music note's range and each column can have multiple music note."
                         " music note is including #."
                         " number that i suggest 35 ~ 0 is match D2 ~ B4 and Beat is 8/8."
                         " empty list like this [] is empty beat."
                         " response format is must be like this suggestion = [['1', '2'], [], ['3', '4'], [], ['7']]",
            tools=[],
            model="gpt-3.5-turbo-16k"
        )

    def request_to_model(self, text_data):
        cnt = 0
        while cnt < 3:
            print(str(cnt) + "th attempt....")
            output = self.interpreter_assistant.invoke({"content": text_data})
            note_list = self.post_process(output[0].content[0].text.value)
            if note_list is not None:
                return note_list
            cnt += 1

        print("No notes found")
        return None

    def post_process(self, text_data):
        note_area = re.findall(r'\[\[.*\]\]', text_data)

        if note_area:
            result = [[int(num) if num.isdigit() else None for num in sublist] for sublist in
                      ast.literal_eval(note_area[-1])]
            return result


class ChordGenAssistant:
    def __init__(self):
        self.interpreter_assistant = OpenAIAssistantRunnable.create_assistant(
            name="chord_gen_assistant",
            # instructions=(
            #     f"in terms of Theory of Harmony, consider Interval and scales make me just one most proper lower-pitch chord in range D2 ~ B2 (35 ~ 24) based on my music note."
            #     f" suggestion's index is 1/8 beat and value is music note's range and each column can have multiple music note. music note is including #."
            #     f" number that i suggest 35 ~ 0 is match D2 ~ B4 and Beat is 8/8."
            #     f" empty list like this [] is empty beat. response format is must be like this suggestion = [['1', '2'], [], ['3', '4'], [], ['7']]"),
            instructions=(
                """
                in terms of Theory of Harmony, consider Interval and scales make me just one most proper lower-pitch chord in range D2 ~ B2 (35 ~ 24) based on my music note.
                suggestion's index is 1/8 beat and value is music note's range that match 35 ~ 0 to D2 ~ B4 which including # and each column can have multiple music note.
                basic Beat is 8/8.
                suggest me among first and each 4th column major, minor triad
                response format's is like this and notice that this is just example suggestion = [['35', '31', '28'], ['35', '31', '28'], ['35', '31', '28']] in this, inside array's each value is location of note must in range 35 ~ 24 and array's index is 0th, 4th, 8th ... location
                """
            ),

            tools=[],
            model="gpt-3.5-turbo-16k"
        )

    def request_to_model(self, text_data):
        cnt = 0
        while cnt < 3:
            print(str(cnt) + "th attempt....")
            output = self.interpreter_assistant.invoke({"content": text_data})
            note_list = self.post_process(output[0].content[0].text.value)
            if note_list is not None:
                return note_list
            cnt += 1

        print("No notes found")
        return None

    def post_process(self, text_data):
        note_area = re.findall(r'\[\[.*\]\]', text_data)

        if note_area:
            result = [[int(num) if num.isdigit() else None for num in sublist] for sublist in ast.literal_eval(note_area[-1])]
            return result
