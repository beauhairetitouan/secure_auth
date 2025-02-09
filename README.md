# 🛡️ Application Web d'Authentification Flask

Une application web Flask permettant aux utilisateurs de s'inscrire et de se connecter de manière sécurisée.

---

## 🚀 Fonctionnalités

- ✅ Système d'authentification complet (inscription, connexion, déconnexion)
- 🔑 Authentification sécurisée avec **Flask-Login**
- 🔒 Protection contre les attaques web courantes :
- Protection XSS (Cross-Site Scripting)
- Protection CSRF (Cross-Site Request Forgery)
- Protection contre les injections SQL
- Protection contre les attaques par force brute
- 📂 Base de données sécurisée avec **SQLAlchemy**
- 🔄 Gestion avancée des sessions utilisateur
- 📊 Système de logging complet des tentatives de connexion
- 🤖 Protection anti-bot avec **Google reCAPTCHA**
- 🔐 Support HTTPS natif avec Gunicorn
- ⚡ Limitation de taux avec **Redis** et **Flask-Limiter**

---


### Logiciels requis

- Python 3.8 ou supérieur
- Redis (pour la limitation de taux)
- OpenSSL (pour la génération des certificats)

### Vérification des installations

```bash
# Vérifier Python
python --version

# Vérifier pip
pip --version

# Vérifier Redis
redis-cli ping  # Devrait répondre "PONG"

---

## 🛠 Installation du projet

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/beauhairetitouan/secure_auth.git
cd secure_auth
```

#### Installation des prérequis manquants

##### Python et pip
- **Windows** : Téléchargez depuis [python.org](https://www.python.org/downloads/)
- **macOS** : `brew install python3`
- **Linux** : `sudo apt install python3 python3-pip`

##### Redis
- **Windows** : Utilisez [WSL2](https://redis.io/docs/getting-started/installation/install-redis-on-windows/) ou [Memurai](https://www.memurai.com/)
- **macOS** : `brew install redis && brew services start redis`
- **Linux** : `sudo apt install redis-server && sudo systemctl start redis-server`

##### OpenSSL
- **Windows** : Installez [OpenSSL pour Windows](https://slproweb.com/products/Win32OpenSSL.html)
- **macOS** : `brew install openssl`
- **Linux** : `sudo apt install openssl`

## 🛠 Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/beauhairetitouan/secure_auth.git
cd secure_auth
```

2. **Créer et activer l'environnement virtuel**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration**
```bash
# Copier le fichier de configuration exemple
cp .env.example .env

# Éditer le fichier .env avec vos paramètres
```

---


## 🚦 Démarrage

### Génération du certificat SSL
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

### Lancement avec Gunicorn (HTTPS)
```bash
gunicorn --certfile=server.crt --keyfile=server.key --bind 0.0.0.0:5001 app:app
```

L'application sera accessible à l'adresse : `https://localhost:5001`


---

## 🔒 Sécurité intégrée

### Authentification
- Hachage des mots de passe avec bcrypt
- Gestion sécurisée des sessions avec Flask-Login
- Protection contre la force brute avec Redis et Flask-Limiter

### Protection contre les attaques
- En-têtes de sécurité avec Flask-Talisman
- Tokens CSRF avec Flask-WTF
- Validation stricte des entrées
- Protection XSS via l'échappement automatique
- Limitation des tentatives de connexion

### Gestion des sessions
- Sessions chiffrées côté serveur
- Rotation automatique des sessions
- Invalidation sécurisée à la déconnexion

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
