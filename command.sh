#!/bin/bash

# Systemd xizmatlarini qayta boshlash
sudo systemctl daemon-reload

# Celery xizmatini qayta boshlash
sudo systemctl restart celery_ads_manager

# Celery beat xizmatini qayta boshlash (agar kerak bo'lsa)
sudo systemctl restart celery_ads_manager_beat

# Telegram_ads.socket va telegram_ads.service xizmatlarini qayta boshlash
sudo systemctl restart telegram_ads.socket
sudo systemctl restart telegram_ads.service

# client.service xizmatini qayta boshlash (agar kerak bo'lsa)
sudo systemctl restart client.service

# Nginx konfiguratsiyasini tekshirish va Nginx ni qayta boshlash
sudo nginx -t && sudo systemctl restart nginx