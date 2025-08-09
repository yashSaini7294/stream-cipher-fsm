# Stream Cipher (FSM-Based) – Verilog → C++ → Flask Demo

- Started with a Verilog-based stream cipher, using:

	-> a basic Finite State Machine (FSM)

	-> and an LFSR (Linear Feedback Shift Register) for pseudo-randomness

- Converted the same logic into C++ to simulate the FSM behavior in software

- Built a simple Flask web interface to demonstrate encryption/decryption in an interactive way

The webpage is just for demonstration purposes!!


---

## What This Project Shows

- I built a basic FSM in **Verilog** that drives a stream cipher.
- Converted the FSM logic to **C++** using the same LFSR-based PRNG idea.
- Wrapped it all in a **Flask web app** so anyone can test encryption/decryption locally.
- It's just for demonstration — not a real-world encryption tool.

---

## 🧰 Tools and Tech Used

- `Verilog` – FSM and LFSR logic
- `C++` – Core cipher engine (same behavior as FSM)
- `Python + Flask` – Web interface for local testing
- `HTML/CSS` – Simple front-end

---

## Folder Structure

stream-cipher-fsm/
├── cipher.cpp # The original C++ logic (converted from FSM)
├── cipher.exe # Compiled version used by Flask
├── app.py # Flask app (runs the site)
├── templates/
│ └── index.html # Web page
├── static/
│ └── style.css # Styling
├── uploads/ # Input files go here
├── downloads/ # Encrypted/Decrypted output files
├── Use_This_Exp.txt # Sample file to test

---

### View the demo results in the [screenshots] folder.



