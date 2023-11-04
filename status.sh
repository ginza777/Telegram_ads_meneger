#!/bin/bash

# Celery xizmati statusini chiqarish
sudo systemctl status celery_ads_manager

# Celery beat xizmati statusini chiqarish (agar kerak bo'lsa)
sudo systemctl status celery_ads_manager_beat

# Telegram_ads.socket va telegram_ads.service xizmatlari statusini chiqarish
sudo systemctl status telegram_ads.socket
sudo systemctl status telegram_ads.service

# client.service xizmati statusini chiqarish (agar kerak bo'lsa)
sudo systemctl status client.service

# Nginx xizmati statusini chiqarish
sudo systemctl status nginx
