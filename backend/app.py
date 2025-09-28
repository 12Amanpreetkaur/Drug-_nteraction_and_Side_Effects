from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import os
import csv

BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'drugs.db')
INTERACTIONS_CSV = os.path.join(BASE, 'interactions.csv')   # <-- add this
UPLOAD_FOLDER = os.path.join(BASE, 'uploads')
ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super-secret-college-key'  # for admin session

# -------------------- Helper Functions -------------------- #
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def load_interactions():
    interactions = []
    seen = set()
    if not os.path.exists(INTERACTIONS_CSV):
        return interactions
    with open(INTERACTIONS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = row.get('drug_a','').strip().lower()
            b = row.get('drug_b','').strip().lower()
            key = tuple(sorted([a,b]))  # order-independent
            if key in seen:
                continue  # skip duplicates
            seen.add(key)
            interactions.append({
                'drug_a': row.get('drug_a','').strip(),
                'drug_b': row.get('drug_b','').strip(),
                'severity': row.get('severity','low').strip(),
                'description': row.get('description', row.get('note','')).strip()
            })
    return interactions
def save_interaction_row(row):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['drug_a','drug_b','severity','note'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# -------------------- Routes -------------------- #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check_interactions', methods=['POST'])
def check_interactions():
    data = request.get_json()
    meds = data.get('meds', [])
    found = []
    interactions = load_interactions()
    for i in range(len(meds)):
        for j in range(i+1, len(meds)):
            a = meds[i].strip()
            b = meds[j].strip()
            for inter in interactions:
                if (inter['drug_a'].lower()==a.lower() and inter['drug_b'].lower()==b.lower()) or \
                   (inter['drug_a'].lower()==b.lower() and inter['drug_b'].lower()==a.lower()):
                    found.append({
                        'drug_a':a,
                        'drug_b':b,
                        'severity': inter['severity'],
                        'description': inter['description']
                    })
    return jsonify({'interactions': found})

@app.route('/api/import_csv', methods=['POST'])
def import_csv():
    if 'admin' not in session:
        return jsonify({'error':'unauthorized'}), 403

    if 'file' not in request.files:
        return jsonify({'error':'no file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'no selected file'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        count = 0
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                a = row.get('drug_a','').strip()
                b = row.get('drug_b','').strip()
                severity = row.get('severity','low').strip()
                note = row.get('note','').strip()
                if not a or not b: 
                    continue
                save_interaction_row({'drug_a':a,'drug_b':b,'severity':severity,'note':note})
                count +=1
        return jsonify({'imported': count})
    return jsonify({'error':'invalid file'}), 400

# -------------------- Admin Login -------------------- #
ADMIN_PASSWORD = 'college123'  # change if you want

@app.route('/admin', methods=['GET','POST'])
def admin_panel():
    if request.method=='POST':
        password = request.form.get('password')
        if password==ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Wrong password')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_panel'))
    interactions = load_interactions()
    return render_template('admin_panel.html', interactions=interactions)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# -------------------- AI Placeholder -------------------- #
@app.route('/api/ai_query', methods=['POST'])
def ai_query():
    data = request.get_json()
    prompt = data.get('prompt','')
    return jsonify({'response': f'[AI placeholder] Prompt length {len(prompt)} received.'})

if __name__=='__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)
