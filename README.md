# 🛡️ Application Web d'Authentification Flask

Une application web Flask permettant aux utilisateurs de s'inscrire et de se connecter de manière sécurisée.

---

## 🚀 Fonctionnalités

- ✅ Inscription et connexion sécurisées
- 🔑 Authentification avec **Flask-Login**
- 🔒 Sécurisation contre **XSS, CSRF, injections SQL**
- 📂 Base de données **SQLAlchemy (SQLite/PostgreSQL)**
- 🔄 Gestion des sessions utilisateur
- 📊 Logging des connexions pour la sécurité
- 🤖 Captcha pour éviter les inscriptions et connexions en masse

---

## 📋 Prérequis

1. **Python 3.8 ou supérieur**  
   Vérifie l'installation :
   ```bash
   python --version
   ```
   - **Windows** : Télécharge [Python ici](https://www.python.org/downloads/)
   - **Mac/Linux** : Utilise `brew install python3` ou `sudo apt install python3`

2. **pip** (Gestionnaire de paquets Python)  
   Vérifie avec :
   ```bash
   pip --version
   ```

---

## 🛠 Installation du projet

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/beauhairetitouan/secure_auth.git
cd secure_auth
```

### 2️⃣ Créer et activer l'environnement virtuel

#### 🖥 **Windows (cmd/Powershell)**
```powershell
python -m venv venv
venv\Scripts\activate
```

#### 🍏 **Mac**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 🐧 **Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

> ⚠️ **Si `python3` n'est pas trouvé**, essaie `python` à la place.

---

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurer l'environnement
Copie le fichier `.env.example` en `.env` et modifie les valeurs :
```bash
cp .env.example .env
```
> **Modifie `.env` pour inclure tes configurations (clé secrète, base de données, etc.).**

---


## 🚦 Démarrer l'application


### 🔐 Mode HTTPS (avec certificat local et Gunicorn)
Si tu veux exécuter Flask en HTTPS avec Gunicorn, commence par créer ton certificat SSL (si ce n'est pas déjà fait) :

#### 🖥 Windows (Git Bash ou WSL)
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

#### 🍏 Mac / 🐧 Linux
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

Puis lance Gunicorn avec SSL :
```bash
gunicorn --certfile=server.crt --keyfile=server.key -b 0.0.0.0:5001 app:app
```
🚀 Gunicorn va lancer ton application avec HTTPS sur le port 5001.

> 📌 **Si `openssl` n'est pas installé** :
> - **Windows** : Installe [OpenSSL for Windows](https://slproweb.com/products/Win32OpenSSL.html)
> - **Mac** : `brew install openssl`
> - **Linux** : `sudo apt install openssl` (Debian/Ubuntu) ou `sudo dnf install openssl` (Fedora)

---

## 🔒 Sécurité intégrée

- **Hachage des mots de passe** avec **bcrypt**
- **Protection CSRF** avec **Flask-WTF**
- **Sécurisation des en-têtes** avec **Flask-Talisman**
- **Limitation des tentatives de connexion** avec **Flask-Limiter**
- **Gestion des sessions utilisateur** avec **Flask-Login**
- **Gestion des inscriptions et connexions de masse** avec **Google-Recaptcha** 

---

## 📚 API et Routes

| Route | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil |
| `/register` | GET/POST | Inscription utilisateur |
| `/login` | GET/POST | Connexion utilisateur |
| `/logout` | GET | Déconnexion utilisateur |
| `/dashboard` | GET | Profil utilisateur (protégé) |
| `/favicon.ico` | GET | Logo application |

---

## 📂 Structure du Projet

```
secure_auth/
├── __pycache__/
├── instance/
│   ├── database.db
├── static/
│   ├── dashboard.css
│   ├── login.css
│   ├── favicon.ico
│   ├── favicon.webp
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
├── venv/
├── .env
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── forms.py
├── models.py
├── README.md
├── requirements.txt
├── .env.example
├── server.key
└── server.crt
```

---

## 🤝 Contribution

1. **Fork** le projet
2. **Crée une branche** (`git checkout -b feature/amelioration`)
3. **Commit tes changements** (`git commit -m "Ajout de fonctionnalité"`)
4. **Push vers la branche** (`git push origin feature/amelioration`)
5. **Ouvre une Pull Request**

---

## 👤 Contact

Beauhaire Titouan  
📌 **Lien du projet** : [https://github.com/beauhairetitouan/secure_auth](https://github.com/beauhairetitouan/secure_auth)
