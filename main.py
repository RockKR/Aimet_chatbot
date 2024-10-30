from autogen import AssistantAgent, UserProxyAgent
import os
from dotenv import load_dotenv
from customagents import CustomAgents  # Ensure this path is correct
import json
import ast


# Load environment variables from .env file
load_dotenv('.env')

# Define configuration for LLM (Large Language Model)
config_list = [
    {
        "model": os.environ['AZURE_OPENAI_MODEL'],
        "api_type": "azure",
        "api_key": os.environ['AZURE_OPENAI_API_KEY'],
        "base_url": os.environ['AZURE_OPENAI_ENDPOINT'],
        "api_version": "2024-02-01",
    }
]

# LLM configuration
llm_config = {
    "config_list": config_list,
    "temperature": 0,
    "cache_seed": None,  # Disables caching
}

# Initialize a User Proxy Agent
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="Terminator admin.",
    code_execution_config=False,
    human_input_mode="NEVER",
    llm_config=llm_config,
)

# List to hold all agents
all_agents = []


def add_agent(agent_creation_function, llm_config, response_format=None):
    """Creates an agent using the given creation function and adds it to the list of all agents."""
    agent = agent_creation_function(llm_config)
    all_agents.append(agent)
    return agent


# Initialize agents using CustomAgents
session_flow_state_tracker = add_agent(CustomAgents.create_session_flow_state_tracker, llm_config)

comforting_state_tracker = add_agent(CustomAgents.create_comforting_state_tracker, llm_config)
comforting_aspect_promoter = add_agent(CustomAgents.create_comforting_aspect_promoter, llm_config)

main_problem_state_tracker = add_agent(CustomAgents.create_main_problem_state_tracker, llm_config)
main_problem_aspect_promoter = add_agent(CustomAgents.create_main_problem_aspect_promoter, llm_config)

start_state_agent = add_agent(CustomAgents.create_start_state_agent, llm_config)
counseling_exploration_agent = add_agent(CustomAgents.create_counseling_exploration_agent, llm_config)
counseling_medium_exploration_agent = add_agent(CustomAgents.create_counseling_medium_exploration_agent, llm_config)
medical_exploration_agent = add_agent(CustomAgents.create_medical_exploration_agent, llm_config)
medical_medium_exploration_agent = add_agent(CustomAgents.create_medical_medium_exploration_agent, llm_config)
explore_session_control = add_agent(CustomAgents.create_explore_session_control, llm_config)
question_selector_agent = add_agent(CustomAgents.create_question_selector_agent, llm_config)

end_session_state_tracker = add_agent(CustomAgents.create_end_session_state_tracker, llm_config)
end_session_aspect_promoter = add_agent(CustomAgents.create_end_session_aspect_promoter, llm_config)
summary_sheet = add_agent(CustomAgents.create_summary_sheet, llm_config)


global_coordination = add_agent(CustomAgents.create_global_coordination_agent, llm_config)
utterance_generation = add_agent(CustomAgents.create_utterance_generation_agent, llm_config)

# Example dialogue history initialization
# dialogue_history = [
#     {"role": "system", "content": "สวัสดีค่ะ มีอะไรอยากให้ช่วยเหลือ สามารถเล่าให้ฟังได้เลยนะคะ"},
#     {"role": "system", "content": "ก่อนที่จะเริ่มบทสนทนา ฉันขอทราบชื่อและอายุ"}
# ]
dialogue_history = []


def print_and_parse_agent_result(agent_name, result):
    print(f"{agent_name} Result:")
    print(result.summary)
    print('-' * 15)

    try:
        # Parse the result as JSON
        parsed_result = json.loads(result.summary)
        print(f"{agent_name} Parsed JSON:")
        print(json.dumps(parsed_result, indent=4))
        return parsed_result
    except json.JSONDecodeError:
        print(f"Error: Could not parse {agent_name}'s result as JSON.")
        return None


