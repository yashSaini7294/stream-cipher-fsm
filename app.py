from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import subprocess
import random
import time
import secrets  


app = Flask(__name__)
app.secret_key = 'streamciphersecret'

UPLOAD_FOLDER = 'upload'
OUTPUT_FOLDER = 'download'
CIPHER_BINARY = './cipher'  # Use 'cipher.exe' on Windows

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        seed_input = request.form.get('seed')

        if uploaded_file.filename == '':
            flash('No file selected.')
            return redirect(request.url)

        # Save uploaded file
        timestamp = str(int(time.time()))
        input_path = os.path.join(UPLOAD_FOLDER, f"input_{timestamp}")
        uploaded_file.save(input_path)

        # Handle seed input
        if seed_input.strip() == '':
            seed_used = secrets.randbelow(256)
            flash(f"No seed provided. Random seed generated: {seed_used}")
        else:
            try:
                seed_used = int(seed_input)
                if not (0 <= seed_used <= 255):
                    raise ValueError
                flash(f"Seed used: {seed_used}")
            except ValueError:
                flash("Invalid seed. Must be an integer between 0 and 255.")
                return redirect(request.url)

        # Define output path
        output_filename = f"output_{timestamp}.enc"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Run cipher binary
        try:
            subprocess.run([CIPHER_BINARY, input_path, output_path, str(seed_used)], check=True)
        except subprocess.CalledProcessError:
            flash("Encryption failed.")
            return redirect(request.url)

        # Redirect to GET route with download filename
        return redirect(url_for('index', filename=output_filename))

    # Handle GET requests (normal or after redirect)
    download_file = request.args.get('filename')
    return render_template('index.html', download_file=download_file)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
