from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import subprocess
import random
import time

app = Flask(__name__)

# Ensure upload/output folders exist
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        seed_input = request.form.get('seed')
        generate_seed = request.form.get('generate_seed') == 'true'

        if not uploaded_file:
            return "No file uploaded", 400

        # Use user-entered seed or generate a random one
        if generate_seed or not seed_input:
            seed = random.randint(1, 255)
        else:
            try:
                seed = int(seed_input)
                if seed < 0 or seed > 255:
                    raise ValueError
            except ValueError:
                return "Seed must be an integer between 0 and 255", 400

        # Save uploaded file
        input_filename = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(input_filename)

        # Generate output filename
        timestamp = int(time.time())
        output_filename = os.path.join(OUTPUT_FOLDER, f"processed_{timestamp}")

        # Run the compiled C++ binary
        try:
            subprocess.run(['./cipher', input_filename, output_filename, str(seed)], check=True)
        except subprocess.CalledProcessError:
            return "Encryption/Decryption failed", 500

        # Return processed file and show seed used
        return send_file(output_filename, as_attachment=True, download_name='processed_file'), 200

    return render_template('index.html')