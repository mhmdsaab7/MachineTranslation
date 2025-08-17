---
title: "Zaka Machine Translation"
emoji: "🌍"
colorFrom: "blue"
colorTo: "green"
sdk: "docker"
pinned: false

---

## 🛠️ Setup Instructions (Local with Docker)  

1. Clone the repository:  
   ```bash
   git clone https://github.com/mhmdsaab7/MachineTranslation.git
   cd MachineTranslation
2. Build the Docker image:
    ```bash
   docker build -t engfr-translator .
3. Run the container:
   ``` bash
   docker run -p 8080:8080 engfr-translator
4. Open in your browser:
    ```bash
   http://localhost:8080

---- 
## Using the Interface

Enter an English sentence in the text box.

Click Translate.

The French translation will appear instantly below.

---

## Known Issues / Limitations
* The model vocabulary is limited to training data → may fail on rare/long sentences.

* Padding tokens may occasionally appear if sentence lengths exceed max_en/max_fr.

* Works fine on CPU but is slower compared to GPU.

* Currently only supports English → French, not bidirectional translation.
* Model used is not perfect and can be optimized specially by adding attention mechanism

--
### App Screenshot

![Screenshot](images/readme_app_screenshot.png)