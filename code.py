import csv
from optimum.intel.openvino import OVModelForCausalLM
from transformers import AutoTokenizer, TextStreamer
import time
import threading
import keyboard
import re

def generate_text(model, tokenizer, prompt, tokens_per_second=3, max_new_tokens=8192):
    inputs = tokenizer(prompt, return_tensors="pt")

    class KeyboardStreamer(TextStreamer):
        def __init__(self, tokenizer, skip_prompt=True, **decode_kwargs):
            super().__init__(tokenizer, skip_prompt, **decode_kwargs)
            self.token_queue = []
            self.stop_flag = False
            self.print_thread = threading.Thread(target=self._print_tokens)
            self.print_thread.daemon = True
            self.print_thread.start()

        def put(self, value):
            self.token_queue.extend(value.tolist())

        def end(self):
            self.stop_flag = True
            self.print_thread.join()

        def _print_tokens(self):
            while not self.stop_flag or self.token_queue:
                if self.token_queue:
                    token = self.token_queue.pop(0)
                    decoded_text = self.tokenizer.decode(token, skip_special_tokens=True)
                    for char in decoded_text:
                        try:
                            keyboard.write(char)
                        except ValueError:
                            pass
                        time.sleep(1 / (tokens_per_second * 5))  # 속도 조절
                else:
                    time.sleep(0.05)

    streamer = KeyboardStreamer(tokenizer, skip_prompt=True)

    def generate_async():
        model.generate(
            **inputs,
            streamer=streamer,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
        )
        streamer.end()

    generation_thread = threading.Thread(target=generate_async)
    generation_thread.start()
    generation_thread.join()

    generated_text = ""  # 생성된 텍스트를 KeyboardStreamer에서 가져올 필요 없음.
    return generated_text
#
# def extract_tags(text):
#     """텍스트에서 네이버 블로그 스타일의 태그를 추출합니다."""
#     tags = re.findall(r"#\w+", text)
#     return " ".join(tags)

def main():
    model_id = "kimhyunwoo/gemma-2-2b-it-openvino-4bit"
    tokens_per_second = 3

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        ov_model = OVModelForCausalLM.from_pretrained(
            model_id=model_id,
            device="CPU",
            ov_config={"PERFORMANCE_HINT": "LATENCY", "NUM_STREAMS": "1"},
        )
    except Exception as e:
        print(f"모델 로드 중 오류 발생: {e}")
        return

    system_prompt = "당신은 블로그 글을 전문적으로 작성하는 작가입니다. 독자들이 이해하기 쉽고, 흥미를 느낄 수 있도록 글을 작성해주세요."

    with open("topics.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        topics = [row[0] for row in reader]

    for topic in topics:
        if keyboard.is_pressed('q'):
            print("\n프로그램을 종료합니다.")
            break

        print(f"\n\n'{topic}' 주제에 대한 글 생성 시작...")

        try:
            prompt = f"주제: {topic}\n\n"
            generated_text = generate_text(
                ov_model, tokenizer, prompt, tokens_per_second=tokens_per_second, max_new_tokens=8000
            )

            #  "주제:" 부분  제거, 시스템 프롬프트 관련 내용 제거
            generated_text = re.sub(r"^.*?주제:.*?\n\n", "", generated_text).lstrip()
            generated_text = re.sub(r"당신은.*작성해주세요\.", "", generated_text).lstrip()


            # tags = extract_tags(generated_text)
            # if tags: # KeyboardStreamer가 출력하므로 여기서 추가 출력 X
            #     generated_text += "\n\n" + tags

            print(f"\n\n'{topic}' 주제에 대한 글 생성 완료.") # 완료 메시지만 출력

        except Exception as e:
            print(f"\n글 생성 중 오류 발생: {e}")
            continue

if __name__ == "__main__":
    main()
