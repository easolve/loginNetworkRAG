[드라이브](https://drive.google.com/drive/folders/17x5cZ__HzvwEHZf700g2rdtKbxAzJ3fw)

## 개발

- [ ] 테스트 환경 구성: 각 모듈에 `if __name__ == '__main__'`: 추가하여 테스트 가능한 환경 구성
- [x] [msw 가짜 운송장 번호 만들기](https://tracker.delivery/docs/dummy-tracking-number)
- [x] 스트림릿으로 ChatUI 만들기
- [ ] 대화 내용 요약
- [ ] SQLite 추가
  - [ ] 사용자 정보 저장
  - [ ] 회사 정보 저장
  - [ ] 대화 내용 저장
- [ ] 랭그래프 공부
  - [ ] 책 읽기
  - [ ] [QuickStart 이해하기](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
  - [ ] [ToolNode 완벽 이해](https://langchain-ai.github.io/langgraph/how-tos/tool-calling/#define-tools)
  - [ ] [대화 내용 요약](https://github.com/langchain-ai/langchain/discussions/25904?utm_source=pocket_shared)
  - [ ] [컨셉](https://langchain-ai.github.io/langgraph/concepts/)
  - [ ] [리듀서](https://langchain-ai.github.io/langgraph/concepts/low_level/#default-reducer)
  - [ ] [](https://langchain-ai.github.io/langgraph/concepts/persistence/)
  - [ ] [](https://langchain-ai.github.io/langgraph/concepts/low_level/)
  - [ ] [](https://langchain-ai.github.io/langgraph/how-tos/configuration/)
- [ ] 파일 구조 참고하기
  - [ ] [JoshuaC215/agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit/tree/main)
  - [ ] [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund)

## 데이터 처리

- [ ] 메뉴얼 작성

## 2월 8일 인수인계

`feat/dev/enhancedChatbot/#1` => `feat/#1/addDummyTools/#4` 순으로 작업

### feat/dev/enhancedChatbot/#1

```bash
query_analysis
├── query_retriever
│
└── query_checker: 질문을 좀 더 정확하게 검사. 검사 결과는 yes, hold, no로 나뉨
```

query_analysis Node를 query_retriever와 query_checker Node로 나누고 query_checker Noder가 질문을 좀 더 정확하게 검사합니다. 검사 결과는 yes, hold, no 로 나뉘며 yes: cc_agent Node, hold일 경우 상담사 호출, no: login network와 완전 관계 없는 질문으로 생각하고 나눴습니다.

구글 드라이브에 manual_adv 스프레드 시트를 만들었습니다.
기존의 manual.csv를 manual_bef.csv로 두고 새로운 manual.csv를 만들었습니다.
현재의 manual.csv는 request(similar_input), response, manual, info 로 나뉘는데 이를 state의 similar_manual에 저장한 후 cc_agent에서 manual과 similar_input을 보고 처리를 합니다.

manual_adv 스프레드 시트 우측에 어떤 tools 가 필요한지 정의해두었습니다. 이를 바탕으로 몇 개의 tool을 추가해 놓았습니다.

`README.md`에 적어놓았다시피 혹시모를 충돌을 피하기 위해 test폴더와 test 파일을 main으로 만들어 진행했습니다. 추후 main과 합병해도 괜찮을 것 같습니다.

아래는 그렇게 1번 branch에서 질의한 결과물입니다.

```bash
query: 개인정보 오류 관련해서 문자를 받았어요., similar: 개인정보 오류 관련해서 알림톡 받았는데 확인해주세요 score: yes
답변: 개인정보 오류 관련 알림톡을 받으셨군요. 확인을 위해 운송장 번호와 함께 주민등록번호 또는 개인통관고유부호를 입력해 주시겠어요?
질문을 입력하세요 (종료하려면 'q' 입력): # 개인정보 오류 관련 알림톡이 왔습니다. 운송장번호는 324234 이고 통관번호는 2345346이에요.
query: # 개인정보 오류 관련 알림톡이 왔습니다. 운송장번호는 324234 이고 통관번호는 2345346이에요., similar: 개인정보 오류 관련해서 알림톡 받았는데 확인해주세요 score: yes
답변: 입력해 주신 정보를 바탕으로 수입신고를 진행하였습니다. 수입신고가 성공적으로 완료되었습니다. 추가로 궁금한 점이 있으시면 언제든지 문의해 주세요!
질문을 입력하세요 (종료하려면 'q' 입력): 오늘 날씨가 어때요?
query: 오늘 날씨가 어때요?, similar: 세관 검사 시점 ex) 세관 검사는 언제 되나요? score: no
답변: 검색 결과가 없습니다.
```

선코님한테 말한 `[FIX] Retriever 툴에 문맥 정리해서 invoke하기 #5` 이슈 해결하면 성능 더 좋아질 것 같습니다.

### feat/#1/addDummyTools/#4

`feat/dev/enhancedChatbot/#1`를 dev에 안합치고 여기서 포크 따서 작업중입니다.
몇몇 프롬프트를 수정했고 드라이브의 manual_adv 우측 tools에 있는 내용을 껍데기만 구현, ToolNode에 넣어 놓아서 호출하도록 만들었습니다.

현재 질문하면 무한루프 도는 에러가 있고 프롬프트를 수정하거나 END 분기점을 확실히 정하는 방식으로 무한루프를 고쳐야 합니다.(중요!!)

무한루프 먼저 고치고 `[FIX] Retriever 툴에 문맥 정리해서 invoke하기 #5` 이슈 해결하면 좋을 것 같습니다.

## 2월 9일 인수인계

```bash
User: 배송 조회할게요.
Chatbot: 배송 조회를 도와드릴게요. 운송장 번호를 입력해주세요.
User: 1234567890
-> 운송장 번호 조회 툴 무한루프
```

이유:

- `query_checker`에 이전까지의 대화 내용을 추가하여 운송장 번호를 입력 시 `yes`로 인식하게 만들었음
- `cc_agent`에서 보내는 자료형 `info`에 운송장 번호 조회 시 필요없는 정보를 계속 요구하여 무한루프가 발생함
  ```bash
      res = chain.invoke(
        {
            "messages": messages,
            "similar_input": retrieved["similar_input"],
            "manual": retrieved["manual"],
            "info": retrieved["info"],
        }
    )
  ```
