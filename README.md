# 🤖 AI 블로그 글 자동 생성기 (OpenVINO 기반)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

이 프로젝트는 인텔 OpenVINO 툴킷을 사용하여 최적화된 Gemma-2-2b-it 모델을 활용하여 자동으로 블로그 글을 생성하는 프로그램입니다.  `topics.csv` 파일에 있는 주제들을 읽어와 각 주제에 맞는 블로그 글을 생성하고, 실시간으로 타이핑하는 듯한 효과를 주며 출력합니다.

## ✨ 주요 특징

*   **OpenVINO 최적화:** 인텔 OpenVINO를 사용하여 모델 추론 속도를 최적화하여, CPU 환경에서도 빠른 글 생성이 가능합니다.
*   **실시간 타이핑 효과:** `KeyboardStreamer`를 통해 생성되는 글이 마치 사람이 직접 타이핑하는 것처럼 실시간으로 출력됩니다.  `keyboard.write()`를 사용하므로,  출력되는 즉시 다른 곳에 복사-붙여넣기가 가능합니다.
*   **주제 기반 글 생성:** `topics.csv` 파일에 원하는 주제들을 나열하여, 각 주제에 대한 블로그 글을 순차적으로 생성할 수 있습니다.
*   **간편한 종료:**  글 생성 중에 'q' 키를 누르면 언제든지 프로그램 실행을 중단할 수 있습니다.
*   **태그 추출 (주석 처리):**  생성된 텍스트에서 네이버 블로그 스타일의 태그를 자동으로 추출하는 기능이 포함되어 있습니다 (현재는 주석 처리됨).  `extract_tags` 함수를 참고하세요.
*   **후처리:** 생성된 텍스트에서 "주제:" 부분, 시스템 프롬프트 관련 불필요한 부분을 제거합니다.

## ⚙️ 실행 환경 및 요구 사항

*   **운영체제:** Windows (테스트 환경), Linux, macOS (KeyboardStreamer 호환성 확인 필요)
*   **프로세서:** Intel CPU (i7 8세대 이상 권장)
*   **메모리:** 8GB RAM 이상 권장 (테스트 환경: 8GB)
*   **Python 버전:** 3.8 이상
*   **라이브러리:**
    *   `optimum-intel`:  `pip install optimum-intel[openvino]`
    *   `transformers`: `pip install transformers`
    *   `keyboard`: `pip install keyboard`
    *   `accelerate`: `pip install accelerate` (필요한 경우)

## 🚀 설치 및 실행 방법

1.  **저장소 복제:**

    ```bash
    git clone https://github.com/[your-github-username]/[your-repository-name].git
    cd [your-repository-name]
    ```
     (GitHub에 올린 후에는 `[your-github-username]`과 `[your-repository-name]`을 실제 저장소 정보로 바꿔주세요.)

2.  **필수 라이브러리 설치:**

    ```bash
    pip install optimum-intel[openvino] transformers keyboard accelerate
    ```

3.  **`topics.csv` 파일 준비:**

    *   프로젝트 루트 디렉토리에 `topics.csv` 파일을 생성합니다.
    *   CSV 파일의 첫 번째 열에 블로그 글 주제를 한 줄에 하나씩 작성합니다.  예:
        ```csv
        주제
        인공지능 기술의 미래
        맛있는 커피 레시피
        여름 휴가 추천 여행지
        ```

4.  **프로그램 실행:**

    ```bash
    python main.py
    ```

5. **(선택) 태그 추출 기능 활성화:**
  *   `main.py` 파일에서 `extract_tags` 함수 관련 주석을 해제하고,  `tags` 변수 관련 출력 부분의 주석을 해제하면, 생성된 글 하단에 추출된 태그를 함께 출력합니다.

## 🤝 기여

버그 수정, 기능 개선, 성능 향상 등 어떤 형태의 기여도 환영합니다. Pull Request를 통해 기여해주세요!

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고해주세요.

## ❓ FAQ

*   **Q: 글 생성 속도가 너무 느립니다.**
    *   A: `tokens_per_second` 값을 조절하여 출력 속도를 변경할 수 있습니다.  `ov_config`의 `NUM_STREAMS` 값을 조정하거나, 더 강력한 CPU를 사용하는 것도 고려해볼 수 있습니다.
*   **Q:  생성되는 글의 품질이 만족스럽지 않습니다.**
    *    A:  `generate_text` 함수 내의 `temperature`, `top_p`, `repetition_penalty` 등의 파라미터를 조절하여 생성되는 텍스트의 다양성과 품질을 조절할 수 있습니다.  `system_prompt`를 수정하여 모델에게 더 구체적인 지시를 내릴 수도 있습니다.
* **Q: `KeyboardStreamer`가 특정 운영체제에서 작동하지 않습니다.**
    * A: `keyboard` 라이브러리는 운영체제에 따라 호환성 문제가 있을 수 있습니다. `keyboard.write()` 대신 `print()`를 사용하여 표준 출력으로 텍스트를 출력하도록 수정할 수 있습니다.
* **Q: 모델 로드 중 오류가 발생합니다.**
    * A: `huggingface-cli login` 명령어를 실행하여 Hugging Face 계정에 로그인하고, `kimhyunwoo/gemma-2-2b-it-openvino-4bit` 모델에 대한 접근 권한을 확인해주세요.

## 📝 TODO

*   GUI 인터페이스 추가
*   다양한 모델 지원 (Gemma 외 다른 모델)
*   글 생성 옵션 다양화 (글 스타일, 어조 등)
*   생성된 글 자동 저장 기능
