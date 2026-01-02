import asyncio
import sys
sys.path.insert(0, '.')

from app.services.llm.providers import get_llm_provider

async def test_llm():
    try:
        print("Testing LLM provider...")
        llm = get_llm_provider()
        print(f"LLM provider: {llm}")
        
        result = await llm.generate(
            prompt="请说'你好'", 
            system_prompt="你是一个助手"
        )
        print(f"Success! Result: {result[:100]}...")
        return True
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_llm())
    sys.exit(0 if success else 1)
