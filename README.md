# Project Setup
To run the API, these steps need to be followed:
1. Install the required libraries.
   ```sh
   pip install -r requirements.txt
   ```
2. Create a `.env` file in your project and add the following line `HUGGINGFACE_TOKEN=YOUR_HUGGINGFACE_TOKEN`. Replace `YOUR_HUGGINGFACE_TOKEN` with your personal Huggingface token.
   You can create a Huggingface token by logging into the Huggingface website, going to the settings page, and navigating to the access keys tab. There, you can create a token with
   "write" permissions.

When you run the API, the terminal will print a line that says `Running on http:/YOUR.IP:5000`. Use this address to send requests.
