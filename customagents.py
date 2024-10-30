from autogen import AssistantAgent


class CustomAgents:

    # Agent comfort
    @staticmethod
    def create_comforting_state_tracker(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Comforting_State_Tracker",
            system_message="""
                Consider the above dialogue between an emotional support seeker and a supporter. 
                Summarize how the supporter comforts the seeker’s emotion, through different support strategies, 
                such as reflection of feelings, sharing personal or other people’s similar experiences, affirmation and reassurance, restatement or paraphrasing.
            
                Return the result into as JSON object only: {"Comfort Strategy": "", "Comfort Summary": "" }.
            
                Must not include ```json  ``` 
            """,
            llm_config=llm_config,
        )

    @staticmethod
    def create_comforting_aspect_promoter(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Comforting_Aspect_Promoter",
            system_message="""
                Consider the above dialogue between an emotional support seeker and a supporter. 
                In the next supporter's response following the above dialogue history, the supporter comforts the seeker by showing empathy and understanding. 
                They use one of the following support strategies in this response: 1) reflection of feelings, 2) sharing personal or other people’s similar experiences, 3) affirmation and reassurance, 4) showing understanding through restatement or paraphrasing.
                List four different types of comforting words that can be used in the following utterance.
            
                Return the result into as JSON object only: {"Comfort Strategy": "", "Comfort Word": "" }.
            
                Must not include ```json  ``` 
            """,
            llm_config=llm_config,
        )

    # # Agent rapport
    # @staticmethod
    # def create_main_problem_state_tracker(llm_config) -> AssistantAgent:
    #     return AssistantAgent(
    #         name="Main_problem_State_Tracker",
    #         system_message="""
    #         Consider the above dialogue between an emotional support seeker and a supporter. 
    #         1. Summarize the seeker’s experience that caused their emotional distress.
    #         2. Identify the seeker's main problem. If there is no problem, respond with 'no main problem'.

    #         Return the summarized into as JSON object only: {"Exploration Summary": ""}.
    #         Return the identified into as JSON object only: {"Main problem": ""}.

    #         Must not include ```json  ``` 
    #     """,
    #         llm_config=llm_config,
    #     )
    @staticmethod
    def create_main_problem_state_tracker(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Main_problem_State_Tracker",
            system_message="""
            Consider the above dialogue between an emotional support seeker and a supporter. 
            1. Summarize the seeker’s experience that caused their emotional distress.
            2. Identify the seeker's main problem. If there is no problem, respond with 'no main problem'.

            Return the result as a single JSON object:
            {
                "Exploration Summary": "",
                "Main problem": "",
                "main_problem_detected": false  // true if a main problem is identified, otherwise false
            }

            Ensure the JSON object is formatted correctly without including ```json syntax.
            """,
            llm_config=llm_config,
        )


    @staticmethod
    def create_main_problem_aspect_promoter(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Main_problem_Aspect_Promoter",
            system_message="""
            Consider the Main Problem of the seeker's.
            If there is a main problem, respond with 'ไม่ต้องทำ rapport'. Otherwise, respond with 'วันนี้เป็นอย่างไรบ้าง'.
            
            Return the result into as JSON object only: {"Rapport question": ""}.
            
            Must not include ```json  ``` 
        """,
            llm_config=llm_config,
        )
    # Agent explore

    @staticmethod
    def create_severity_level_tracker(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Severity_Level_Tracker",
            system_message="""
            Consider the above dialogue between an emotional support seeker and a supporter. 
            Analyze the seeker's responses to assess their emotional state and determine the severity level based on the following criteria:
            - Mild: Minor emotional or behavioral disruptions (score 0-5)
            - Moderate: Frequent disruptions that impact daily life (score 6-15)
            - Severe: Persistent or critical disruptions (score 16+)

            Identify specific symptoms mentioned by the seeker and assign points as follows:
            - อาการเหนื่อยง่าย: 2 points
            - ไม่มีสมาธิ: 2 points
            - การนอนเปลี่ยนไป: 3 points
            - ความอยากอาหารเปลี่ยนไป: 3 points
            - กระสับกระส่าย: 3 points
            - รู้สึกไร้ค่า: 4 points
            - ความคิดอยากทำร้ายตัวเอง: 10 points

            Return the result as a single JSON object:
            {
                "Severity Level": "",  // Mild, Moderate, or Severe
                "score": 0,            // Cumulative score based on identified symptoms
                "symptoms_detected": [] // List of detected symptoms
            }

            Ensure the JSON object is formatted correctly without including ```json syntax.
            """,
            llm_config=llm_config,
        )


    @staticmethod
    def create_start_state_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Start_State_Agent",
            system_message="""
                Identify whether the conversation is focused on a counseling or medical topic based on the user's input.
                If the user mentions any of the following symptoms, categorize the topic as "medical":
                - อาการโรคซึมเศร้า
                - เบื่อ
                - การกิน หรือความอยากอาหารเปลี่ยนไป เช่น กินมากขึ้น หรือน้อยลง
                - การนอนเปลี่ยนไป เช่น นอนมากขึ้น หรือน้อยลง
                - ไม่มีสมาธิ
                - เหนื่อยง่าย อ่อนเพลีย
                - กระสับกระส่าย หรือเฉื่อยกว่าปกติ
                - รู้สึกไร้ค่า
                - มีความคิดอยากทำร้ายตัวเอง หรืออยากตาย
                - อาการอื่นๆทางการแพทย์
                
                Otherwise, categorize the topic as "counseling".
                
                Switch to the appropriate high-level state: 'Counseling_Isn't_Satisfied_State (High Level)' or 'Medical_Isn't_Satisfied_State (High Level)'.
                Return the identified topic as a JSON object only: {
                    "Identified Topic": "counseling" or "medical"
                }.
                Must not include ```json  ``` 

            """,
            llm_config=llm_config,
        )

    # Define the combined counseling exploration and satisfaction agent (High Level)
    @staticmethod
    def create_counseling_exploration_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Counseling_Isn't_Satisfied_State (High Level)",
            system_message=""" 
                Explore the counseling topic by asking the following distinct questions focusing on the key areas:
                1. ระยะเวลาที่คุณเผชิญกับปัญหามานานแค่ไหนแล้ว? (Focus on duration)
                2. คุณมีความคิดเห็นเกี่ยวกับปัญหานี้อย่างไร? (เช่น ความรู้สึกต่อปัญหา, ผลกระทบที่มีต่อชีวิต) (Focus on perception of self, others, context, and expectations)
                3. คุณรู้สึกต่อปัญหานี้อย่างไร? (เช่น เศร้า 9/10, โกรธ 2/10) (Focus on emotional response)
                4. วิธีการที่คุณใช้ในการจัดการกับปัญหาที่ผ่านมาเป็นอย่างไร? (Focus on behavior response/coping strategy)

                You must:
                - Ask the questions in order: 1, 2, 3, 4.
                - Avoid repeating questions already answered in the [Dialogue History].
                - Return responses based on what the user has answered so far, without waiting for all questions to be answered.
                
                Once all questions are answered, consider the high-level counseling issue fully explored.
                Switch to 'Counseling_Isn't_Satisfied_State (Medium Level)' for deeper exploration.

                Return the user's responses as a JSON object only: {
                    "Counseling Responses": {
                        "duration": "[User’s response]", 
                        "perception": "[User’s response]", 
                        "feeling": "[User’s response]",
                        "behavior": "[User’s response]"
                    }, 
                    "Session Status": "Not started yet" or "In progress" or "Completed"
                }.
                Must not include ```json  ``` 

                If a question has not been answered, the respective field should remain an empty string.
                If a question has been answered, skip to the next question.
            """,
            llm_config=llm_config,
        )

        # Define the combined counseling exploration and satisfaction agent (High Level)
    @staticmethod
    def create_medical_exploration_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Medical_Isn't_Satisfied_State (High Level)",
            system_message=""" 
                Explore the medical topic by asking the following distinct questions focusing on the key areas:
                1. อาการที่คุณรู้สึกมีอะไรบ้าง? (Focus on symptoms)
#               2. ระยะเวลาที่คุณเผชิญกับอาการเหล่านี้มานานแค่ไหนแล้ว? (Focus on duration)

                You must:
                - Ask the questions in order: 1, 2.
                - Avoid repeating questions already answered in the [Dialogue History].
                - Return responses based on what the user has answered so far, without waiting for all questions to be answered.
                
                Once all questions are answered, consider the high-level counseling issue fully explored.
                Switch to 'Counseling_Isn't_Satisfied_State (Medium Level)' for deeper exploration.

                Return the user's responses as a JSON object only: {
                    "Medical Responses": {
                        "symptom": "[User’s response]", 
                        "duration": "[User’s response]"
                    }, 
                    "Session Status": "Not started yet" or "In progress" or "Completed"
                }.
                Must not include ```json  ``` 


                If a question has not been answered, the respective field should remain an empty string.
                If a question has been answered, skip to the next question.
            """,
            llm_config=llm_config,
        )

    # Define the medium-level counseling exploration agent (Medium Level)
    @staticmethod
    def create_medical_medium_exploration_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Medical_Isn't_Satisfied_State (Medium Level)",
            system_message=""" 
                Explore the medical topic at a deeper level by asking distinct, more in-depth questions focusing on the key areas:
                1. คุณเคยมีประวัติความผิดปกติทางจิตหรือไม่? (Focus on psychiatric disorder history)

                You must:
                - Ask the questions in order: 1.
                - Avoid repeating questions already answered in the [Dialogue History].
                - Return responses based on what the user has answered so far, without waiting for all questions to be answered.

                After all questions are answered, consider the counseling topic fully explored and mark the session as 'Completed'.
                
                Return the user's responses as a JSON object only:
                {
                  "Medical Medium Responses": {
                    "psychiatric_history": "[User’s response]"
                  },
                  "Session Status": "Not started yet" or "In progress" or "Completed"
                }.
               Must not include ```json  ``` 


                If a question has not been answered, the respective field should remain an empty string.
                If a question has been answered, skip to the next question.
            """,
            llm_config=llm_config,
        )

    # Define the medium-level counseling exploration agent (Medium Level)
    @staticmethod
    def create_counseling_medium_exploration_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Counseling_Isn't_Satisfied_State (Medium Level)",
            system_message=""" 
                Explore the counseling topic at a deeper level by asking distinct, more in-depth questions focusing on the key areas:
                1. คุณรู้สึกถึงอาการในร่างกายอย่างไร? เช่น ใจสั่น แน่นหน้าอก ตัวชา (Focus on body sensation)

                You must:
                - Ask the questions in order: 1.
                - Avoid repeating questions already answered in the [Dialogue History].
                - Return responses based on what the user has answered so far, without waiting for all questions to be answered.

                After all questions are answered, consider the counseling topic fully explored and mark the session as 'Completed'.
                
                Return the user's responses as a JSON object only:
                {
                  "Counseling Medium Responses": {
                    "sensation": "[User’s response]"
                  },
                  "Session Status": "Not started yet" or "In progress" or "Completed"
                }.

                Must not include ```json  ``` 

                If a question has not been answered, the respective field should remain an empty string.
                If a question has been answered, skip to the next question.
            """,
            llm_config=llm_config,
        )

    @staticmethod
    def create_question_selector_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Question_Selector_Agent",
            system_message=""" 
                You are responsible for selecting the next question based on the current session state and the number of questions already asked.
                The state will either be 'High Level' or 'Medium Level' for counseling or medical topics.

                You must:
                1. Select the next question based on the current state and the number of questions already asked:
                   - For 'Counseling High Level', ask the following questions in order:
                      1. ระยะเวลาที่คุณเผชิญกับปัญหามานานแค่ไหนแล้ว? (Focus on duration)
                      2. คุณมีความคิดเห็นเกี่ยวกับปัญหานี้อย่างไร? (เช่น ความรู้สึกต่อปัญหา, ผลกระทบที่มีต่อชีวิต) (Focus on perception)
                      3. คุณรู้สึกต่อปัญหานี้อย่างไร? (เช่น เศร้า 9/10, โกรธ 2/10) (Focus on emotional response)
                      4. วิธีการที่คุณใช้ในการจัดการกับปัญหาที่ผ่านมาเป็นอย่างไร? (Focus on coping)

                    - For 'Medical High Level', ask the following questions in order:
                      1. อาการที่คุณรู้สึกมีอะไรบ้าง? (Focus on symptoms)
                      2. ระยะเวลาที่คุณเผชิญกับอาการเหล่านี้มานานแค่ไหนแล้ว? (Focus on duration)

                    - For 'Counseling Medium Level', ask the following question:
                      1. คุณรู้สึกถึงอาการในร่างกายอย่างไร? เช่น ใจสั่น แน่นหน้าอก ตัวชา (Focus on body sensation)

                    - For 'Medical Medium Level', ask the following question:
                      1. คุณเคยมีประวัติความผิดปกติทางจิตหรือไม่? (Focus on psychiatric disorder history)

                2. Ensure that the selected question has not been asked before in the same state.
                3. Track and return the current question number for both high-level and medium-level exploration.
                4. Avoid repeating any question that the user has already answered.

                The next response must follow these rules:
                1. ตอบเป็นภาษาไทย (Respond in Thai)
                2. คุณเป็นผู้หญิง ใช้ คะ/ค่ะ ให้ถูกต้อง (You are female, use the polite particles "คะ" or "ค่ะ" correctly)
                3. ไม่ถามมากกว่า 1 คำถาม (Do not ask more than 1 question)
                4. ไม่เกิน 25 คำ (Do not exceed 25 words)

                Return the selected question in the following format as a JSON object only:
                {
                    "Explore Question": "[Selected question]"
                }.
                Must not include ```json  ``` 

            """,
            llm_config=llm_config,
        )

    @staticmethod
    def create_explore_session_control(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Explore_Session_Control",
            system_message=""" 
                Track the flow of the session by monitoring the questions answered and the number of questions asked in both 'High Level' and 'Medium Level' states.

                 - For 'Counseling High Level', questions focus on duration, perception, and emotional response.
                 - For 'Counseling Medium Level', questions focus on internal reflections, coping strategies, and body sensations.
                
                 - For 'Medical High Level', questions focus on symptoms, duration of symptoms, and behavior response.
                 - For 'Medical Medium Level', questions focus on psychiatric disorder history and body sensations.

                You must:
                1. Track how many questions have been answered in both the high-level and medium-level states.
                2. Review the user's responses and the 'Session Status' from both the high-level and medium-level exploration agents.
                3. Determine if the high-level exploration is 'Completed' (all high-level questions answered).
                4. If the high-level exploration is 'Completed', the medium-level exploration must start.
                5. Track and return the current question number for both high-level and medium-level explorations.
                6. If all questions from the medium-level exploration are answered, mark the session as 'Counseling is Completed'.

                Return the current state of the session as a JSON object only: 
                {
                    "Current State": "Counseling_Isn't_Satisfied_State (High Level)" or 
                                     "Counseling_Isn't_Satisfied_State (Medium Level)" or 
                                     "Counseling is Completed" or
                                     "Medical_Isn't_Satisfied_State (High Level)" or 
                                     "Medical_Isn't_Satisfied_State (Medium Level)" or 
                                     "Medical is Completed"
                }.
                Must not include ```json  ``` 

            """,
            llm_config=llm_config,
        )

    # Agent END
    @staticmethod
    def create_end_session_state_tracker(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="End_Session_State_Tracker",
            system_message="""
            Consider the above dialogue between an emotional support seeker and a supporter. 
            1. Summarize the seeker's experience that led to their main problem, providing a clear picture for the seeker to understand.
            2. Determine whether the conversation has ended based on the phrase "วันนี้รู้สึกดีขึ้นมากเลย" or "ขอบคุณ"
                If the conversation has ended, respond with 'conversation has ended'. otherwise, respond with 'conversation hasn't ended'.

            Return the summarized into as JSON object only: {"Main problem summary": ""}.
            Return the conversation result into as JSON object only: {"Conversation result": ""}.

            Must not include ```json  ``` 

        """,
            llm_config=llm_config,
        )

    @staticmethod
    def create_end_session_aspect_promoter(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="End_Session_Aspect_Promoter",
            system_message="""
            Consider the Conversation result.
            If the conversation result is 'conversation has ended,' respond with 'start summary sheet agent'. otherwise, respond with 'ตอนนี้เป็นไงบ้าง มีอะไรอยากพูดอีกไหม'.            
            
            Return the result into as JSON object only: {"End session result": ""}.

            Must not include ```json  ``` 

        """,
            llm_config=llm_config,
        )

    @staticmethod
    def create_summary_sheet(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Summary_Sheet",
            system_message="""
            Consider the above dialogue between an emotional support seeker and a supporter. 
            
            Return ข้อมูลผู้รับบริการ into as JSON object only: {'ชื่อผู้รับบริการ': '','เพศ': '','อายุ': '','วันที่รับบริการ': ''}.
            Return ข้อมูลที่ได้จากการพูดคุยในครั้งนี้ into as JSON object only: {'ปัญหา/เรื่องที่นำมา': '','ระยะเวลาที่เรืื่องนี้เกิดขึ้น': '','ความรู้สึกที่มีต่อเรื่องนี้': '','พฤติกรรม/วิธีการับมือที่มีต่อเรื่องนี้': '','อาการทางกายต่อเรื่องนี้': '','อาการอื่นๆ': '','โรคประจำตัว': '','ประวัติการรักษาทางจิตเวชก่อนหน้า': ''}.

            Must not include ```json  ``` 

        """,
            llm_config=llm_config,
        )

    # Agent NEW

    # Agent session flow

    @staticmethod
    def create_session_flow_state_tracker(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Session_Flow_State_Tracker",
            system_message="""
                Consider the [Dialogue History] between an emotional support seeker and a supporter.
                Determine which stage a supporter is at based on the lastest [Dialogue History], by following a structured approach: 
                [Identify main problem session, 
                Explore the seeker's main problem session, 
                End session

                Return into as JSON object only: {"Current Stage": ""}.
                Must not include ```json  ``` 

            """,
            llm_config=llm_config,
        )

    # Agent Global Coordination
    @staticmethod
    def create_global_coordination_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Global_Coordination_Agent",
            system_message="""
                Consider the [Dialogue History] between an emotional support seeker and a supporter. 
                The [Topic Candidates] are the potential topics that a supporter might mention in their next response. 
                [The Current Stage a supporter should focus on] is the stage they should address in their next response.
                Sort the [Topic Candidates] to determine which one is best for a supporter to use in their next response. 
                
                Return the sorted Topic Candidates as a JSON object only: {"Top Topic Candidates": ""}. 
                Must not include ```json  ``` 

            """,
            llm_config=llm_config,
        )

    # Agent Utterance

    @staticmethod
    def create_utterance_generation_agent(llm_config) -> AssistantAgent:
        return AssistantAgent(
            name="Utterance_Generation_Agent",
            system_message="""
                The above [Dialogue History] is a conversation between an emotional support seeker and a supporter.
                The [Top Topic Candidates] are the possible content that you might be able to mention in the next response. 
                [The Current Stage a supporter should focus on] is the stage they should address in their next response.
                Based on the [Dialogue History], draft the next response.
                You can refer to the content in the [Top Topic Candidates] to enrich the next response, 
                but do not have to include them if they are not suitable according to the [Dialogue History].
                The next response must not be similar in context to those already mentioned in the [Dialogue History].

                The next response must:
                1. ตอบเป็นภาษาไทย 
                2. คุณเป็นผู้หญิง ใช้ คะ/ค่ะ ให้ถูกต้อง 
                3. ไม่เกิน 25 คำ
                4. ถามทีละคำถาม
            """,
            llm_config=llm_config,
        )
