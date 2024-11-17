# Standardizer
Standardizer permet de créer facilement un premier jet d'un standard lean à l'aide de :
- Intention : Pourquoi ce standard est important et ce qu'il doit accomplir pour le client.
- Points de contrôle : Les éléments essentiels pour garantir la qualité du travail.
- Erreurs courantes : Les pièges à éviter et leurs conséquences.


# Developping
```bash
# First install
pyenv virtualenv 3.10.7 standardizer
pyenv local standardizer
poetry install

# Launch reload
gradio standardizer/main.py --demo-name=interface
```