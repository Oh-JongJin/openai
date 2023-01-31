import json
import urllib.request
import openai


papago_client_id = 'OK7Kx4_4mYQ73cdvl9wq'   # 파파고 API ID
papago_client_secret = 'n7VHviMSrC'     # 파파고 API secret 키
openai.api_key = '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'  # openai API 키


def papago(text: str, current_lang_type: str, convert_lang_type: str):
    encText = urllib.parse.quote(text)
    data = f'source={current_lang_type}&target={convert_lang_type}&text=' + encText
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", papago_client_id)
    request.add_header("X-Naver-Client-Secret", papago_client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result = response_body.decode('utf-8')
        d = json.loads(result)
        return d['message']['result']['translatedText']
    else:
        print(f'Error Code: {rescode}')


def generate_reponse(prompt):
    model_engine = 'text-davinci-003'   # OpenAI의 모델 종류 중 하나 / https://platform.openai.com/docs/models/overview
    prompt = f'{prompt}'

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message.strip()


while True:
    current_lang = None
    convert_lang = None
    user_input = input('User: ')    # 사용자 대화 입력 대기

    if user_input.upper() != user_input.lower():
        # 영어인지 한글인지 판별하는 간단한 조건문
        # 영어에는 대소문자 구별이 있기 때문에, 대문자와 소문자가 같지 않는 점을 이용하였다.
        current_lang = 'en'
        convert_lang = 'ko'
    else:
        current_lang = 'ko'
        convert_lang = 'en'

    if user_input == 'exit':    # 사용자가 exit를 입력하면 종료
        break

    response = generate_reponse(papago(user_input, current_lang, convert_lang))
    print(f'ChatGPT: {papago(response, convert_lang, current_lang)}')   # 영어로 물어보면 한글로 대답, 한글로 물어보면 영어로 대답
    print(f'ChatGPT: {papago(response, "en", "ko")}')   # 무조건 한글로 대답. 위 두 개중 쓰고싶은거 아무거나
