
# Getting Started with TheProdBot TAM/SAM/SOM Evals Notebook

This guide provides step-by-step instructions for Product Managers on how to set up and run TheProdBot TAM/SAM/SOM Evals notebook in Google Colab. This notebook helps you understand how different AI models estimate market size (TAM, SAM, SOM) for new product ideas and provides a framework for evaluating their performance.

Follow these steps sequentially to get started:

## Step 1: Clone the GitHub Repository to Google Drive

First, you need to get a copy of the notebook files and associated scripts onto your Google Drive, which Google Colab can access.

1.  Open the notebook in Google Colab.
2.  Open the Terminal in Colab. You can do this by going to the menu at the top: `Tools` -> `Terminal` -> `New terminal`.
3.  In the terminal window that appears at the bottom, navigate to your Google Drive directory. This is usually located at `/content/drive/MyDrive/`. You can use the `cd` command:
    ```bash
    cd "/content/drive/MyDrive/Colab Notebooks"
    ```
    *(Note: If the "Colab Notebooks" folder doesn't exist, you might need to create it first using `mkdir "Colab Notebooks"`)*
4.  Now, clone the GitHub repository containing the notebook files. Replace `[REPOSITORY_URL]` with the actual URL of the GitHub repository.
    ```bash
    git clone [REPOSITORY_URL] TAM-SAM-SOM.Notebook
    ```
    *(Note: You'll need to find the correct GitHub repository URL for TheProdBot Evals. This command will create a new folder named `TAM-SAM-SOM.Notebook` in your Google Drive.)*

## Step 2: Open the Notebook in Google Colab

Now that the files are on your Google Drive, you can open the main notebook file in Colab.

1.  In the Colab file browser (the folder icon on the left sidebar), navigate to the folder you just cloned: `drive` -> `MyDrive` -> `Colab Notebooks` -> `TAM-SAM-SOM.Notebook`.
2.  Click on the notebook file. It should be named something like `TheProdBot_Evals_Demo.ipynb`. This will open the notebook in your Colab environment.

## Step 3: Run the Notebook Cells Sequentially

Go through the notebook and run each code cell one by one. You can run a cell by clicking the "play" button to the left of the cell or by selecting the cell and pressing `Shift + Enter`.

Here's a breakdown of each important cell and what it does:

### Cell 1: Environment Setup & Drive Mount

*   **Purpose:** This cell sets up the necessary environment. It installs the required software libraries (like `openai` and `pyyaml`) and connects the notebook to your Google Drive so it can read and write files. It also navigates to the project directory on your Drive.
*   **What to expect:** You will see output indicating that packages are being installed and that your Google Drive is mounted. It will then list some files in the project directory to confirm you are in the right place.

### Cell 2: Notebook Health Check

*   **Purpose:** This cell runs a quick check to make sure everything is set up correctly before you start running the AI models. It verifies that Google Drive is connected, essential files are present, and your configuration is valid.
*   **What to expect:** You should see a series of "✅" symbols indicating successful checks. If you see any "❌" or "⚠️", stop and address the issue before continuing. The output will also suggest the next steps you can take.

### Cell 3: Securely Capture or Confirm Your OpenAI API Key

*   **Purpose:** The AI models used in this notebook require an API key from OpenAI (or a similar provider) to function. This cell makes sure your key is available to the notebook securely. It will prompt you to enter your key if it's not already set up in your Colab environment. **Your key is never displayed or stored in the notebook file itself.**
*   **What to expect:** If your key is already set, it will confirm this. If not, a box will appear asking you to paste your API key. Paste it carefully (it will be hidden) and press Enter.

    **⚠️ API Cost Warning:** Running models using this notebook will incur charges based on your usage with the API provider (e.g., OpenAI). Be mindful of your API key and usage.

### Cell 4: Interactive Model Selector & Runner

*   **Purpose:** This cell provides a way to run the market sizing flow with a single selected AI model. You can choose a model from a dropdown menu and then click a button to start the process.
*   **What to expect:** You will see a dropdown list of available models and a "Run TAM→SAM→SOM Flow" button. Selecting a model and clicking the button will start the AI generating market size estimates based on the prompts. The output will show the progress and confirm completion.

    **⚠️ API Cost Warning:** Running the flow in this cell will call the AI API and incur charges.

### Cell 5: Load and Launch the Prompt Runner

*   **Purpose:** This cell is similar to the previous one but focuses on ensuring the custom Python scripts used for running the prompts are correctly loaded and available. It then launches the same interactive model selector interface.
*   **What to expect:** You will see output confirming the API key is loaded and then the same interactive model selector (dropdown and button) as in the previous cell.

    **⚠️ API Cost Warning:** Running the flow via this interface will call the AI API and incur charges.

### Cell 6: Run Prompts + Model Bakeoff (Live Streaming Logs)

*   **Purpose:** This is a crucial step where you run the full set of prompts against one or multiple AI models (a "bakeoff"). This generates the raw output that you will later analyze and evaluate. It also streams the process logs live so you can see what's happening.
*   **What to expect:** The cell will confirm the API key is available and then start running the scripts. You will see detailed output showing which model is being run and the progress for each prompt (T5_tam, T6_sam, T7_som, etc.). This process can take some time depending on the number of models. Finally, it will show a summary of how each model performed based on the auto-scoring and where the logs are saved.

    **⚠️ API Cost Warning:** This cell will make multiple calls to the AI API for each model and will incur charges.

### Cell 7: Quick Model Scoreboard Summary

*   **Purpose:** This cell provides a quick summary of how many of the core market sizing prompts (TAM, SAM, SOM - T5-T7) were successfully completed by each model during the previous run.
*   **What to expect:** You will see a small table showing each model that was run and the number of completed trace files found for it. This is a good way to quickly verify that the previous step ran successfully for all models.

### Cell 8: Build → Trace → Export Pipeline

*   **Purpose:** This cell processes the raw output generated by the AI models into structured data that is easier to analyze and evaluate. It runs scripts to build a synthetic evaluation dataset (auto-scoring), extract detailed records for each conversation turn (traces), and export a human-readable version of these traces into a CSV file.
*   **What to expect:** You will see output indicating that each step (building evals, generating traces, exporting CSV) is running. It will confirm that the process is complete and list the names of the generated files (like `synthetic_evals.csv` and `traces_export.csv`) and where to find them in the `/outputs` folder.

### Cell 9: Mount Google Drive & Verify Output Artifacts

*   **Purpose:** This cell ensures your Google Drive is still connected and then changes the current working directory to the `/outputs` folder. This makes it easy to see and access all the files generated in the previous steps.
*   **What to expect:** It will confirm that Google Drive is mounted and show the current directory as `/content/drive/MyDrive/Colab Notebooks/TAM-SAM-SOM.Notebook/outputs`. It will then list the files in this directory. You should see folders for each model, the CSV and JSONL files from the previous step, and log files.

### Cell 10: Launch Interactive Human-in-the-Loop Evals Labeler

*   **Purpose:** This is where you, the Product Manager, provide valuable human feedback on the AI's performance. This cell loads the structured trace data and launches an interactive tool within the notebook that allows you to review each AI response turn-by-turn, assess its quality, and provide specific feedback (e.g., is the reasoning clear? Is the math correct?). Your feedback is saved automatically.
*   **What to expect:** The output will confirm that the trace data is loaded and then display an interactive user interface. This interface will show the prompt given to the AI, the AI's response (with reasoning and any structured data), and options for you to label the response's quality and provide comments. Use the navigation buttons to move through the different responses.

## Analyzing Results and Providing Feedback

After running the cells, you can:

*   **Review Logs:** Examine the `.log` files in the `/outputs` folder to see the detailed process logs for each step.
*   **Inspect Data:** Open the `synthetic_evals.csv` and `traces_export.csv` files in the `/outputs` folder to view the structured evaluation data and trace records.
*   **Use the Labeler:** Spend time in the interactive labeler (Cell 10 output) to provide detailed, human feedback on the AI's responses. This feedback is crucial for improving the AI's performance in future iterations. Your labels are saved to `outputs/human_labels.jsonl`.

By following these steps, you will successfully run the TAM/SAM/SOM evaluation process and generate valuable data and feedback for improving TheProdBot.
