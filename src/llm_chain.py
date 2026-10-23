import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
import logging

# 🔥 reduce transformer noise
logging.getLogger("transformers").setLevel(logging.ERROR)

def create_qa_chain(model_name: str = "Qwen/Qwen2.5-1.5B-Instruct", vector_store=None):

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # Use a smart causal LLM (Instruct model)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Load model dynamically based on architecture type
    is_causal = True
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True
        ).to(device)
    except (ValueError, KeyError, EnvironmentError):
        # Fallback to seq2seq if the model isn't causal or fails to load as causal
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True
        ).to(device)
        is_causal = False

    retriever = vector_store.get_retriever(k=4)

    def qa_chain(inputs):
        query = inputs["input"]

        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 🔥 FIX: prevent token overflow
        context = context[:3000]

        if not context.strip():
            return {"result": "No relevant information found."}

        messages = [
            {"role": "system", "content": "You are an expert HR recruiter and AI resume screener. Your goal is to provide clear, detailed, and professional responses in full sentences and paragraphs. When asked to summarize or evaluate a candidate, write a comprehensive paragraph that synthesizes their core skills, experience, and suitability. Do not just list keywords. Format clearly."},
            {"role": "user", "content": f"Based ONLY on the following context, please answer the question.\n\nContext:\n{context}\n\nQuestion:\n{query}"}
        ]
        
        if is_causal:
            try:
                # Apply chat template for modern instruct models
                text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            except Exception:
                text = f"{messages[0]['content']}\n\n{messages[1]['content']}\n\nAnswer:\n"
                
            input_ids = tokenizer([text], return_tensors="pt").input_ids.to(device)
            
            outputs = model.generate(
                input_ids,
                max_new_tokens=600,
                temperature=0.4,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id if tokenizer.eos_token_id is not None else tokenizer.eos_token_id
            )
            
            generated_ids = outputs[0][len(input_ids[0]):]
            generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
        else:
            # Fallback format for seq2seq models like T5
            text = f"{messages[0]['content']}\n\n{messages[1]['content']}\n\nAnswer:\n"
            input_ids = tokenizer([text], return_tensors="pt").input_ids.to(device)
            
            outputs = model.generate(
                input_ids,
                max_new_tokens=600,
                temperature=0.4,
                do_sample=True
            )
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {
            "result": generated_text.strip()
        }

    return qa_chain