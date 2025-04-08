from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    Event,
    step,
)
import asyncio
import chatgpt
from chatgpt import Conversation
import youtube_api

class UserPromptEvent(Event):
    conversation: Conversation

class CategorizedEvent(Event):
    query: str

class SearchedEvent(Event):
    results: str

class RankedEvent(Event):
    video_id: str

class MyWorkflow(Workflow):
    youtube = None
    user_prompt = str

    @step
    async def get_user_promtp(self, ev: StartEvent) -> UserPromptEvent:
        user_prompt = input("Enter request: ")
        self.user_prompt = user_prompt
        conversation = Conversation(system_prompt=chatgpt.Conversation.system_prompt_get_keywords)
        conversation.add_message(user_prompt, "user")
        return UserPromptEvent(conversation=conversation)
    
    @step
    async def chatgpt_categorize(self, ev:UserPromptEvent) -> CategorizedEvent:
        response = chatgpt.get_chat_completion(ev.conversation.messages)
        print("\nassistant: ", response)
        ev.conversation.add_message(response, "assistant")
        return CategorizedEvent(query=response)
    
    @step
    async def search_youtube_with_keywords(self, ev:CategorizedEvent) -> SearchedEvent:
        results = youtube_api.search_youtube(self.youtube, ev.query)
        return SearchedEvent(results=results)
    
    @step
    async def chatgpt_rank(self, ev:SearchedEvent) -> RankedEvent:
        user_prompt = f"<user_prompt> {self.user_prompt} \n <youtube_results> {ev.results}"
        conversation = Conversation(system_prompt=chatgpt.Conversation.system_prompt_rank_videos)
        conversation.add_message(user_prompt, "user")
        response = chatgpt.get_chat_completion(conversation.messages)
        print("\nassistant: ", response)
        return RankedEvent(video_id=response)
    
    @step
    async def show_to_user(self, ev:RankedEvent) -> StopEvent:
        print(f"choosen video: https://www.youtube.com/watch?v={ev.video_id}")
        return StopEvent("Done")

async def main(youtube):
    w = MyWorkflow(timeout=10, verbose=False)
    w.youtube = youtube
    result = await w.run()
    print(result)


if __name__ == "__main__":
    # set up ChatGPT
    chatgpt.setup_chatgpt()
    youtube = youtube_api.setup_youtube_api()
    asyncio.run(main(youtube))