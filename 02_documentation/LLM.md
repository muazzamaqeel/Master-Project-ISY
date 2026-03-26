# Ollama or vLLM

### What is Ollama?
Ollama is a local LLM runtime tool that lets you run large language models on your own machine easily.

1. Downloads and runs models (e.g., Llama, Mistral)
2. Provides a simple REST API (OpenAI-like)
3. Handles: model loading, memory management, inference

#### How to install (Powershell):
```powershell
 irm https://ollama.com/install.ps1 | iex
```
Open a new Terminal
```powershell
ollama run phi3
```
#### Results:
![Result](/images/01_image.png)


### What is vLLM?
vLLM is a high-performance inference engine for LLMs, designed for serving models efficiently at scale.

1. Runs LLMs with optimized GPU performance
2. Supports high-throughput serving
3. Implements advanced techniques like:
4. PagedAttention (efficient memory handling)
5. continuous batching

How to install:

1. Install WSL
    ```powershell
    wsl --install Ubuntu
    ```
2. Open WSL
    ```powershell
    wsl
    ```
3. Next Commands to run in WSL
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip python3-venv git -y
    python3 --version
    ```
    
    ```bash
    # Expected: /home/username
    cd ~
    pwd
    ```

    ```bash
    # Good Practice (Create an Env.)
    python3 -m venv vllm-env
    source vllm-env/bin/activate
    ```
    
    ```bash
    # Required Pacakges
    pip install --upgrade pip
    pip install vllm
    sudo apt install nvidia-cuda-toolkit -y
    ```
    ```bash
    (vllm-env) muazzam@DESKTOP-FBB9PSC:~$ nvcc --version
                        nvcc: NVIDIA (R) Cuda compiler driver
                        Copyright (c) 2005-2023 NVIDIA Corporation
                        Built on Fri_Jan__6_16:45:21_PST_2023
                        Cuda compilation tools, release 12.0, V12.0.140
                        Build cuda_12.0.r12.0/compiler.32267302_0
    ```
    
    ```bash
    python -m vllm.entrypoints.openai.api_server \
        --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
        --gpu-memory-utilization 0.75 \
        --max-model-len 256 \
        --enforce-eager
    ```
    ```bash
    # Local IP
        hostname -I
        # - muazzam@DESKTOP-FBB9PSC:/mnt/c/Users/Muazzam$ hostname -I
                                192.168.37.145
    # Open a new WSL Instance and use the same IP that you Found Above
        curl http://192.168.37.145:8000/v1/chat/completions   -H "Content-Type: application/json"   -d '{
            "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "messages": [
            {"role": "user", "content": "Hello, how are you?"}
            ]
        }'
    ```
#### Results:
![Result](/images/01_image.png)