# Main interaction loop
while True:
    try:
        user_message = input("User: ")
        print("-" * 15)
        dialogue_history.append({"role": "user", "content": user_message})

        # Execute each agent in sequence as per their specific roles

        #####################################
        session_flow_state_tracker_summary = user_proxy.initiate_chat(
            recipient=session_flow_state_tracker,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[f"[Dialogue History] {str(dialogue_history)}"]
        )

        session_flow_json = print_and_parse_agent_result("Session flow", session_flow_state_tracker_summary)

        #####################################
        comforting_state_summary_result = user_proxy.initiate_chat(
            recipient=comforting_state_tracker,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[f"[Dialogue History] {str(dialogue_history)}"]
            # response_format={"type": "json_object"}  # Add response_format here
        )

        comforting_aspect_promoter_result = user_proxy.initiate_chat(
            recipient=comforting_aspect_promoter,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[
                f"[Dialogue History] {str(dialogue_history)}",
                f"[Comforting Summary] {str(comforting_state_summary_result.summary)}",
            ]
            # response_format={"type": "json_object"}  # Add response_format here
        )

        #####################################
        if session_flow_json and session_flow_json.get('Current Stage') == 'Identify main problem session':
            print("main problem session, Start Rapport Agent..")

            main_problem_result_state_summary = user_proxy.initiate_chat(
                recipient=main_problem_state_tracker,
                message="",
                max_turns=1,
                summary_method="last_msg",
                carryover=[f"[Dialogue History] {str(dialogue_history)}"],
                response_format={"type": "json_object"}  # Add response_format here
            )

            main_problem_json = print_and_parse_agent_result("Main Problem Results", main_problem_result_state_summary)

            # Step 2: Extract 'main_problem_detected' and summary from the response
            main_problem_detected = main_problem_json.get("main_problem_detected", False)
            print(f"Main Problem Detected: {main_problem_detected}")

            main_problem_result_aspect_promoter = user_proxy.initiate_chat(
                recipient=main_problem_aspect_promoter,
                message="",
                max_turns=1,
                summary_method="last_msg",
                carryover=[f"[Main problem] {str(main_problem_result_state_summary.summary)}"],
                response_format={"type": "json_object"}  # Add response_format here
            )

        #####################################
        # Start State: Identify if it's a counseling topic
        if session_flow_json and (session_flow_json.get('Current Stage') == "Explore the seeker's main problem session" or main_problem_detected):
            print("explore session, Start Explore Agent..")

            start_state_result = user_proxy.initiate_chat(
                recipient=start_state_agent,
                message=user_message,
                max_turns=1,
                summary_method="last_msg",
                carryover=[f"[Dialogue History] {str(dialogue_history)}"],
                response_format={"type": "json_object"}  # Add response_format here
            )

            # Parse the start state result JSON
            start_state_json = print_and_parse_agent_result("Start State", start_state_result)

            if start_state_json and start_state_json.get('Identified Topic') == 'counseling':
                print("Identified Topic is counseling, moving to exploration...")

                # High-level counseling exploration
                exploration_result = user_proxy.initiate_chat(
                    recipient=counseling_exploration_agent,
                    message="",
                    max_turns=1,
                    summary_method="last_msg",
                    carryover=[f"[Dialogue History] {str(dialogue_history)}"],
                    response_format={"type": "json_object"}  # Add response_format here

                )
                counseling_exploration_json = print_and_parse_agent_result("Counseling Exploration (High Level)", exploration_result)

                # Check high-level session status
                high_level_status = counseling_exploration_json.get('Session Status')

                if high_level_status == 'Completed':
                    print("High-level exploration completed, moving to medium-level exploration...")

                    # Medium-level counseling exploration
                    medium_exploration_result = user_proxy.initiate_chat(
                        recipient=counseling_medium_exploration_agent,
                        message="",
                        max_turns=1,
                        summary_method="last_msg",
                        carryover=[f"[Dialogue History] {str(dialogue_history)}"],
                        response_format={"type": "json_object"}  # Add response_format here
                    )
                    counseling_medium_exploration_json = print_and_parse_agent_result(
                        "Counseling Exploration (Medium Level)", medium_exploration_result)
                else:
                    print(f"High-level exploration is {high_level_status}. Medium-level will not start until it is 'Completed'.")

            elif start_state_json and start_state_json.get('Identified Topic') == 'medical':
                print("Identified Topic is medical, moving to exploration...")

                # High-level counseling exploration
                exploration_result = user_proxy.initiate_chat(
                    recipient=medical_exploration_agent,
                    message="",
                    max_turns=1,
                    summary_method="last_msg",
                    carryover=[f"[Dialogue History] {str(dialogue_history)}"],
                    response_format={"type": "json_object"}  # Add response_format here
                )
                medical_exploration_json = print_and_parse_agent_result("Medical Exploration (High Level)", exploration_result)

                # Check high-level session status
                high_level_status = medical_exploration_json.get('Session Status')

                if high_level_status == 'Completed':
                    print("High-level exploration completed, moving to medium-level exploration...")

                    # Medium-level counseling exploration
                    medium_exploration_result = user_proxy.initiate_chat(
                        recipient=medical_medium_exploration_agent,
                        message="",
                        max_turns=1,
                        summary_method="last_msg",
                        carryover=[f"[Dialogue History] {str(dialogue_history)}"],
                        response_format={"type": "json_object"}  # Add response_format here
                    )
                    medical_medium_exploration_json = print_and_parse_agent_result("Medical Exploration (Medium Level)", medium_exploration_result)
                else:
                    print(f"High-level exploration is {high_level_status}. Medium-level will not start until it is 'Completed'.")

            # Track the session state
            explore_session_control_result = user_proxy.initiate_chat(
                recipient=explore_session_control,
                message="",
                max_turns=1,
                summary_method="last_msg",
                carryover=[f"[Dialogue History] {str(dialogue_history)}"],
                response_format={"type": "json_object"}  # Add response_format here
            )
            explore_session_control_json = print_and_parse_agent_result("Session Flow", explore_session_control_result)

            # Select the next question based on the current session flow state
            question_selector_result = user_proxy.initiate_chat(
                recipient=question_selector_agent,
                message="",
                max_turns=1,
                summary_method="last_msg",
                carryover=[
                    f"[Dialogue History] {str(dialogue_history)}",
                    f"[Session Flow] {str(explore_session_control_result.summary)}"
                ],
                response_format={"type": "json_object"}  # Add response_format here

            )

        #####################################
        if session_flow_json and session_flow_json.get('Current Stage') == "End session":
            print("end session, Start End Agent..")
            end_session_result_state_summary = user_proxy.initiate_chat(
                recipient=end_session_state_tracker,
                message="",
                max_turns=1,
                summary_method="last_msg",
                carryover=[f"[Dialogue History] {str(dialogue_history)}",
                           f"[Main problem] {str(main_problem_result_state_summary.summary)}"
                           ],
                response_format={"type": "json_object"}  # Add response_format here
            )

            end_session_result_aspect_promoter = user_proxy.initiate_chat(
                recipient=end_session_aspect_promoter,
                message="",
                max_turns=1,
                summary_method="last_msg",
                carryover=[f"[Conversation result] {str(end_session_result_state_summary.summary)}"
                           ],
                response_format={"type": "json_object"}  # Add response_format here
            )

            end_session_json = print_and_parse_agent_result("End session", end_session_result_aspect_promoter)
            if end_session_json and end_session_json.get('End session result') == 'start summary sheet agent':
                print("moving to summary sheet")
                summary_sheet_result = user_proxy.initiate_chat(
                    recipient=summary_sheet,
                    message="",
                    max_turns=1,
                    summary_method="last_msg",
                    carryover=[f"[Dialogue History] {str(dialogue_history)}"
                               ],
                )
            else:
                print(f"session has not ended, not start summary sheet")

        ##########################################
        # Initialize topic candidates as an empty list
        topic_candidates = [comforting_aspect_promoter_result.summary]

        # Function to safely add summaries if they are defined and not empty
        def add_summary_if_defined(summary):
            if summary:
                topic_candidates.append(summary)

        # Attempt to add each summary
        try:
            add_summary_if_defined(main_problem_result_aspect_promoter.summary)
        except NameError:
            pass  # Variable is not defined; ignore

        try:
            add_summary_if_defined(end_session_result_aspect_promoter.summary)
        except NameError:
            pass  # Variable is not defined; ignore

        try:
            add_summary_if_defined(question_selector_result.summary)
        except NameError:
            pass  # Variable is not defined; ignore

        global_coordination_result = user_proxy.initiate_chat(
            recipient=global_coordination,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[
                f"[Dialogue History] {str(dialogue_history)}",

                f"[Topic Candidates] {str(topic_candidates)}",

                f"[The Current Stage a supporter should focus on] {str(session_flow_state_tracker_summary.summary)}",
            ],
            response_format={"type": "json_object"}  # Add response_format here

        )

        utterance_generation_result = user_proxy.initiate_chat(
            recipient=utterance_generation,
            message="",
            max_turns=1,
            summary_method="last_msg",
            carryover=[
                f"[Dialogue History] {str(dialogue_history)}",

                f"[Top Topic Candidates] {str(global_coordination_result.summary)}",

                f"[The Current Stage a supporter should focus on] {str(session_flow_state_tracker_summary.summary)}",
            ],
            response_format={"type": "json_object"}  # Add response_format here
        )

        # Output the bot's response
        bot_answer = utterance_generation_result.summary
        print(bot_answer)
        print('-' * 15)

        dialogue_history.append({"role": "system", "content": bot_answer})

        # Calculate and display total cost

    except KeyboardInterrupt:
        print("\nExiting the dialogue loop.")
        break
    except Exception as e:
        print(f"Error: {e}")
