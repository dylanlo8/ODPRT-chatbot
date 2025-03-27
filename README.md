# ODPRT Chatbot
A chatbot designed to answer questions relating to the ODPRT department.

- [Features](#features)
  - [Architecture Diagram](#architecture-diagram)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running Locally](#running-locally)
- [Usage](#usage)
  - [Backend API](#backend-api)
  - [Frontend Interface](#frontend-interface)

### Architecture Diagram
![Overall Architecture](./docs/images/architecture.png)

![Chat Workflow](./docs/images/chat_workflow.png)

![Email](placeholder.png)

## Getting Started

### Prerequisites

Scripting Languages:
- Python 3.11 or higher
- Node.js 14.x or higher

Tech Stack and Cloud Services
- Milvus Vector DB: Zillis Cloud Account (FREE!)
- Supabase account (FREE!)

### Installation

#### Clone this repository
```bash
git clone https://github.com/dylanlo8/ODPRT-chatbot.git
```

#### Chatbot: Backend - `Miniconda`

```bash
# make script executable
chmod +x bootstrap.sh

# run script
./env/bootstrap.sh

# !! ACTIVATE whenever coding
conda activate odprt
```

#### Chatbot: Frontend - `npm`

```bash
# navigate to frontend directory
cd chatbot/frontend

# install required libraries and packages
npm install

# run
npm run dev
```

#### Admin Dashboard: Frontend - `npm`

```bash
placeholder
```


### Configuration
1. Create a `.env` file in the root directory.

2. Add following variables to the `.env`
```shell
## for llms and vlms
OPENAI_API_KEY=
OPENAI_MODEL=
HYPERBOLIC_API_KEY=

## for databases
# Cloud Vector DB
ZILLIS_ENDPOINT=
ZILLIS_TOKEN=

# Bucket and Relational DB
SUPABASE_TOKEN=

```

#### Setting up LLM models

##### OpenAI
To get an OpenAI API key, you can follow the steps listed in this [article](https://medium.com/@lorenzozar/how-to-get-your-own-openai-api-key-f4d44e60c327). Thereafter, set `OPENAI_API_KEY` to the API key you just obtained and `OPENAI_MODEL` to the GPT model for your LLM (eg gpt-4o-mini).

### Running Locally

#### Windows

From the root directory, run the following command:
```shell
./start.ps1
```
This script starts up both the backend and the frontend components sequentially. Alternatively, to set them up separately, you can run the following commands:

To set up the backend, run
```shell
python chatbot/backend/main.py
```
To set up the frontend, navigate to chatbot/frontend by running
```shell
cd chatbot/frontend
```
Then, run the command
```shell
npm start
```

#### Mac/Linux

From the root directory, run the following command:
```shell
./start.sh
```
This script starts up both the backend and the frontend components sequentially. Alternatively, to set them up separately, you can run the following commands:

To set up the backend, run
```shell
python chatbot/backend/main.py
```
To set up the frontend, navigate to chatbot/frontend by running
```shell
cd chatbot/frontend
```
Then, run the command
```shell
npm start
```

## Usage

### Backend API

`/chat` - Handle user queries and generate chatbot responses. Expects a POST request with JSON payload containing query (user's input message) and messages (conversation history)

`/email` - Generate an email draft based on chat conversation history. Expects a POST request with JSON payload containing messages (conversation history)

### Frontend Interface

![Landing Page](./docs/images/chatbot_landing_page.png)
*Page where chatbot will be hosted*


![Interface](./docs/images/chatbot_interface.png)
*Interface of the chatbot*


![Q&A](./docs/images/chatbot_q&a.png)
*Question and answer*


![Email](./docs/images/chatbot_mailto_link.png)
*Mailto link appears when user wants to email IEP department*


![Feedback](./docs/images/chatbot_feedback.png)
*Feedback modal pops up after user is done interacting with the chatbot*
