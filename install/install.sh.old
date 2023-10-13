
BASE_DIR=`pwd`
MODE=dev

#########################
# Install BACKEND
#########################
# Install python dependancies
cd "${BASE_DIR}"/backend
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


# Copy the custom components
if [[ ! -f "${BASE_DIR}"/backend/config/config.py]]; then
  echo "Création des fichiers de customisation du backend: Configuration..."
  cp -n  config/config.py.sample config/config.py
fi

# Install systemctl
cd "${BASE_DIR}"
echo "Installation du service-file systemd…"
envsubst '${USER} ${BASE_DIR}' <"${BASE_DIR}/installation/reservation_animations.service" | sudo tee /etc/systemd/system/reservation_animations.service && sudo systemctl daemon-reload || exit 1
if [[ "${MODE}" != "dev" ]]; then
  echo "Activation de reservation_animations au démarrage…"
  sudo systemctl enable reservation_animations || exit 1
fi



#########################
# Install FRONTEND
#########################
cd "${BASE_DIR}"/frontend

# Copy the custom components
if [[ ! -f "${BASE_DIR}"/frontend/src/config/config.js ]]; then
  echo "Création des fichiers de customisation du frontend: Configuration..."
  cp -n  src/config/config.js.sample src/config/config.js
fi
if [[ ! -f "${BASE_DIR}"/frontend/src/views/config.js ]]; then
  echo "Création des fichiers de customisation du frontend: Page d'information..."
  cp -n  src/views/Informations.vue.sample src/views/Informations.vue
fi

npm ci
npm run build
