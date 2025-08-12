# VPS Deployment Guide Template

Пошаговое руководство по безопасному развертыванию Business Trip Report Bot на VPS сервере.

## 📋 Информация о сервере

**IP адрес VPS:** `YOUR_SERVER_IP`  
**SSH порт (стандартный):** `22`  
**SSH порт (после настройки):** `YOUR_CUSTOM_PORT`  
**Пользователи:**
- `root` - для первоначальной настройки
- `admin_user` - для административных задач
- `bot_user` - для работы бота

**Быстрые команды подключения:**
```bash
# Первоначальное подключение
ssh root@YOUR_SERVER_IP

# После настройки безопасности
ssh -p YOUR_CUSTOM_PORT admin_user@YOUR_SERVER_IP    # административные задачи
ssh -p YOUR_CUSTOM_PORT bot_user@YOUR_SERVER_IP      # работа с ботом
```

## 🔒 Этапы развертывания

### 1. Первоначальная настройка безопасности VPS

#### 1.1 Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git ufw fail2ban htop nano
```

#### 1.2 Создание пользователей
```bash
# Создание административного пользователя
sudo adduser admin_user
sudo usermod -aG sudo admin_user

# Создание пользователя для бота (БЕЗ sudo прав)
sudo adduser bot_user
```

#### 1.3 Настройка SSH безопасности
```bash
sudo nano /etc/ssh/sshd_config

# Основные настройки:
Port YOUR_CUSTOM_PORT
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers bot_user admin_user
MaxAuthTries 3
```

### 2. Настройка файрвола (UFW)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow YOUR_CUSTOM_PORT/tcp
sudo ufw enable
```

### 3. Настройка Fail2Ban
```bash
sudo nano /etc/fail2ban/jail.local

[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = YOUR_CUSTOM_PORT
maxretry = 3
bantime = 3600
```

### 4. Установка приложения
```bash
# Подключение под пользователем бота
ssh -p YOUR_CUSTOM_PORT bot_user@YOUR_SERVER_IP

# Клонирование репозитория
git clone https://github.com/YOUR_USERNAME/business_trip_report.git
cd business_trip_report

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка переменных окружения
nano .env
# BOT_TOKEN=your_bot_token_here
```

### 5. Настройка systemd сервиса
```bash
# Подключение под admin пользователем
sudo nano /etc/systemd/system/business-trip-bot.service

[Unit]
Description=Business Trip Report Bot
After=network.target

[Service]
Type=simple
User=bot_user
Group=bot_user
WorkingDirectory=/home/bot_user/business_trip_report
Environment=PATH=/home/bot_user/business_trip_report/venv/bin
ExecStart=/home/bot_user/business_trip_report/venv/bin/python -m bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6. Запуск и мониторинг
```bash
sudo systemctl daemon-reload
sudo systemctl enable business-trip-bot
sudo systemctl start business-trip-bot
sudo systemctl status business-trip-bot
```

## 🔧 Команды для управления

```bash
# Просмотр статуса
sudo systemctl status business-trip-bot

# Просмотр логов
sudo journalctl -u business-trip-bot -f

# Перезапуск
sudo systemctl restart business-trip-bot
```

## 🛡️ Рекомендации по безопасности

1. **Смените стандартный SSH порт** на нестандартный
2. **Отключите вход по паролю**, используйте только SSH ключи
3. **Настройте файрвол** для блокировки ненужных портов
4. **Используйте Fail2Ban** для защиты от брутфорса
5. **Создайте отдельного пользователя** для бота без sudo прав
6. **Регулярно обновляйте систему** и зависимости

## 📋 Чеклист развертывания

- [ ] Обновлена система
- [ ] Созданы пользователи
- [ ] Настроены SSH ключи
- [ ] Настроен файрвол
- [ ] Настроен Fail2Ban
- [ ] Установлен Python
- [ ] Склонирован репозиторий
- [ ] Создано виртуальное окружение
- [ ] Настроены переменные окружения
- [ ] Настроен systemd сервис
- [ ] Протестирована работа бота

## ⚠️ Важно

- НЕ коммитьте файлы с реальными IP адресами и конфигурациями
- Используйте переменные окружения для чувствительных данных
- Регулярно делайте бэкапы базы данных
- Мониторьте логи на предмет подозрительной активности

---

**Примечание:** Этот шаблон содержит общие инструкции. Создайте собственную копию с реальными данными для локального использования и НЕ добавляйте ее в Git репозиторий.
